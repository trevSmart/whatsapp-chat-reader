#!/usr/bin/env python3
"""
WhatsApp Chat Reader - Static Virtual Scrolling Version
Genera un document HTML amb virtual scrolling utilitzant fitxers JSON estàtics
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from whatsapp_chat_reader.parser import WhatsAppParser
from whatsapp_chat_reader.static_virtual_generator import StaticVirtualHTMLGenerator

def main():
    parser = argparse.ArgumentParser(
        description="WhatsApp Chat Reader - Static Virtual Scrolling Version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'ús:
  %(prog)s chat.txt --attachments ./adjunts --output chat.html
  %(prog)s chat.txt --output-directory ./chat_output
        """
    )

    parser.add_argument(
        'chat_file',
        help='Fitxer de xat de WhatsApp (.txt)'
    )

    parser.add_argument(
        '--attachments',
        help='Directori amb els adjunts del xat'
    )

    parser.add_argument(
        '--output',
        help='Fitxer HTML de sortida (per defecte: chat_virtual.html)'
    )

    parser.add_argument(
        '--output-directory',
        help='Directori de sortida per fitxers HTML i JSON (per defecte: directori actual)'
    )

    parser.add_argument(
        '--chat-name',
        default='WhatsApp Chat',
        help='Nom del xat per mostrar (per defecte: "WhatsApp Chat")'
    )

    parser.add_argument(
        '--chunk-size',
        type=int,
        default=100,
        help='Mida dels chunks de missatges (per defecte: 100)'
    )

    args = parser.parse_args()

    # Verificar que el fitxer de xat existeix
    if not os.path.exists(args.chat_file):
        print(f"Error: El fitxer de xat '{args.chat_file}' no existeix.")
        sys.exit(1)

    # Verificar que el directori d'adjunts existeix (si s'especifica)
    attachment_map = {}
    if args.attachments:
        if not os.path.exists(args.attachments):
            print(f"Error: El directori d'adjunts '{args.attachments}' no existeix.")
            sys.exit(1)

    # Configurar directori de sortida
    output_dir = args.output_directory or ""
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Configurar fitxer de sortida
    output_file = args.output or "chat_virtual.html"
    if output_dir:
        output_file = os.path.join(output_dir, output_file)

    print(f"Processant xat: {args.chat_file}")
    if args.attachments:
        print(f"Directori d'adjunts: {args.attachments}")
    print(f"Fitxer de sortida: {output_file}")
    if output_dir:
        print(f"Directori de sortida: {output_dir}")
    print(f"Nom del xat: {args.chat_name}")
    print(f"Mida dels chunks: {args.chunk_size}")
    print()

    # Parsejar missatges
    print("Parsejant missatges del xat...")
    parser_instance = WhatsAppParser()
    messages = parser_instance.parse_chat_file(args.chat_file)
    print(f"Trobats {len(messages)} missatges")

    # Trobar adjunts
    if args.attachments:
        print("Buscant adjunts...")
        attachment_map = parser_instance.find_attachment_files(messages, args.attachments)
        print(f"Trobats {len(attachment_map)} fitxers d'adjunts")

    # Estadístiques
    total_attachments = sum(len(msg.attachments) for msg in messages)
    unique_senders = len(set(msg.sender for msg in messages))

    print()
    print("Estadístiques:")
    print(f"  - Missatges totals: {len(messages)}")
    print(f"  - Adjunts totals: {total_attachments}")
    print(f"  - Participants: {unique_senders}")
    print(f"  - Adjunts trobats: {len(attachment_map)}")
    print()

    # Generar HTML amb virtual scrolling
    print("Generant document HTML amb virtual scrolling...")
    generator = StaticVirtualHTMLGenerator()

    # Modificar el chunk size si s'especifica
    if args.chunk_size != 100:
        generator.chunk_size = args.chunk_size

    html_content = generator.generate_html(messages, attachment_map, args.chat_name, output_dir)

    # Escriure fitxer HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Document HTML generat: {output_file}")

    if output_dir:
        chunk_files = [f for f in os.listdir(output_dir) if f.startswith('chunk_') and f.endswith('.json')]
        print(f"Fitxers JSON generats: {len(chunk_files)} chunks")
        print(f"Directori complet: {output_dir}")

    print()
    print("✅ Generació completada!")
    print(f"Obre {output_file} al teu navegador per veure el xat amb virtual scrolling.")

if __name__ == '__main__':
    main()
