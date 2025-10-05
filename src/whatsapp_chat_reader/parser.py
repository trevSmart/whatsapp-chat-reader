import re
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class WhatsAppMessage:
    timestamp: datetime
    sender: str
    content: str
    attachments: List[str]
    is_system_message: bool = False

class WhatsAppParser:
    def __init__(self):
        # Regex pattern to match WhatsApp message format
        # [date time] sender: message content
        # Note: Lines may start with zero-width characters like \u200e (LEFT-TO-RIGHT MARK)
        self.message_pattern = re.compile(
            r'^\u200e?\[(\d{1,2}/\d{1,2}/\d{2,4})\s+(\d{1,2}:\d{2}:\d{2})\]\s+([^:]+):\s+(.*)$',
            re.MULTILINE
        )

        # Pattern to match attachments
        self.attachment_pattern = re.compile(r'\u200e<adjunt:\s+([^>]+)>')

        # Pattern to match system messages (like encryption notice)
        # Note: Lines may start with zero-width characters like \u200e (LEFT-TO-RIGHT MARK)
        self.system_pattern = re.compile(r'^\u200e?\[(\d{1,2}/\d{1,2}/\d{2,4})\s+(\d{1,2}:\d{2}:\d{2})\]\s+([^:]+):\s+‎(.*)$')

    def parse_chat_file(self, file_path: str) -> List[WhatsAppMessage]:
        """Parse a WhatsApp chat export file and return list of messages."""
        messages = []

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.read()

        # Split content into lines and process
        lines = content.split('\n')
        current_message = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if this line is an attachment
            attachment_match = self.attachment_pattern.search(line)
            if attachment_match:
                attachment_name = attachment_match.group(1)
                if current_message:
                    current_message.attachments.append(attachment_name)
                continue

            # Check if this is a new message
            match = self.message_pattern.match(line)
            if match:
                # Save previous message if exists
                if current_message:
                    messages.append(current_message)

                # Parse new message
                date_str, time_str, sender, content = match.groups()

                # Parse timestamp
                try:
                    timestamp = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%y %H:%M:%S")
                except ValueError:
                    try:
                        timestamp = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M:%S")
                    except ValueError:
                        # Fallback to current time if parsing fails
                        timestamp = datetime.now()

                # Check if it's a system message
                is_system = sender.startswith('‎') or 'xifrats' in content.lower()

                # Extract attachments from content
                attachments = self.attachment_pattern.findall(content)

                # Remove attachment markers from content and strip zero-width characters
                clean_content = self.attachment_pattern.sub('', content).strip().strip('\u200e')

                current_message = WhatsAppMessage(
                    timestamp=timestamp,
                    sender=sender.strip('‎'),
                    content=clean_content,
                    attachments=attachments,
                    is_system_message=is_system
                )
            else:
                # This is a continuation of the previous message
                if current_message:
                    current_message.content += '\n' + line

        # Add the last message
        if current_message:
            messages.append(current_message)

        return messages

    def find_attachment_files(self, messages: List[WhatsAppMessage], chat_dir: str) -> Dict[str, str]:
        """Find actual attachment files in the directory and map them to message attachments."""
        attachment_map = {}

        if not os.path.exists(chat_dir):
            return attachment_map

        # Get all files in the directory
        for filename in os.listdir(chat_dir):
            file_path = os.path.join(chat_dir, filename)
            if os.path.isfile(file_path):
                attachment_map[filename] = file_path

        return attachment_map