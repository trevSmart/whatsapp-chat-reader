#!/usr/bin/env python3
"""
Script per regenerar el document HTML amb lazy loading
"""

import sys
import os
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
    
    # Generar HTML
    generator = HTMLGenerator()
    html_content = generator.generate_html(messages, attachment_map, "Xat amb Lazy Loading")
    
    # Escriure el fitxer HTML
    with open("examples/regenerat_lazy_loading.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("Document HTML regenerat: examples/regenerat_lazy_loading.html")
    
    # Mostrar estadístiques
    total_attachments = sum(len(msg.attachments) for msg in messages)
    unique_senders = len(set(msg.sender for msg in messages))
    
    print()
    print("Estadístiques:")
    print(f"  - Missatges totals: {len(messages)}")
    print(f"  - Adjunts totals: {total_attachments}")
    print(f"  - Participants: {unique_senders}")
    print(f"  - Adjunts trobats: {len(attachment_map)}")

if __name__ == '__main__':
    main()
