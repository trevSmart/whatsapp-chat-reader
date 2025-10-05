import os
import json
import base64
import mimetypes
from typing import List, Dict, Generator
from .parser import WhatsAppMessage

class ProgressiveVirtualHTMLGenerator:
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
                font-size: 14px;
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

            .segment-indicator {
                width: 100%;
                height: 8px;
                background: #e0e0e0;
                border-radius: 2px;
                margin: 10px 0;
                position: relative;
                display: flex;
            }

            .segment {
                height: 100%;
                transition: background-color 0.3s ease;
                border-right: 1px solid #fff;
                box-sizing: border-box;
            }

            .segment.loaded {
                background: #4caf50;
            }

            .segment.unloaded {
                background: #f44336;
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

            .server-info {
                background: #e3f2fd;
                padding: 10px;
                margin: 10px;
                border-radius: 5px;
                border-left: 4px solid #2196f3;
                font-size: 14px;
            }

            .time-scrollbar-container {
                position: fixed;
                right: 0;
                top: 0;
                bottom: 0;
                width: 120px;
                background: rgba(0, 0, 0, 0.1);
                z-index: 1000;
                display: flex;
                flex-direction: column;
                padding: 10px 5px;
                box-sizing: border-box;
            }

            .time-scrollbar {
                position: relative;
                flex: 1;
                background: #e0e0e0;
                border-radius: 8px;
                cursor: pointer;
                margin: 5px 0;
            }

            .time-scrollbar-thumb {
                position: absolute;
                left: 0;
                right: 0;
                background: #075e54;
                border-radius: 8px;
                min-height: 30px;
                transition: background 0.2s;
                cursor: grab;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 10px;
                font-weight: bold;
                padding: 2px;
                text-align: center;
                line-height: 1.2;
            }

            .time-scrollbar-thumb:hover {
                background: #064d44;
            }

            .time-scrollbar-thumb:active {
                cursor: grabbing;
                background: #053b34;
            }

            .time-indicator {
                text-align: center;
                font-size: 11px;
                color: #333;
                font-weight: bold;
                margin: 5px 0;
                background: rgba(255, 255, 255, 0.9);
                padding: 5px;
                border-radius: 5px;
            }

            .time-label {
                font-size: 10px;
                color: #666;
            }

            .time-mark {
                position: absolute;
                left: 0;
                right: 0;
                height: 2px;
                background: #999;
                pointer-events: none;
                display: flex;
                align-items: center;
            }

            .time-mark::before {
                content: '';
                position: absolute;
                left: 0;
                right: 0;
                height: 2px;
                background: #999;
            }

            .time-mark-label {
                position: absolute;
                left: 100%;
                margin-left: 5px;
                font-size: 9px;
                color: #666;
                white-space: nowrap;
                background: rgba(255, 255, 255, 0.9);
                padding: 2px 4px;
                border-radius: 3px;
                transform: translateY(-50%);
                font-weight: normal;
                pointer-events: none;
                z-index: 1;
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

    def extract_urls(self, text: str) -> str:
        """Extract URLs from text and make them clickable."""
        import re
        url_pattern = re.compile(r'https?://[^\s]+')
        return url_pattern.sub(r'<a href="\g<0>" class="url-link" target="_blank">\g<0></a>', text)

    def generate_html(self, chat_file_path: str, attachment_dir: str, chat_name: str = "WhatsApp Chat") -> str:
        """Generate HTML with progressive loading from TXT file."""

        # Get file size for progress calculation
        try:
            file_size = os.path.getsize(chat_file_path)
            file_size_mb = file_size / (1024 * 1024)
        except:
            file_size = 0
            file_size_mb = 0

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
            <div class="segment-indicator" id="segmentIndicator">
                <!-- Segments will be dynamically generated -->
            </div>
        </div>

        <div class="messages-container" id="messagesContainer">
            <div class="loading">Carregant missatges...</div>
        </div>

        <div class="stats" id="stats">
            Carregant missatges del fitxer TXT...
        </div>
    </div>

    <div class="scroll-indicator" id="scrollIndicator" style="display: none;">
        <div id="scrollInfo">Carregant...</div>
    </div>

    <div class="time-scrollbar-container" id="timeScrollbarContainer">
        <div class="time-indicator">
            <div class="time-label">Data actual</div>
            <div id="currentTimeLabel">--</div>
        </div>
        <div class="time-scrollbar" id="timeScrollbar">
            <div class="time-scrollbar-thumb" id="timeScrollbarThumb"></div>
        </div>
        <div class="time-indicator">
            <div class="time-label">Temps transcorregut</div>
            <div id="timeProgress">--</div>
        </div>
    </div>

    <script>
        class ProgressiveVirtualChat {{
            constructor() {{
                this.messagesContainer = document.getElementById('messagesContainer');
                this.searchInput = document.getElementById('searchInput');
                this.scrollIndicator = document.getElementById('scrollIndicator');
                this.scrollInfo = document.getElementById('scrollInfo');
                this.segmentIndicator = document.getElementById('segmentIndicator');
                this.stats = document.getElementById('stats');
                this.timeScrollbar = document.getElementById('timeScrollbar');
                this.timeScrollbarThumb = document.getElementById('timeScrollbarThumb');
                this.currentTimeLabel = document.getElementById('currentTimeLabel');
                this.timeProgress = document.getElementById('timeProgress');

                this.isLoading = false;
                this.searchQuery = '';
                this.allMessages = [];
                this.filteredMessages = [];
                this.loadedAttachments = new Map();
                this.loadedAttachmentsContent = new Map(); // Store actual content (data URLs)
                this.scrollTimeout = null;
                this.lastScrollHeight = 0; // Track scroll height to prevent infinite loops
                this.loadedSegments = []; // Track loaded message ranges
                this.isRendering = false; // Track when we're inside renderMessages() to ignore scroll events
                
                // Time-based scrollbar properties
                this.firstTimestamp = null;
                this.lastTimestamp = null;
                this.totalTimeSpan = 0;
                this.isDraggingTimeScrollbar = false;
                this.isScrollingFromTimeScrollbar = false;

                // Configuration
                this.chatFileUrl = '{chat_file_path}';
                this.attachmentDir = '{attachment_dir}';
                this.chunkSize = 50; // Messages per request
                this.currentOffset = 0;
                this.isEndOfFile = false;
                this.totalMessages = 0;
                this.serverTotalMessages = null; // Total messages from server

                this.init();
            }}

            init() {{
                this.setupEventListeners();
                this.loadTimeRange();
                this.loadInitialMessages();
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

                // Time-based scrollbar events
                this.timeScrollbarThumb.addEventListener('mousedown', (e) => {{
                    this.isDraggingTimeScrollbar = true;
                    e.preventDefault();
                }});

                document.addEventListener('mousemove', (e) => {{
                    if (this.isDraggingTimeScrollbar) {{
                        this.handleTimeScrollbarDrag(e);
                    }}
                }});

                document.addEventListener('mouseup', () => {{
                    this.isDraggingTimeScrollbar = false;
                }});

                this.timeScrollbar.addEventListener('click', (e) => {{
                    if (e.target === this.timeScrollbar) {{
                        this.handleTimeScrollbarClick(e);
                    }}
                }});
            }}

            async loadInitialMessages() {{
                try {{
                    // Load first chunk
                    await this.loadMessagesChunk();
                    this.renderMessages();
                }} catch (error) {{
                    console.error('Error loading initial messages:', error);
                    this.showError('Error carregant missatges. Assegura\\'t que el servidor està executant-se.');
                }}
            }}

            async loadTimeRange() {{
                try {{
                    const response = await fetch('/api/time-range');
                    if (!response.ok) {{
                        throw new Error(`HTTP error! status: ${{response.status}}`);
                    }}
                    const data = await response.json();
                    
                    this.firstTimestamp = new Date(data.first_timestamp);
                    this.lastTimestamp = new Date(data.last_timestamp);
                    this.totalTimeSpan = this.lastTimestamp - this.firstTimestamp;
                    
                    console.log(`Time range: ${{this.firstTimestamp.toISOString()}} to ${{this.lastTimestamp.toISOString()}}`);
                    console.log(`Total time span: ${{this.totalTimeSpan / (1000 * 60 * 60 * 24)}} days`);
                    
                    this.updateTimeScrollbar(0, this.firstTimestamp);
                    this.renderTimeMarks();
                }} catch (error) {{
                    console.error('Error loading time range:', error);
                }}
            }}

            renderTimeMarks() {{
                if (!this.firstTimestamp || !this.lastTimestamp) {{
                    return;
                }}

                // Calculate time span in days
                const totalDays = this.totalTimeSpan / (1000 * 60 * 60 * 24);
                
                // Determine interval based on total time span
                let intervalMonths = 1;
                let intervalDays = 0;
                
                if (totalDays < 30) {{
                    // Less than 1 month: mark every week
                    intervalDays = 7;
                    intervalMonths = 0;
                }} else if (totalDays < 180) {{
                    // 1-6 months: mark every month
                    intervalMonths = 1;
                }} else if (totalDays < 365) {{
                    // 6-12 months: mark every 2 months
                    intervalMonths = 2;
                }} else if (totalDays < 730) {{
                    // 1-2 years: mark every 3 months
                    intervalMonths = 3;
                }} else {{
                    // More than 2 years: mark every 6 months
                    intervalMonths = 6;
                }}

                console.log(`Rendering time marks with interval: ${{intervalMonths > 0 ? intervalMonths + ' months' : intervalDays + ' days'}}`);

                // Generate marks
                const marks = [];
                let currentMark = new Date(this.firstTimestamp);
                
                if (intervalMonths > 0) {{
                    // Round to start of month
                    currentMark.setDate(1);
                    currentMark.setHours(0, 0, 0, 0);
                    
                    // Add marks at month intervals
                    while (currentMark <= this.lastTimestamp) {{
                        if (currentMark >= this.firstTimestamp) {{
                            marks.push(new Date(currentMark));
                        }}
                        currentMark.setMonth(currentMark.getMonth() + intervalMonths);
                    }}
                }} else {{
                    // Add marks at day intervals
                    currentMark.setHours(0, 0, 0, 0);
                    
                    while (currentMark <= this.lastTimestamp) {{
                        if (currentMark >= this.firstTimestamp) {{
                            marks.push(new Date(currentMark));
                        }}
                        currentMark.setDate(currentMark.getDate() + intervalDays);
                    }}
                }}

                // Remove existing marks
                const existingMarks = this.timeScrollbar.querySelectorAll('.time-mark');
                existingMarks.forEach(mark => mark.remove());

                // Add new marks
                marks.forEach(markTime => {{
                    const percentage = (markTime - this.firstTimestamp) / this.totalTimeSpan;
                    const markElement = document.createElement('div');
                    markElement.className = 'time-mark';
                    markElement.style.top = `${{percentage * 100}}%`;
                    
                    // Format label based on interval
                    let label;
                    if (intervalMonths > 0) {{
                        // Show month and year for monthly marks
                        label = markTime.toLocaleDateString('ca-ES', {{
                            month: 'short',
                            year: '2-digit'
                        }});
                    }} else {{
                        // Show day and month for weekly marks
                        label = markTime.toLocaleDateString('ca-ES', {{
                            day: 'numeric',
                            month: 'short'
                        }});
                    }}
                    
                    const labelElement = document.createElement('span');
                    labelElement.className = 'time-mark-label';
                    labelElement.textContent = label;
                    markElement.appendChild(labelElement);
                    
                    this.timeScrollbar.appendChild(markElement);
                }});

                console.log(`Rendered ${{marks.length}} time marks`);
            }}

            handleTimeScrollbarClick(e) {{
                const rect = this.timeScrollbar.getBoundingClientRect();
                const y = e.clientY - rect.top;
                const percentage = y / rect.height;
                this.scrollToTimePercentage(percentage);
            }}

            handleTimeScrollbarDrag(e) {{
                const rect = this.timeScrollbar.getBoundingClientRect();
                const y = Math.max(0, Math.min(e.clientY - rect.top, rect.height));
                const percentage = y / rect.height;
                this.scrollToTimePercentage(percentage);
            }}

            async scrollToTimePercentage(percentage) {{
                if (!this.firstTimestamp || !this.lastTimestamp) {{
                    return;
                }}

                // Calculate target timestamp
                const targetTime = new Date(this.firstTimestamp.getTime() + (percentage * this.totalTimeSpan));
                
                console.log(`Scrolling to time: ${{targetTime.toISOString()}} (${{Math.round(percentage * 100)}}%)`);
                
                // Update UI immediately
                this.updateTimeScrollbar(percentage, targetTime);
                this.updateTimeLabels(targetTime, percentage);
                
                // Load messages starting from this timestamp
                this.isScrollingFromTimeScrollbar = true;
                try {{
                    const response = await fetch(`/api/messages-by-time?timestamp=${{targetTime.toISOString()}}&limit=${{this.chunkSize}}`);
                    if (!response.ok) {{
                        throw new Error(`HTTP error! status: ${{response.status}}`);
                    }}
                    const data = await response.json();
                    
                    if (data.messages && data.messages.length > 0) {{
                        // Clear existing messages and load from this point
                        this.allMessages = data.messages;
                        this.currentOffset = data.offset + data.messages.length;
                        this.filteredMessages = [...this.allMessages];
                        
                        // Reset the isEndOfFile flag since we're jumping to a new position
                        this.isEndOfFile = false;
                        
                        if (data.total_messages && !this.serverTotalMessages) {{
                            this.serverTotalMessages = data.total_messages;
                        }}
                        
                        // Reset rendering and scroll to top of new messages
                        this.messagesContainer.scrollTop = 0;
                        this.renderMessages();
                        this.updateStats();
                    }}
                }} catch (error) {{
                    console.error('Error loading messages by time:', error);
                }} finally {{
                    this.isScrollingFromTimeScrollbar = false;
                }}
            }}

            updateTimeScrollbar(percentage, currentTime = null) {{
                const scrollbarHeight = this.timeScrollbar.offsetHeight;
                const thumbHeight = 30; // minimum height
                const maxThumbTop = scrollbarHeight - thumbHeight;
                
                const thumbTop = Math.max(0, Math.min(percentage * maxThumbTop, maxThumbTop));
                this.timeScrollbarThumb.style.top = `${{thumbTop}}px`;
                this.timeScrollbarThumb.style.height = `${{thumbHeight}}px`;
                
                // Update thumb text with date if provided
                if (currentTime) {{
                    const dateStr = currentTime.toLocaleDateString('ca-ES', {{
                        day: 'numeric',
                        month: 'short',
                        year: '2-digit'
                    }});
                    this.timeScrollbarThumb.textContent = dateStr;
                }}
            }}

            updateTimeLabels(currentTime, percentage) {{
                // Format current date
                const dateStr = currentTime.toLocaleDateString('ca-ES', {{
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric'
                }});
                this.currentTimeLabel.textContent = dateStr;
                
                // Calculate time elapsed
                const timeElapsed = currentTime - this.firstTimestamp;
                const daysElapsed = Math.floor(timeElapsed / (1000 * 60 * 60 * 24));
                const totalDays = Math.floor(this.totalTimeSpan / (1000 * 60 * 60 * 24));
                
                this.timeProgress.textContent = `${{daysElapsed}} / ${{totalDays}} dies`;
            }}

            updateTimeScrollbarFromMessages() {{
                if (!this.firstTimestamp || !this.lastTimestamp || this.filteredMessages.length === 0) {{
                    return;
                }}

                // Get the first visible message
                const container = this.messagesContainer;
                const scrollTop = container.scrollTop;
                const itemHeight = 100; // Approximate message height
                
                const visibleIndex = Math.floor(scrollTop / itemHeight);
                const visibleMessage = this.filteredMessages[Math.min(visibleIndex, this.filteredMessages.length - 1)];
                
                if (!visibleMessage || !visibleMessage.timestamp) {{
                    return;
                }}

                // Calculate time percentage based on visible message
                const messageTime = new Date(visibleMessage.timestamp);
                const timeElapsed = messageTime - this.firstTimestamp;
                const percentage = Math.max(0, Math.min(1, timeElapsed / this.totalTimeSpan));
                
                // Update scrollbar position
                this.updateTimeScrollbar(percentage, messageTime);
                this.updateTimeLabels(messageTime, percentage);
            }}

            async loadMessagesChunk() {{
                if (this.isEndOfFile || this.isLoading) {{
                    return;
                }}

                this.isLoading = true;
                console.log(`Loading chunk: offset=${{this.currentOffset}}, limit=${{this.chunkSize}}`);

                try {{
                    const response = await fetch(`/api/messages?offset=${{this.currentOffset}}&limit=${{this.chunkSize}}`);

                    if (!response.ok) {{
                        throw new Error(`HTTP error! status: ${{response.status}}`);
                    }}

                    const data = await response.json();

                    if (data.messages && data.messages.length > 0) {{
                        // Record the segment that was loaded
                        // Use data.offset from server response to ensure accuracy
                        const segmentStart = data.offset;
                        const segmentEnd = data.offset + data.messages.length;
                        
                        // Add to loaded segments (merge if overlapping with existing segments)
                        this.addLoadedSegment(segmentStart, segmentEnd);
                        
                        this.allMessages.push(...data.messages);
                        this.currentOffset += data.messages.length;
                        this.totalMessages += data.messages.length;

                        // Store the total messages count from server (only on first load)
                        if (data.total_messages && !this.serverTotalMessages) {{
                            this.serverTotalMessages = data.total_messages;
                            console.log(`Total messages in chat: ${{this.serverTotalMessages}}`);
                        }}

                        console.log(`Loaded ${{data.messages.length}} messages, total: ${{this.allMessages.length}}`);

                        // Update filtered messages if search is active
                        if (this.searchQuery) {{
                            this.filterMessages();
                        }} else {{
                            this.filteredMessages = [...this.allMessages];
                            this.renderMessages();
                        }}

                        this.updateSegments();
                        this.updateStats();
                    }} else {{
                        this.isEndOfFile = true;
                        console.log('End of file reached');
                    }}

                }} catch (error) {{
                    console.error('Error loading messages chunk:', error);
                    this.showError('Error carregant missatges. Assegura\\'t que el servidor està executant-se.');
                }} finally {{
                    this.isLoading = false;
                }}
            }}

            addLoadedSegment(start, end) {{
                // Add a new loaded segment and merge with existing overlapping segments
                // Add the new segment to the list
                this.loadedSegments.push({{ start, end }});
                
                // Sort segments by start position
                this.loadedSegments.sort((a, b) => a.start - b.start);
                
                // Merge all overlapping or adjacent segments
                const mergedSegments = [];
                let currentSegment = null;
                
                for (const segment of this.loadedSegments) {{
                    if (!currentSegment) {{
                        // First segment
                        currentSegment = {{ start: segment.start, end: segment.end }};
                    }} else if (segment.start <= currentSegment.end) {{
                        // Overlapping or adjacent - merge by extending the end
                        currentSegment.end = Math.max(currentSegment.end, segment.end);
                    }} else {{
                        // Gap found - save current segment and start a new one
                        mergedSegments.push(currentSegment);
                        currentSegment = {{ start: segment.start, end: segment.end }};
                    }}
                }}
                
                // Don't forget to add the last segment
                if (currentSegment) {{
                    mergedSegments.push(currentSegment);
                }}
                
                this.loadedSegments = mergedSegments;
                console.log('Loaded segments:', this.loadedSegments);
            }}

            updateSegments() {{
                // Update the loaded segments tracking
                // Note: We track segments based on message indices in the TOTAL chat
                // The allMessages array contains messages we've loaded, but they might not be continuous
                
                if (!this.serverTotalMessages || this.serverTotalMessages === 0) {{
                    return;
                }}

                // Render segments visualization
                this.renderSegments();
            }}

            renderSegments() {{
                if (!this.serverTotalMessages || this.serverTotalMessages === 0) {{
                    return;
                }}

                // Calculate number of segments to display (e.g., 100 segments for the whole chat)
                const numSegments = 100;
                const messagesPerSegment = Math.ceil(this.serverTotalMessages / numSegments);

                this.segmentIndicator.innerHTML = '';

                // Create segments
                for (let i = 0; i < numSegments; i++) {{
                    const segmentStart = i * messagesPerSegment;
                    const segmentEnd = Math.min((i + 1) * messagesPerSegment, this.serverTotalMessages);
                    
                    // Check if this segment is loaded
                    const isLoaded = this.isSegmentLoaded(segmentStart, segmentEnd);
                    
                    const segment = document.createElement('div');
                    segment.className = `segment ${{isLoaded ? 'loaded' : 'unloaded'}}`;
                    segment.style.flex = '1';
                    segment.title = `Messages ${{segmentStart}}-${{segmentEnd}}: ${{isLoaded ? 'Loaded' : 'Not loaded'}}`;
                    
                    this.segmentIndicator.appendChild(segment);
                }}
            }}

            isSegmentLoaded(segmentStart, segmentEnd) {{
                // Check if any messages in this segment range are loaded
                for (const segment of this.loadedSegments) {{
                    // Check if there's any overlap between the segment range and loaded range
                    if (segment.start < segmentEnd && segment.end > segmentStart) {{
                        return true;
                    }}
                }}
                return false;
            }}

            updateStats() {{
                const totalInfo = this.serverTotalMessages ? `${{this.totalMessages}}/${{this.serverTotalMessages}}` : `${{this.totalMessages}}`;
                this.stats.innerHTML = `
                    Missatges: ${{totalInfo}} |
                    Adjunts: ${{this.getTotalAttachments()}} |
                    Cerca: ${{this.searchQuery ? 'Activa' : 'Inactiva'}}
                `;
            }}

            getTotalAttachments() {{
                return this.allMessages.reduce((total, msg) => total + (msg.attachments ? msg.attachments.length : 0), 0);
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
                // Set flag to ignore scroll events triggered by this method
                this.isRendering = true;
                
                // Save current scroll position
                const currentScrollTop = this.messagesContainer.scrollTop;
                const currentScrollHeight = this.messagesContainer.scrollHeight;

                this.messagesContainer.innerHTML = '';

                if (this.filteredMessages.length === 0) {{
                    this.messagesContainer.innerHTML = '<div class="loading">No s\\'han trobat missatges.</div>';
                    this.isRendering = false; // Reset flag before early return
                    return;
                }}

                // Render only visible messages (virtual scrolling)
                const containerHeight = this.messagesContainer.clientHeight;
                const scrollTop = currentScrollTop;
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
                    const messageElement = this.createMessageElement(message, i);
                    this.messagesContainer.appendChild(messageElement);
                }}

                // Create bottom spacer
                const bottomSpacer = document.createElement('div');
                bottomSpacer.style.height = `${{(this.filteredMessages.length - endIndex) * itemHeight}}px`;
                this.messagesContainer.appendChild(bottomSpacer);

                // Restore loaded attachments after rendering
                this.restoreLoadedAttachments();

                // Restore scroll position
                this.messagesContainer.scrollTop = currentScrollTop;

                // Update last scroll height to prevent infinite loops
                this.lastScrollHeight = this.messagesContainer.scrollHeight;
                
                // Update time scrollbar after rendering
                if (this.firstTimestamp && this.lastTimestamp && !this.isScrollingFromTimeScrollbar) {{
                    this.updateTimeScrollbarFromMessages();
                }}
                
                // Clear flag - we're done rendering
                this.isRendering = false;
            }}

            createMessageElement(message, messageIndex) {{
                const messageDiv = document.createElement('div');
                messageDiv.className = `message${{message.is_system_message ? ' system' : ''}}`;

                const timestamp = new Date(message.timestamp).toLocaleString('ca-ES');

                let attachmentsHtml = '';
                if (message.attachments && message.attachments.length > 0) {{
                    attachmentsHtml = '<div class="attachments">';
                    message.attachments.forEach((attachment, attachmentIndex) => {{
                        attachmentsHtml += this.createAttachmentHtml(attachment, messageIndex, attachmentIndex);
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

            createAttachmentHtml(attachment, messageIndex, attachmentIndex) {{
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

                // Create stable attachment ID based on message index and attachment index
                const attachmentId = `attachment_${{messageIndex}}_${{attachmentIndex}}`;

                if (attachment.type === 'image') {{
                    return `
                        <div class="attachment">
                            <div class="attachment-placeholder" onclick="progressiveChat.loadAttachment('${{attachmentId}}', '${{attachment.name}}', 'image')">
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
                            <div class="attachment-placeholder" onclick="progressiveChat.loadAttachment('${{attachmentId}}', '${{attachment.name}}', 'video')">
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
                            <div class="attachment-placeholder" onclick="progressiveChat.loadAttachment('${{attachmentId}}', '${{attachment.name}}', 'audio')">
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
                                <a href="/api/attachment/${{attachment.name}}" class="download-link" target="_blank">Descarregar</a>
                            </div>
                        </div>
                    `;
                }}
            }}

            async loadAttachment(attachmentId, fileName, type) {{
                if (this.loadedAttachments.has(attachmentId)) {{
                    return;
                }}

                try {{
                    const response = await fetch(`/api/attachment/${{fileName}}`);
                    const blob = await response.blob();
                    const reader = new FileReader();

                    reader.onload = () => {{
                        const container = document.getElementById(attachmentId);
                        const placeholder = container?.previousElementSibling;

                        if (!container) {{
                            console.warn(`Container ${{attachmentId}} not found`);
                            return;
                        }}

                        let contentHtml = '';
                        if (type === 'image') {{
                            contentHtml = `<img src="${{reader.result}}" alt="Attachment" style="max-width: 100%; height: auto;" />`;
                        }} else if (type === 'video') {{
                            contentHtml = `<video controls style="max-width: 100%; height: auto;"><source src="${{reader.result}}" type="video/mp4">El teu navegador no suporta el tag de vídeo.</video>`;
                        }} else if (type === 'audio') {{
                            contentHtml = `<audio controls style="width: 100%;"><source src="${{reader.result}}" type="audio/mpeg">El teu navegador no suporta el tag d'àudio.</audio>`;
                        }}

                        container.innerHTML = contentHtml;
                        container.style.display = 'block';
                        if (placeholder) {{
                            placeholder.style.display = 'none';
                        }}

                        // Store both the flag and the actual content for restoration
                        this.loadedAttachments.set(attachmentId, true);
                        this.loadedAttachmentsContent.set(attachmentId, {{ content: contentHtml, type: type }});
                    }};

                    reader.readAsDataURL(blob);
                }} catch (error) {{
                    console.error('Error loading attachment:', error);
                    const container = document.getElementById(attachmentId);
                    if (container) {{
                        container.innerHTML = '<div class="error-message">Error carregant adjunt</div>';
                        container.style.display = 'block';
                    }}
                }}
            }}

            extractUrls(text) {{
                const urlPattern = /https?:\\/\\/[^\\s]+/g;
                return text.replace(urlPattern, '<a href="$&" class="url-link" target="_blank">$&</a>');
            }}

            restoreLoadedAttachments() {{
                // Restore loaded attachments after DOM is recreated
                this.loadedAttachmentsContent.forEach((data, attachmentId) => {{
                    const container = document.getElementById(attachmentId);
                    if (container) {{
                        // Restore the content
                        container.innerHTML = data.content;
                        container.style.display = 'block';

                        // Hide placeholder
                        const placeholder = container.previousElementSibling;
                        if (placeholder && placeholder.classList.contains('attachment-placeholder')) {{
                            placeholder.style.display = 'none';
                        }}
                    }}
                }});
            }}

            handleScroll() {{
                // Ignore scroll events triggered by renderMessages()
                if (this.isRendering) {{
                    return;
                }}
                
                this.showScrollIndicator();
                this.updateScrollInfo();

                // Update time-based scrollbar based on visible messages
                if (!this.isScrollingFromTimeScrollbar) {{
                    this.updateTimeScrollbarFromMessages();
                }}

                // Clear existing scroll timeout
                if (this.scrollTimeout) {{
                    clearTimeout(this.scrollTimeout);
                }}

                // Set new timeout to wait for scroll to end
                this.scrollTimeout = setTimeout(() => {{
                    this.onScrollEnd();
                }}, 300); // Wait 300ms after scroll stops

                // Re-render messages for virtual scrolling (throttled)
                if (!this.renderTimeout) {{
                    this.renderTimeout = setTimeout(() => {{
                        this.renderMessages();
                        this.renderTimeout = null;
                    }}, 200);
                }}
            }}

            onScrollEnd() {{
                // Load more messages when approaching bottom (only if not already loading)
                const container = this.messagesContainer;
                const scrollTop = container.scrollTop;
                const scrollHeight = container.scrollHeight;
                const clientHeight = container.clientHeight;

                // Only trigger load if:
                // 1. Not already loading
                // 2. Not at end of file
                // 3. Scroll position is at 80% or more
                // 4. Scroll height has not changed since last check (prevents load during rendering)
                if (!this.isLoading &&
                    !this.isEndOfFile &&
                    scrollTop + clientHeight >= scrollHeight * 0.8 &&
                    scrollHeight === this.lastScrollHeight) {{
                    console.log('Scroll ended, loading more messages...');
                    this.loadMessagesChunk();
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
                    Carregats: ${{loadedMessages}}<br>
                    Offset: ${{this.currentOffset}}
                `;
            }}

            showError(message) {{
                this.messagesContainer.innerHTML = `
                    <div class="error-message">${{message}}</div>
                    <div class="server-info">
                        <strong>Instruccions per executar el servidor:</strong><br>
                        1. Obre una terminal<br>
                        2. Navega al directori del projecte<br>
                        3. Executa: <code>python3 progressive_server.py</code><br>
                        4. Obre aquesta pàgina al navegador
                    </div>
                `;
            }}
        }}

        // Initialize progressive virtual chat when page loads
        let progressiveChat;
        document.addEventListener('DOMContentLoaded', () => {{
            progressiveChat = new ProgressiveVirtualChat();
        }});
    </script>
</body>
</html>'''

        return html_content
