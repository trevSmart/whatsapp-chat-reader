import os
import base64
import mimetypes
from typing import List, Dict
from .parser import WhatsAppMessage

class HTMLGenerator:
    def __init__(self):
        self.css_styles = """
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
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
            }

            .chat-header {
                background: #075e54;
                color: white;
                padding: 20px;
                text-align: center;
            }

            .chat-header h1 {
                margin: 0;
                font-size: 24px;
            }

            .messages-container {
                padding: 20px;
                max-height: 80vh;
                overflow-y: auto;
            }

            .message {
                margin-bottom: 15px;
                display: flex;
                flex-direction: column;
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
                word-wrap: break-word;
                font-size: 14px;
            }

            .message.system .message-content {
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
                opacity: 0;
                transition: opacity 0.3s ease;
            }

            .attachment img.loaded {
                opacity: 1;
            }

            .image-placeholder {
                background: #f0f0f0;
                border: 2px dashed #ccc;
                border-radius: 8px;
                padding: 40px;
                text-align: center;
                color: #666;
                margin: 5px 0;
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .image-placeholder:hover {
                background: #e0e0e0;
                border-color: #999;
            }

            .media-placeholder {
                background: #f8f9fa;
                border: 2px solid #075e54;
                border-radius: 8px;
                padding: 30px;
                text-align: center;
                color: #075e54;
                margin: 5px 0;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 10px;
            }

            .media-placeholder:hover {
                background: #075e54;
                color: white;
            }

            .media-placeholder .icon {
                font-size: 48px;
                margin-bottom: 10px;
            }

            .media-placeholder .text {
                font-weight: bold;
                font-size: 16px;
            }

            .media-placeholder .subtext {
                font-size: 12px;
                opacity: 0.8;
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
        audio_extensions = {'.mp3', '.wav', '.ogg', '.m4a', '.aac', '.flac'}
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

    def generate_attachment_html(self, attachment_name: str, attachment_path: str, chat_dir: str = "") -> str:
        """Generate HTML for a single attachment with lazy loading and placeholders."""
        if not os.path.exists(attachment_path):
            return f'<div class="attachment"><div class="attachment-file"><span class="file-icon">📎</span><div class="file-info"><div class="file-name">{attachment_name}</div><div class="file-size">File not found</div></div></div></div>'

        file_size = self.get_file_size(attachment_path)

        if self.is_image(attachment_name):
            # Use relative path for lazy loading
            relative_path = attachment_name if not chat_dir else os.path.join(chat_dir, attachment_name)
            return f'''
            <div class="attachment">
                <div class="image-placeholder" onclick="loadImage(this)">
                    <div style="font-size: 24px; margin-bottom: 10px;">🖼️</div>
                    <div style="font-weight: bold;">Click to load image</div>
                    <div style="font-size: 12px; opacity: 0.7;">{attachment_name}</div>
                </div>
                <img data-src="{relative_path}" alt="{attachment_name}" style="display: none;" />
            </div>
            '''

        elif self.is_video(attachment_name):
            try:
                base64_data = self.encode_file_to_base64(attachment_path)
                mime_type = mimetypes.guess_type(attachment_path)[0] or 'video/mp4'
                return f'''
                <div class="attachment">
                    <div class="media-placeholder" onclick="loadVideo(this)">
                        <div class="icon">🎥</div>
                        <div class="text">Click to load video</div>
                        <div class="subtext">{attachment_name}</div>
                        <video data-src="data:{mime_type};base64,{base64_data}" controls style="display: none;">
                            Your browser does not support the video tag.
                        </video>
                    </div>
                    <div class="attachment-file">
                        <span class="file-icon">🎥</span>
                        <div class="file-info">
                            <div class="file-name">{attachment_name}</div>
                            <div class="file-size">{file_size}</div>
                        </div>
                        <a href="file://{attachment_path}" class="download-link" download>Download</a>
                    </div>
                </div>
                '''
            except Exception as e:
                print(f"Error processing video {attachment_name}: {e}")
                return f'<div class="attachment"><div class="attachment-file"><span class="file-icon">🎥</span><div class="file-info"><div class="file-name">{attachment_name}</div><div class="file-size">{file_size}</div></div><a href="file://{attachment_path}" class="download-link" download>Download</a></div></div>'

        elif self.is_audio(attachment_name):
            try:
                base64_data = self.encode_file_to_base64(attachment_path)
                mime_type = mimetypes.guess_type(attachment_path)[0] or 'audio/mpeg'
                return f'''
                <div class="attachment">
                    <div class="media-placeholder" onclick="loadAudio(this)">
                        <div class="icon">🎵</div>
                        <div class="text">Click to load audio</div>
                        <div class="subtext">{attachment_name}</div>
                        <audio data-src="data:{mime_type};base64,{base64_data}" controls style="display: none;">
                            Your browser does not support the audio tag.
                        </audio>
                    </div>
                    <div class="attachment-file">
                        <span class="file-icon">🎵</span>
                        <div class="file-info">
                            <div class="file-name">{attachment_name}</div>
                            <div class="file-size">{file_size}</div>
                        </div>
                        <a href="file://{attachment_path}" class="download-link" download>Download</a>
                    </div>
                </div>
                '''
            except Exception as e:
                print(f"Error processing audio {attachment_name}: {e}")
                return f'<div class="attachment"><div class="attachment-file"><span class="file-icon">🎵</span><div class="file-info"><div class="file-name">{attachment_name}</div><div class="file-size">{file_size}</div></div><a href="file://{attachment_path}" class="download-link" download>Download</a></div></div>'

        else:
            # Generic file
            return f'''
            <div class="attachment">
                <div class="attachment-file">
                    <span class="file-icon">📄</span>
                    <div class="file-info">
                        <div class="file-name">{attachment_name}</div>
                        <div class="file-size">{file_size}</div>
                    </div>
                    <a href="file://{attachment_path}" class="download-link" download>Download</a>
                </div>
            </div>
            '''

    def extract_urls(self, text: str) -> str:
        """Extract URLs from text and make them clickable."""
        import re
        url_pattern = re.compile(r'https?://[^\s]+')
        return url_pattern.sub(r'<a href="\g<0>" class="url-link" target="_blank">\g<0></a>', text)

    def generate_html(self, messages: List[WhatsAppMessage], attachment_map: Dict[str, str], chat_name: str = "WhatsApp Chat", chat_dir: str = "") -> str:
        """Generate complete HTML document."""
        html_parts = [
            '<!DOCTYPE html>',
            '<html lang="ca">',
            '<head>',
            '<meta charset="UTF-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'<title>{chat_name}</title>',
            self.css_styles,
            '</head>',
            '<body>',
            '<div class="chat-container">',
            f'<div class="chat-header"><h1>{chat_name}</h1></div>',
            '<div class="messages-container">'
        ]

        for message in messages:
            # Message header
            html_parts.append('<div class="message' + (' system' if message.is_system_message else '') + '">')
            html_parts.append('<div class="message-header">')
            html_parts.append(f'<span class="sender">{message.sender}</span>')
            html_parts.append(f'<span class="timestamp">{message.timestamp.strftime("%d/%m/%Y %H:%M:%S")}</span>')
            html_parts.append('</div>')

            # Message content
            if message.content.strip():
                content_with_urls = self.extract_urls(message.content)
                html_parts.append(f'<div class="message-content">{content_with_urls}</div>')

            # Attachments
            if message.attachments:
                html_parts.append('<div class="attachments">')
                for attachment_name in message.attachments:
                    attachment_path = attachment_map.get(attachment_name)
                    if attachment_path:
                        html_parts.append(self.generate_attachment_html(attachment_name, attachment_path, chat_dir))
                    else:
                        html_parts.append(f'<div class="attachment"><div class="attachment-file"><span class="file-icon">📎</span><div class="file-info"><div class="file-name">{attachment_name}</div><div class="file-size">File not found</div></div></div></div>')
                html_parts.append('</div>')

            html_parts.append('</div>')

        # Statistics
        total_messages = len(messages)
        total_attachments = sum(len(msg.attachments) for msg in messages)
        unique_senders = len(set(msg.sender for msg in messages))

        # JavaScript for lazy loading and media placeholders
        javascript = """
        <script>
            // Lazy loading for images
            function loadImage(placeholder) {
                const img = placeholder.querySelector('img[data-src]');
                if (img) {
                    img.src = img.dataset.src;
                    img.style.display = 'block';
                    img.classList.add('loaded');
                    placeholder.style.display = 'none';
                }
            }

            // Load video on click
            function loadVideo(placeholder) {
                const video = placeholder.querySelector('video[data-src]');
                if (video) {
                    video.src = video.dataset.src;
                    video.style.display = 'block';
                    placeholder.style.display = 'none';
                }
            }

            // Load audio on click
            function loadAudio(placeholder) {
                const audio = placeholder.querySelector('audio[data-src]');
                if (audio) {
                    audio.src = audio.dataset.src;
                    audio.style.display = 'block';
                    placeholder.style.display = 'none';
                }
            }

            // Intersection Observer for automatic lazy loading
            document.addEventListener('DOMContentLoaded', function() {
                if ('IntersectionObserver' in window) {
                    const imageObserver = new IntersectionObserver((entries, observer) => {
                        entries.forEach(entry => {
                            if (entry.isIntersecting) {
                                const img = entry.target;
                                const placeholder = img.closest('.attachment').querySelector('.image-placeholder');

                                if (img.dataset.src) {
                                    img.src = img.dataset.src;
                                    img.classList.add('loaded');
                                    img.style.display = 'block';
                                    if (placeholder) {
                                        placeholder.style.display = 'none';
                                    }
                                    observer.unobserve(img);
                                }
                            }
                        });
                    }, {
                        rootMargin: '50px 0px',
                        threshold: 0.1
                    });

                    // Observe all images with data-src
                    const lazyImages = document.querySelectorAll('img[data-src]');
                    lazyImages.forEach(img => imageObserver.observe(img));
                }
            });
        </script>
        """

        html_parts.extend([
            '</div>',  # messages-container
            f'<div class="stats">',
            f'Total messages: {total_messages} | ',
            f'Total attachments: {total_attachments} | ',
            f'Participants: {unique_senders}',
            '</div>',
            '</div>',  # chat-container
            javascript,
            '</body>',
            '</html>'
        ])

        return '\n'.join(html_parts)
