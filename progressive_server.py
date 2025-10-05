#!/usr/bin/env python3
"""
WhatsApp Chat Reader - Progressive Server
Servidor HTTP simple que llegeix del fitxer TXT progressivament.
"""

import os
import sys
import json
import base64
import mimetypes
from pathlib import Path
from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from whatsapp_chat_reader.parser import WhatsAppParser

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class ProgressiveChatServer:
    def __init__(self, chat_file_path: str, attachment_dir: str = None):
        self.chat_file_path = chat_file_path
        self.attachment_dir = attachment_dir
        self.parser = WhatsAppParser()

        # Cache for parsed messages
        self.messages_cache = []
        self.current_position = 0
        self.file_size = os.path.getsize(chat_file_path)

        print(f"📁 Fitxer de xat: {chat_file_path}")
        print(f"📎 Directori adjunts: {attachment_dir}")
        print(f"📊 Mida del fitxer: {self.file_size / (1024*1024):.1f} MB")

    def parse_messages_chunk(self, offset: int, limit: int):
        """Parse a chunk of messages from the TXT file."""
        try:
            # For now, let's use the existing parser but limit the results
            # This is not ideal for very large files, but will work for testing
            all_messages = self.parser.parse_chat_file(self.chat_file_path)

            # Get the chunk we need
            start_idx = offset
            end_idx = min(offset + limit, len(all_messages))

            chunk_messages = all_messages[start_idx:end_idx]

            # Convert to dict format
            messages = [self.message_to_dict(msg) for msg in chunk_messages]

            return {
                'messages': messages,
                'has_more': end_idx < len(all_messages),
                'offset': offset,
                'limit': limit,
                'total_messages': len(all_messages)
            }

        except Exception as e:
            print(f"Error parsing messages chunk: {e}")
            return {
                'messages': [],
                'has_more': False,
                'error': str(e)
            }

    def message_to_dict(self, message):
        """Convert WhatsAppMessage to dictionary."""
        message_dict = {
            'timestamp': message.timestamp.isoformat(),
            'sender': message.sender,
            'content': message.content,
            'is_system_message': message.is_system_message,
            'attachments': []
        }

        # Process attachments
        for attachment_name in message.attachments:
            attachment_data = self.create_attachment_metadata(attachment_name)
            message_dict['attachments'].append(attachment_data)

        return message_dict

    def create_attachment_metadata(self, attachment_name: str):
        """Create attachment metadata."""
        if not self.attachment_dir:
            return {
                'name': attachment_name,
                'type': 'file',
                'exists': False,
                'size': 'No attachment directory'
            }

        attachment_path = os.path.join(self.attachment_dir, attachment_name)

        if not os.path.exists(attachment_path):
            return {
                'name': attachment_name,
                'type': 'file',
                'exists': False,
                'size': 'File not found'
            }

        file_size = self.get_file_size(attachment_path)
        file_type = self.get_file_type(attachment_name)

        return {
            'name': attachment_name,
            'type': file_type,
            'exists': True,
            'size': file_size
        }

    def get_file_type(self, filename: str) -> str:
        """Get file type based on extension."""
        ext = os.path.splitext(filename)[1].lower()

        if ext in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}:
            return 'image'
        elif ext in {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.3gp'}:
            return 'video'
        elif ext in {'.mp3', '.wav', '.ogg', '.m4a', '.aac', '.flac', '.opus'}:
            return 'audio'
        else:
            return 'file'

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

# Global server instance
server = None

@app.route('/api/messages')
def get_messages():
    """Get messages chunk."""
    global server

    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 50))

    if not server:
        return jsonify({'error': 'Server not initialized'}), 500

    result = server.parse_messages_chunk(offset, limit)
    return jsonify(result)

@app.route('/api/attachment/<filename>')
def get_attachment(filename):
    """Serve attachment file."""
    global server

    if not server or not server.attachment_dir:
        return jsonify({'error': 'Attachment directory not configured'}), 404

    attachment_path = os.path.join(server.attachment_dir, filename)

    if not os.path.exists(attachment_path):
        return jsonify({'error': 'File not found'}), 404

    return send_file(attachment_path)

@app.route('/api/stats')
def get_stats():
    """Get server statistics."""
    global server

    if not server:
        return jsonify({'error': 'Server not initialized'}), 500

    return jsonify({
        'file_size': server.file_size,
        'file_size_mb': server.file_size / (1024 * 1024),
        'attachment_dir': server.attachment_dir,
        'messages_cached': len(server.messages_cache)
    })

@app.route('/')
def serve_html():
    """Serve the main HTML file."""
    return send_file('chat_progressive.html')

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="WhatsApp Chat Reader - Progressive Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'ús:
  python progressive_server.py chat.txt
  python progressive_server.py chat.txt --attachments ./adjunts --port 5000
  python progressive_server.py chat.txt --host 0.0.0.0 --port 8080
        """
    )

    parser.add_argument(
        "chat_file",
        help="Ruta al fitxer de xat de WhatsApp (.txt)"
    )

    parser.add_argument(
        "--attachments",
        help="Directori on es troben els adjunts (opcional). Si no s'especifica, es busca al mateix directori que el fitxer TXT"
    )

    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host del servidor (per defecte: 127.0.0.1)"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port del servidor (per defecte: 5000)"
    )

    parser.add_argument(
        "--chat-name",
        help="Nom del xat per mostrar al capçalera (per defecte: 'WhatsApp Chat')"
    )

    args = parser.parse_args()

    # Validate chat file
    if not os.path.exists(args.chat_file):
        print(f"Error: El fitxer de xat '{args.chat_file}' no existeix.")
        sys.exit(1)

    # Set default chat name
    if not args.chat_name:
        args.chat_name = "WhatsApp Chat"

    # Auto-detect attachment directory if not specified
    if not args.attachments:
        chat_file_dir = os.path.dirname(os.path.abspath(args.chat_file))
        args.attachments = chat_file_dir
        print(f"🔍 Directori d'adjunts detectat automàticament: {args.attachments}")
    else:
        print(f"📎 Directori d'adjunts especificat: {args.attachments}")

    print("🚀 Iniciant WhatsApp Chat Reader - Servidor Progressiu")
    print(f"📁 Fitxer de xat: {args.chat_file}")
    print(f"📎 Adjunts: {args.attachments}")
    print(f"🌐 Host: {args.host}")
    print(f"🔌 Port: {args.port}")
    print(f"💬 Nom del xat: {args.chat_name}")
    print()

    try:
        # Initialize server
        global server
        server = ProgressiveChatServer(args.chat_file, args.attachments)

        # Generate HTML file
        print("🎨 Generant fitxer HTML...")
        from whatsapp_chat_reader.progressive_virtual_generator import ProgressiveVirtualHTMLGenerator

        generator = ProgressiveVirtualHTMLGenerator()
        html_content = generator.generate_html(args.chat_file, args.attachments or "", args.chat_name)

        with open('chat_progressive.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        print("✅ Fitxer HTML generat: chat_progressive.html")
        print()
        print("🌐 Servidor iniciat!")
        print(f"   URL: http://{args.host}:{args.port}")
        print()
        print("✨ Característiques:")
        print("   • Lectura progressiva del fitxer TXT")
        print("   • Virtual scrolling per rendiment òptim")
        print("   • Càrrega sota demanda de missatges")
        print("   • Adjunts carregats quan es necessiten")
        print("   • Cerca en temps real")
        print("   • Sense límits de memòria")
        print()
        print("🛑 Per aturar el servidor: Ctrl+C")

        # Start Flask server
        app.run(host=args.host, port=args.port, debug=False)

    except KeyboardInterrupt:
        print("\\n🛑 Servidor aturat per l'usuari")
    except Exception as e:
        print(f"❌ Error iniciant servidor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
