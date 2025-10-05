#!/usr/bin/env python3
"""
WhatsApp Chat Reader
Processa xats exportats de WhatsApp i genera un document HTML amb els adjunts integrats.
"""

import os
import sys
import argparse
from pathlib import Path
from whatsapp_chat_reader import WhatsAppParser, HTMLGenerator

def main():
    parser = argparse.ArgumentParser(
        description='Processa xats exportats de WhatsApp i genera un document HTML amb adjunts integrats.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'ús:
  python whatsapp_chat_reader.py chat.txt
  python whatsapp_chat_reader.py chat.txt --output chat.html
  python whatsapp_chat_reader.py chat.txt --attachments-dir ./attachments
  python whatsapp_chat_reader.py chat.txt --chat-name "Xat amb Noemí"
        """
    )

    parser.add_argument('chat_file', help='Fitxer del xat exportat de WhatsApp')
    parser.add_argument('--output', '-o', help='Fitxer HTML de sortida (per defecte: nom del xat + .html)')
    parser.add_argument('--attachments-dir', '-a', help='Directori amb els adjunts (per defecte: mateix directori que el xat)')
    parser.add_argument('--chat-name', '-n', help='Nom del xat per mostrar al document HTML')
    parser.add_argument('--open', help='Obrir el document HTML generat al navegador', action='store_true')

    args = parser.parse_args()

    # Verificar que el fitxer del xat existeix
    chat_file_path = Path(args.chat_file)
    if not chat_file_path.exists():
        print(f"Error: El fitxer '{chat_file_path}' no existeix.")
        sys.exit(1)

    # Determinar el directori dels adjunts
    if args.attachments_dir:
        attachments_dir = Path(args.attachments_dir)
    else:
        attachments_dir = chat_file_path.parent

    if not attachments_dir.exists():
        print(f"Error: El directori d'adjunts '{attachments_dir}' no existeix.")
        sys.exit(1)

    # Determinar el nom del fitxer de sortida
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = chat_file_path.with_suffix('.html')

    # Determinar el nom del xat
    if args.chat_name:
        chat_name = args.chat_name
    else:
        chat_name = chat_file_path.stem.replace('_', ' ').title()

    print(f"Processant xat: {chat_file_path}")
    print(f"Directori d'adjunts: {attachments_dir}")
    print(f"Fitxer de sortida: {output_file}")
    print(f"Nom del xat: {chat_name}")
    print()

    try:
        # Parsejar el xat
        print("Parsejant missatges del xat...")
        whatsapp_parser = WhatsAppParser()
        messages = whatsapp_parser.parse_chat_file(str(chat_file_path))
        print(f"Trobats {len(messages)} missatges")

        # Trobar els adjunts
        print("Buscant adjunts...")
        attachment_map = whatsapp_parser.find_attachment_files(messages, str(attachments_dir))
        print(f"Trobats {len(attachment_map)} fitxers d'adjunts")

        # Generar HTML
        print("Generant document HTML...")
        html_generator = HTMLGenerator()

        # Calcular ruta relativa des del HTML fins als adjunts
        try:
            relative_attachment_dir = os.path.relpath(attachments_dir, output_file.parent)
        except ValueError:
            # Si no es pot calcular ruta relativa, utilitzar ruta absoluta
            relative_attachment_dir = str(attachments_dir)

        html_content = html_generator.generate_html(messages, attachment_map, chat_name, relative_attachment_dir)

        # Escriure el fitxer HTML
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Document HTML generat: {output_file}")

        # Obrir al navegador si s'ha demanat
        if args.open:
            import webbrowser
            webbrowser.open(f'file://{output_file.absolute()}')
            print("Document obert al navegador")

        # Mostrar estadístiques
        total_attachments = sum(len(msg.attachments) for msg in messages)
        unique_senders = len(set(msg.sender for msg in messages))

        print()
        print("Estadístiques:")
        print(f"  - Missatges totals: {len(messages)}")
        print(f"  - Adjunts totals: {total_attachments}")
        print(f"  - Participants: {unique_senders}")
        print(f"  - Adjunts trobats: {len(attachment_map)}")

        if len(attachment_map) < total_attachments:
            missing = total_attachments - len(attachment_map)
            print(f"  - Adjunts no trobats: {missing}")
            print("    (Alguns adjunts poden no estar disponibles)")

    except Exception as e:
        print(f"Error processant el xat: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
