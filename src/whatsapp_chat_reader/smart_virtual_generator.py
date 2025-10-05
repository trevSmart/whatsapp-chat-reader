import os
import json
import base64
import mimetypes
from typing import List, Dict
from .parser import WhatsAppMessage

class SmartVirtualHTMLGenerator:
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

            .progress-bar {
                width: 100%;
                height: 4px;
                background: #e0e0e0;
                border-radius: 2px;
                overflow: hidden;
                margin: 10px 0;
            }

            .progress-fill {
                height: 100%;
                background: #075e54;
                transition: width 0.3s ease;
                width: 0%;
            }

            .attachment-placeholder {
                padding: 20px;
                text-align: center;
                background: #f8f9fa;
                border: 2px dashed #ddd;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s;
            }

            .attachment-placeholder:hover {
                background: #e9ecef;
                border-color: #075e54;
            }

            .attachment-placeholder .icon {
                font-size: 32px;
                margin-bottom: 10px;
                color: #075e54;
            }

            .attachment-placeholder .text {
                font-weight: bold;
                color: #333;
                margin-bottom: 5px;
            }

            .attachment-placeholder .subtext {
                font-size: 12px;
                color: #666;
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

    def create_attachment_metadata(self, attachment_name: str, attachment_path: str) -> Dict:
        """Create attachment metadata without Base64 data."""
        if not os.path.exists(attachment_path):
            return {
                'name': attachment_name,
                'type': 'file',
                'exists': False,
                'size': 'File not found',
                'path': attachment_path
            }

        file_size = self.get_file_size(attachment_path)

        if self.is_image(attachment_name):
            return {
                'name': attachment_name,
                'type': 'image',
                'exists': True,
                'size': file_size,
                'path': attachment_path
            }
        elif self.is_video(attachment_name):
            return {
                'name': attachment_name,
                'type': 'video',
                'exists': True,
                'size': file_size,
                'path': attachment_path
            }
        elif self.is_audio(attachment_name):
            return {
                'name': attachment_name,
                'type': 'audio',
                'exists': True,
                'size': file_size,
                'path': attachment_path
            }
        else:
            return {
                'name': attachment_name,
                'type': 'file',
                'exists': True,
                'size': file_size,
                'path': attachment_path
            }

    def extract_urls(self, text: str) -> str:
        """Extract URLs from text and make them clickable."""
        import re
        url_pattern = re.compile(r'https?://[^\s]+')
        return url_pattern.sub(r'<a href="\g<0>" class="url-link" target="_blank">\g<0></a>', text)

    def generate_html(self, messages: List[WhatsAppMessage], attachment_map: Dict[str, str], chat_name: str = "WhatsApp Chat") -> str:
        """Generate HTML with smart virtual scrolling and lazy loading."""

        print("Processant missatges per chunks intel·ligents...")

        # Configuration
        CHUNK_SIZE = 200  # Messages per chunk
        total_messages = len(messages)
        total_chunks = (total_messages + CHUNK_SIZE - 1) // CHUNK_SIZE

        print(f"Dividint {total_messages} missatges en {total_chunks} chunks de {CHUNK_SIZE} missatges...")

        # Process messages in chunks (without Base64 data)
        chunks = []
        for i in range(0, total_messages, CHUNK_SIZE):
            chunk_messages = messages[i:i + CHUNK_SIZE]
            chunk_data = []

            for message in chunk_messages:
                message_data = {
                    'timestamp': message.timestamp.isoformat(),
                    'sender': message.sender,
                    'content': message.content,
                    'is_system_message': message.is_system_message,
                    'attachments': []
                }

                # Process attachments (metadata only)
                for attachment_name in message.attachments:
                    attachment_path = attachment_map.get(attachment_name)
                    if attachment_path:
                        attachment_data = self.create_attachment_metadata(attachment_name, attachment_path)
                        message_data['attachments'].append(attachment_data)
                    else:
                        message_data['attachments'].append({
                            'name': attachment_name,
                            'type': 'file',
                            'exists': False,
                            'size': 'File not found',
                            'path': ''
                        })

                chunk_data.append(message_data)

            chunks.append(chunk_data)
            if len(chunks) % 10 == 0:
                print(f"Processat chunk {len(chunks)}/{total_chunks}")

        # Statistics
        total_attachments = sum(len(msg.attachments) for msg in messages)
        unique_senders = len(set(msg.sender for msg in messages))

        # Generate JavaScript chunks (much smaller without Base64)
        chunks_js = []
        for i, chunk in enumerate(chunks):
            chunk_json = json.dumps(chunk, ensure_ascii=False)
            chunks_js.append(f"window.chunk_{i:04d} = {chunk_json};")

        chunks_js_str = "\n".join(chunks_js)

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
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
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
        // Chunks data embedded as JavaScript variables (metadata only)
        {chunks_js_str}

        class SmartVirtualChat {{
            constructor() {{
                this.messagesContainer = document.getElementById('messagesContainer');
                this.searchInput = document.getElementById('searchInput');
                this.scrollIndicator = document.getElementById('scrollIndicator');
                this.scrollInfo = document.getElementById('scrollInfo');
                this.progressFill = document.getElementById('progressFill');

                this.isLoading = false;
                this.searchQuery = '';
                this.totalChunks = {total_chunks};
                this.chunkSize = {CHUNK_SIZE};
                this.totalMessages = {total_messages};

                this.loadedChunks = new Set();
                this.allMessages = [];
                this.filteredMessages = [];
                this.loadedAttachments = new Map();

                this.init();
            }}

            init() {{
                this.loadInitialChunks();
                this.setupEventListeners();
            }}

            setupEventListeners() {{
                // Scroll event for virtual scrolling and lazy loading
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

            loadInitialChunks() {{
                // Load first few chunks immediately
                const initialChunks = Math.min(5, this.totalChunks);
                for (let i = 0; i < initialChunks; i++) {{
                    this.loadChunk(i);
                }}
                this.renderMessages();
            }}

            loadChunk(chunkIndex) {{
                if (this.loadedChunks.has(chunkIndex)) {{
                    return;
                }}

                try {{
                    const chunkData = window[`chunk_${{chunkIndex.toString().padStart(4, '0')}}`];
                    if (chunkData) {{
                        this.allMessages.push(...chunkData);
                        this.loadedChunks.add(chunkIndex);
                        this.updateProgress();

                        // Update filtered messages if search is active
                        if (this.searchQuery) {{
                            this.filterMessages();
                        }} else {{
                            this.renderMessages();
                        }}
                    }}
                }} catch (error) {{
                    console.error(`Error loading chunk ${{chunkIndex}}:`, error);
                }}
            }}

            updateProgress() {{
                const loadedMessages = this.allMessages.length;
                const progress = (loadedMessages / this.totalMessages) * 100;
                this.progressFill.style.width = `${{progress}}%`;
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

                // Create placeholder for lazy loading
                const attachmentId = `attachment_${{Math.random().toString(36).substr(2, 9)}}`;

                if (attachment.type === 'image') {{
                    return `
                        <div class="attachment">
                            <div class="attachment-placeholder" onclick="smartChat.loadAttachment('${{attachmentId}}', '${{attachment.path}}', 'image')">
                                <div class="icon">🖼️</div>
                                <div class="text">Click per carregar imatge</div>
                                <div class="subtext">${{attachment.name}} (${{attachment.size}})</div>
                            </div>
                            <div id="${{attachmentId}}" style="display: none;"></div>
                        </div>
                    `;
                }} else if (attachment.type === 'video') {{
                    return `
                        <div class="attachment">
                            <div class="attachment-placeholder" onclick="smartChat.loadAttachment('${{attachmentId}}', '${{attachment.path}}', 'video')">
                                <div class="icon">🎥</div>
                                <div class="text">Click per carregar vídeo</div>
                                <div class="subtext">${{attachment.name}} (${{attachment.size}})</div>
                            </div>
                            <div id="${{attachmentId}}" style="display: none;"></div>
                        </div>
                    `;
                }} else if (attachment.type === 'audio') {{
                    return `
                        <div class="attachment">
                            <div class="attachment-placeholder" onclick="smartChat.loadAttachment('${{attachmentId}}', '${{attachment.path}}', 'audio')">
                                <div class="icon">🎵</div>
                                <div class="text">Click per carregar àudio</div>
                                <div class="subtext">${{attachment.name}} (${{attachment.size}})</div>
                            </div>
                            <div id="${{attachmentId}}" style="display: none;"></div>
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
                                <a href="file://${{attachment.path}}" class="download-link" target="_blank">Descarregar</a>
                            </div>
                        </div>
                    `;
                }}
            }}

            async loadAttachment(attachmentId, filePath, type) {{
                if (this.loadedAttachments.has(attachmentId)) {{
                    return;
                }}

                try {{
                    const response = await fetch(`file://${{filePath}}`);
                    const blob = await response.blob();
                    const reader = new FileReader();

                    reader.onload = () => {{
                        const container = document.getElementById(attachmentId);
                        const placeholder = container.previousElementSibling;

                        if (type === 'image') {{
                            container.innerHTML = `<img src="${{reader.result}}" alt="Attachment" style="max-width: 100%; height: auto;" />`;
                        }} else if (type === 'video') {{
                            container.innerHTML = `<video controls style="max-width: 100%; height: auto;"><source src="${{reader.result}}" type="video/mp4">El teu navegador no suporta el tag de vídeo.</video>`;
                        }} else if (type === 'audio') {{
                            container.innerHTML = `<audio controls style="width: 100%;"><source src="${{reader.result}}" type="audio/mpeg">El teu navegador no suporta el tag d'àudio.</audio>`;
                        }}

                        container.style.display = 'block';
                        placeholder.style.display = 'none';
                        this.loadedAttachments.set(attachmentId, true);
                    }};

                    reader.readAsDataURL(blob);
                }} catch (error) {{
                    console.error('Error loading attachment:', error);
                    const container = document.getElementById(attachmentId);
                    container.innerHTML = '<div class="error-message">Error carregant adjunt</div>';
                    container.style.display = 'block';
                }}
            }}

            extractUrls(text) {{
                const urlPattern = /https?:\\/\\/[^\\s]+/g;
                return text.replace(urlPattern, '<a href="$&" class="url-link" target="_blank">$&</a>');
            }}

            handleScroll() {{
                this.showScrollIndicator();
                this.updateScrollInfo();

                // Lazy load chunks based on scroll position
                this.loadChunksOnScroll();

                // Re-render messages for virtual scrolling
                setTimeout(() => {{
                    this.renderMessages();
                }}, 100);
            }}

            loadChunksOnScroll() {{
                const container = this.messagesContainer;
                const scrollTop = container.scrollTop;
                const scrollHeight = container.scrollHeight;
                const clientHeight = container.clientHeight;

                // Calculate which chunks should be loaded based on scroll position
                const scrollPercentage = scrollTop / (scrollHeight - clientHeight);
                const targetChunk = Math.floor(scrollPercentage * this.totalChunks);

                // Load chunks around current position
                const loadRange = 3; // Load 3 chunks before and after current position
                for (let i = Math.max(0, targetChunk - loadRange);
                     i <= Math.min(this.totalChunks - 1, targetChunk + loadRange);
                     i++) {{
                    this.loadChunk(i);
                }}
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
                const loadedMessages = this.allMessages.length;

                this.scrollInfo.innerHTML = `
                    ${{percentage}}%<br>
                    Carregats: ${{loadedMessages}}/${{this.totalMessages}}<br>
                    Chunks: ${{this.loadedChunks.size}}/${{this.totalChunks}}
                `;
            }}

            showError(message) {{
                this.messagesContainer.innerHTML = `<div class="error-message">${{message}}</div>`;
            }}
        }}

        // Initialize smart virtual chat when page loads
        let smartChat;
        document.addEventListener('DOMContentLoaded', () => {{
            smartChat = new SmartVirtualChat();
        }});
    </script>
</body>
</html>'''

        return html_content
