import os
import json
import base64
import mimetypes
from typing import List, Dict
from .parser import WhatsAppMessage

class EmbeddedVirtualHTMLGenerator:
    def __init__(self):
        self.css_styles = """
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f0f0f0;
                line-height: 1.6;
            }

            .chat-container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                overflow: hidden;
                height: 100vh;
                display: flex;
                flex-direction: column;
            }

            .chat-header {
                background: #075e54;
                color: white;
                padding: 20px;
                text-align: center;
                flex-shrink: 0;
            }

            .chat-header h1 {
                margin: 0;
                font-size: 24px;
            }

            .search-container {
                padding: 15px;
                background: #f8f9fa;
                border-bottom: 1px solid #eee;
                flex-shrink: 0;
            }

            .search-input {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 20px;
                font-size: 16px;
                outline: none;
            }

            .search-input:focus {
                border-color: #075e54;
            }

            .messages-container {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                position: relative;
            }

            .loading {
                text-align: center;
                padding: 20px;
                color: #666;
            }

            .message {
                margin-bottom: 15px;
                display: flex;
                flex-direction: column;
                opacity: 0;
                animation: fadeIn 0.3s ease-in forwards;
            }

            @keyframes fadeIn {
                to { opacity: 1; }
            }

            .message-header {
                font-size: 12px;
                color: #666;
                margin-bottom: 5px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .sender {
                font-weight: bold;
                color: #075e54;
            }

            .timestamp {
                color: #999;
            }

            .message-content {
                background: #e7f3ff;
                padding: 10px 15px;
                border-radius: 10px;
                border-top-left-radius: 0;
                word-wrap: break-word;
            }

            .message.system .message-content {
                background: #f0f0f0;
                color: #666;
                font-style: italic;
            }

            .attachments {
                margin-top: 10px;
            }

            .attachment {
                margin-bottom: 10px;
                border: 1px solid #ddd;
                border-radius: 8px;
                overflow: hidden;
            }

            .attachment img {
                max-width: 100%;
                height: auto;
                display: block;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin: 5px 0;
            }

            .attachment video {
                max-width: 100%;
                height: auto;
                display: block;
            }

            .attachment audio {
                width: 100%;
                margin: 10px 0;
            }

            .attachment-file {
                padding: 15px;
                background: #f8f9fa;
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .file-icon {
                font-size: 24px;
                color: #075e54;
            }

            .file-info {
                flex: 1;
            }

            .file-name {
                font-weight: bold;
                color: #333;
            }

            .file-size {
                font-size: 12px;
                color: #666;
            }

            .download-link {
                color: #075e54;
                text-decoration: none;
                font-size: 12px;
                padding: 5px 10px;
                border: 1px solid #075e54;
                border-radius: 4px;
                transition: all 0.3s;
            }

            .download-link:hover {
                background: #075e54;
                color: white;
            }

            .url-link {
                color: #075e54;
                text-decoration: none;
                word-break: break-all;
            }

            .url-link:hover {
                text-decoration: underline;
            }

            .stats {
                background: #f8f9fa;
                padding: 15px;
                border-top: 1px solid #eee;
                font-size: 14px;
                color: #666;
                text-align: center;
                flex-shrink: 0;
            }

            .scroll-indicator {
                position: fixed;
                top: 50%;
                right: 20px;
                transform: translateY(-50%);
                background: rgba(0,0,0,0.7);
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 12px;
                z-index: 1000;
            }

            .error-message {
                background: #ffebee;
                color: #c62828;
                padding: 15px;
                margin: 10px;
                border-radius: 5px;
                border-left: 4px solid #c62828;
            }
        </style>
        """

    def get_file_extension(self, filename: str) -> str:
        """Get file extension from filename."""
        return os.path.splitext(filename)[1].lower()

    def is_image(self, filename: str) -> bool:
        """Check if file is an image."""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}
        return self.get_file_extension(filename) in image_extensions

    def is_video(self, filename: str) -> bool:
        """Check if file is a video."""
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.3gp'}
        return self.get_file_extension(filename) in video_extensions

    def is_audio(self, filename: str) -> bool:
        """Check if file is an audio file."""
        audio_extensions = {'.mp3', '.wav', '.ogg', '.m4a', '.aac', '.flac', '.opus'}
        return self.get_file_extension(filename) in audio_extensions

    def encode_file_to_base64(self, file_path: str) -> str:
        """Encode file to base64 for embedding in HTML."""
        try:
            with open(file_path, 'rb') as file:
                return base64.b64encode(file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error encoding file {file_path}: {e}")
            return ""

    def get_file_size(self, file_path: str) -> str:
        """Get human readable file size."""
        try:
            size = os.path.getsize(file_path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except:
            return "Unknown size"

    def create_attachment_data(self, attachment_name: str, attachment_path: str) -> Dict:
        """Create attachment data for JSON serialization."""
        if not os.path.exists(attachment_path):
            return {
                'name': attachment_name,
                'type': 'file',
                'exists': False,
                'size': 'File not found'
            }

        file_size = self.get_file_size(attachment_path)

        if self.is_image(attachment_name):
            return {
                'name': attachment_name,
                'type': 'image',
                'exists': True,
                'size': file_size,
                'base64': self.encode_file_to_base64(attachment_path)
            }
        elif self.is_video(attachment_name):
            return {
                'name': attachment_name,
                'type': 'video',
                'exists': True,
                'size': file_size,
                'base64': self.encode_file_to_base64(attachment_path)
            }
        elif self.is_audio(attachment_name):
            return {
                'name': attachment_name,
                'type': 'audio',
                'exists': True,
                'size': file_size,
                'base64': self.encode_file_to_base64(attachment_path)
            }
        else:
            return {
                'name': attachment_name,
                'type': 'file',
                'exists': True,
                'size': file_size
            }

    def extract_urls(self, text: str) -> str:
        """Extract URLs from text and make them clickable."""
        import re
        url_pattern = re.compile(r'https?://[^\s]+')
        return url_pattern.sub(r'<a href="\g<0>" class="url-link" target="_blank">\g<0></a>', text)

    def generate_html(self, messages: List[WhatsAppMessage], attachment_map: Dict[str, str], chat_name: str = "WhatsApp Chat") -> str:
        """Generate HTML with embedded virtual scrolling."""

        print("Processant missatges per integració...")

        # Process all messages and attachments
        processed_messages = []
        for message in messages:
            message_data = {
                'timestamp': message.timestamp.isoformat(),
                'sender': message.sender,
                'content': message.content,
                'is_system_message': message.is_system_message,
                'attachments': []
            }

            # Process attachments
            for attachment_name in message.attachments:
                attachment_path = attachment_map.get(attachment_name)
                if attachment_path:
                    attachment_data = self.create_attachment_data(attachment_name, attachment_path)
                    message_data['attachments'].append(attachment_data)
                else:
                    message_data['attachments'].append({
                        'name': attachment_name,
                        'type': 'file',
                        'exists': False,
                        'size': 'File not found'
                    })

            processed_messages.append(message_data)

        # Statistics
        total_messages = len(messages)
        total_attachments = sum(len(msg.attachments) for msg in messages)
        unique_senders = len(set(msg.sender for msg in messages))

        # Convert to JSON string for embedding
        messages_json = json.dumps(processed_messages, ensure_ascii=False)

        html_content = f'''<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{chat_name}</title>
    {self.css_styles}
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>{chat_name}</h1>
        </div>

        <div class="search-container">
            <input type="text" class="search-input" placeholder="Cerca missatges..." id="searchInput">
        </div>

        <div class="messages-container" id="messagesContainer">
            <div class="loading">Carregant missatges...</div>
        </div>

        <div class="stats" id="stats">
            Total missatges: {total_messages} |
            Total adjunts: {total_attachments} |
            Participants: {unique_senders}
        </div>
    </div>

    <div class="scroll-indicator" id="scrollIndicator" style="display: none;">
        <div id="scrollInfo">Carregant...</div>
    </div>

    <script>
        class EmbeddedVirtualChat {{
            constructor() {{
                this.messagesContainer = document.getElementById('messagesContainer');
                this.searchInput = document.getElementById('searchInput');
                this.scrollIndicator = document.getElementById('scrollIndicator');
                this.scrollInfo = document.getElementById('scrollInfo');

                this.isLoading = false;
                this.searchQuery = '';
                this.allMessages = {messages_json};
                this.filteredMessages = [...this.allMessages];

                this.init();
            }}

            init() {{
                this.renderMessages();
                this.setupEventListeners();
            }}

            setupEventListeners() {{
                // Scroll event for virtual scrolling
                this.messagesContainer.addEventListener('scroll', () => {{
                    this.handleScroll();
                }});

                // Search input
                this.searchInput.addEventListener('input', (e) => {{
                    clearTimeout(this.searchTimeout);
                    this.searchTimeout = setTimeout(() => {{
                        this.searchQuery = e.target.value;
                        this.filterMessages();
                    }}, 300);
                }});
            }}

            filterMessages() {{
                if (!this.searchQuery.trim()) {{
                    this.filteredMessages = [...this.allMessages];
                }} else {{
                    const query = this.searchQuery.toLowerCase();
                    this.filteredMessages = this.allMessages.filter(message =>
                        message.content.toLowerCase().includes(query) ||
                        message.sender.toLowerCase().includes(query)
                    );
                }}
                this.renderMessages();
            }}

            renderMessages() {{
                this.messagesContainer.innerHTML = '';

                if (this.filteredMessages.length === 0) {{
                    this.messagesContainer.innerHTML = '<div class="loading">No s\\'han trobat missatges.</div>';
                    return;
                }}

                // Render only visible messages (virtual scrolling)
                const containerHeight = this.messagesContainer.clientHeight;
                const scrollTop = this.messagesContainer.scrollTop;
                const itemHeight = 100; // Approximate message height

                const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - 10);
                const endIndex = Math.min(this.filteredMessages.length, startIndex + Math.ceil(containerHeight / itemHeight) + 20);

                // Create spacer for virtual scrolling
                const topSpacer = document.createElement('div');
                topSpacer.style.height = `${{startIndex * itemHeight}}px`;
                this.messagesContainer.appendChild(topSpacer);

                // Render visible messages
                for (let i = startIndex; i < endIndex; i++) {{
                    const message = this.filteredMessages[i];
                    const messageElement = this.createMessageElement(message);
                    this.messagesContainer.appendChild(messageElement);
                }}

                // Create bottom spacer
                const bottomSpacer = document.createElement('div');
                bottomSpacer.style.height = `${{(this.filteredMessages.length - endIndex) * itemHeight}}px`;
                this.messagesContainer.appendChild(bottomSpacer);
            }}

            createMessageElement(message) {{
                const messageDiv = document.createElement('div');
                messageDiv.className = `message${{message.is_system_message ? ' system' : ''}}`;

                const timestamp = new Date(message.timestamp).toLocaleString('ca-ES');

                let attachmentsHtml = '';
                if (message.attachments && message.attachments.length > 0) {{
                    attachmentsHtml = '<div class="attachments">';
                    message.attachments.forEach(attachment => {{
                        attachmentsHtml += this.createAttachmentHtml(attachment);
                    }});
                    attachmentsHtml += '</div>';
                }}

                const contentWithUrls = this.extractUrls(message.content);

                messageDiv.innerHTML = `
                    <div class="message-header">
                        <span class="sender">${{message.sender}}</span>
                        <span class="timestamp">${{timestamp}}</span>
                    </div>
                    ${{message.content ? `<div class="message-content">${{contentWithUrls}}</div>` : ''}}
                    ${{attachmentsHtml}}
                `;

                return messageDiv;
            }}

            createAttachmentHtml(attachment) {{
                if (!attachment.exists) {{
                    return `
                        <div class="attachment">
                            <div class="attachment-file">
                                <span class="file-icon">📎</span>
                                <div class="file-info">
                                    <div class="file-name">${{attachment.name}}</div>
                                    <div class="file-size">${{attachment.size}}</div>
                                </div>
                            </div>
                        </div>
                    `;
                }}

                if (attachment.type === 'image') {{
                    return `
                        <div class="attachment">
                            <img src="data:image/jpeg;base64,${{attachment.base64}}" alt="${{attachment.name}}" />
                        </div>
                    `;
                }} else if (attachment.type === 'video') {{
                    return `
                        <div class="attachment">
                            <video controls>
                                <source src="data:video/mp4;base64,${{attachment.base64}}" type="video/mp4">
                                El teu navegador no suporta el tag de vídeo.
                            </video>
                        </div>
                    `;
                }} else if (attachment.type === 'audio') {{
                    return `
                        <div class="attachment">
                            <audio controls>
                                <source src="data:audio/mpeg;base64,${{attachment.base64}}" type="audio/mpeg">
                                El teu navegador no suporta el tag d'àudio.
                            </audio>
                        </div>
                    `;
                }} else {{
                    return `
                        <div class="attachment">
                            <div class="attachment-file">
                                <span class="file-icon">📄</span>
                                <div class="file-info">
                                    <div class="file-name">${{attachment.name}}</div>
                                    <div class="file-size">${{attachment.size}}</div>
                                </div>
                            </div>
                        </div>
                    `;
                }}
            }}

            extractUrls(text) {{
                const urlPattern = /https?:\\/\\/[^\\s]+/g;
                return text.replace(urlPattern, '<a href="$&" class="url-link" target="_blank">$&</a>');
            }}

            handleScroll() {{
                this.showScrollIndicator();
                this.updateScrollInfo();

                // Re-render messages for virtual scrolling
                setTimeout(() => {{
                    this.renderMessages();
                }}, 100);
            }}

            showScrollIndicator() {{
                this.scrollIndicator.style.display = 'block';
            }}

            hideScrollIndicator() {{
                setTimeout(() => {{
                    this.scrollIndicator.style.display = 'none';
                }}, 1000);
            }}

            updateScrollInfo() {{
                const container = this.messagesContainer;
                const scrollTop = container.scrollTop;
                const scrollHeight = container.scrollHeight;
                const clientHeight = container.clientHeight;

                const percentage = Math.round((scrollTop / (scrollHeight - clientHeight)) * 100);
                this.scrollInfo.innerHTML = `
                    ${{percentage}}%<br>
                    Missatges: ${{this.filteredMessages.length}}<br>
                    Total: ${{this.allMessages.length}}
                `;
            }}

            showError(message) {{
                this.messagesContainer.innerHTML = `<div class="error-message">${{message}}</div>`;
            }}
        }}

        // Initialize virtual chat when page loads
        document.addEventListener('DOMContentLoaded', () => {{
            new EmbeddedVirtualChat();
        }});
    </script>
</body>
</html>'''

        return html_content
