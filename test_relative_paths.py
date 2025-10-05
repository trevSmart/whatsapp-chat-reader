#!/usr/bin/env python3
"""
Script per provar la generació HTML amb rutes relatives
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from whatsapp_chat_reader import WhatsAppParser, HTMLGenerator

def main():
    # Parsejar el xat
    parser = WhatsAppParser()
    messages = parser.parse_chat_file("examples/exemple_chat.txt")
    print(f"Trobats {len(messages)} missatges")

    # Trobar els adjunts
    attachment_map = parser.find_attachment_files(messages, "tmp")
    print(f"Trobats {len(attachment_map)} fitxers d'adjunts")

    # Generar HTML al mateix directori que el xat
    output_file = Path("examples/exemple_chat.html")
    attachments_dir = Path("tmp")

    # Calcular ruta relativa des del HTML fins als adjunts
    try:
        relative_attachment_dir = os.path.relpath(attachments_dir, output_file.parent)
        print(f"Ruta relativa als adjunts: {relative_attachment_dir}")
    except ValueError:
        relative_attachment_dir = str(attachments_dir)

    # Generar HTML
    generator = HTMLGenerator()
    html_content = generator.generate_html(messages, attachment_map, "Xat amb Rutes Relatives", relative_attachment_dir)

    # Escriure el fitxer HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Document HTML generat: {output_file}")
    print("Les imatges ara utilitzen rutes relatives correctes!")

if __name__ == '__main__':
    main()
