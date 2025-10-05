#!/usr/bin/env python3
"""
WhatsApp Chat Reader - Hybrid Virtual Scrolling Version
Genera un fitxer HTML únic amb càrrega progressiva sense CORS.
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from whatsapp_chat_reader.parser import WhatsAppParser
from whatsapp_chat_reader.hybrid_virtual_generator import HybridVirtualHTMLGenerator

def main():
    parser = argparse.ArgumentParser(
        description="WhatsApp Chat Reader - Hybrid Virtual Scrolling Version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'ús:
  python hybrid_virtual_chat.py chat.txt
  python hybrid_virtual_chat.py chat.txt --attachments ./adjunts --chat-name "El meu xat"
  python hybrid_virtual_chat.py chat.txt --output ./output.html --chunk-size 50
        """
    )

    parser.add_argument(
        "chat_file",
        help="Ruta al fitxer de xat de WhatsApp (.txt)"
    )

    parser.add_argument(
        "--attachments",
        help="Directori on es troben els adjunts (opcional)"
    )

    parser.add_argument(
        "--output",
        help="Fitxer de sortida HTML (per defecte: chat_hybrid.html)"
    )

    parser.add_argument(
        "--chat-name",
        help="Nom del xat per mostrar al capçalera (per defecte: 'WhatsApp Chat')"
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=100,
        help="Mida dels chunks de missatges (per defecte: 100)"
    )

    args = parser.parse_args()

    # Validate chat file
    if not os.path.exists(args.chat_file):
        print(f"Error: El fitxer de xat '{args.chat_file}' no existeix.")
        sys.exit(1)

    # Set default output file
    if not args.output:
        chat_file_path = Path(args.chat_file)
        args.output = chat_file_path.parent / "chat_hybrid.html"

    # Set default chat name
    if not args.chat_name:
        args.chat_name = "WhatsApp Chat"

    print("🚀 Iniciant WhatsApp Chat Reader - Versió Híbrida")
    print(f"📁 Fitxer de xat: {args.chat_file}")
    print(f"📎 Adjunts: {args.attachments if args.attachments else 'No especificat'}")
    print(f"📄 Sortida: {args.output}")
    print(f"💬 Nom del xat: {args.chat_name}")
    print(f"📦 Mida dels chunks: {args.chunk_size}")
    print()

    try:
        # Parse chat file
        print("📖 Parsejant fitxer de xat...")
        parser = WhatsAppParser()
        messages = parser.parse_chat_file(args.chat_file)
        print(f"✅ Parsejats {len(messages)} missatges")

        # Find attachments if directory provided
        attachment_map = {}
        if args.attachments and os.path.exists(args.attachments):
            print("🔍 Buscant adjunts...")
            attachment_map = parser.find_attachment_files(messages, args.attachments)
            print(f"✅ Trobats {len(attachment_map)} adjunts")
        else:
            print("⚠️  No s'han especificat adjunts o el directori no existeix")

        # Calculate chunks info
        total_chunks = (len(messages) + args.chunk_size - 1) // args.chunk_size
        print(f"📦 Es generaran {total_chunks} chunks de {args.chunk_size} missatges")

        # Generate HTML
        print("🎨 Generant HTML híbrid...")
        generator = HybridVirtualHTMLGenerator()
        html_content = generator.generate_html(messages, attachment_map, args.chat_name)

        # Write output file
        print("💾 Escrivint fitxer de sortida...")
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Get file size
        file_size = os.path.getsize(args.output)
        file_size_mb = file_size / (1024 * 1024)

        print()
        print("🎉 Generació completada!")
        print(f"📄 Fitxer generat: {args.output}")
        print(f"📊 Mida del fitxer: {file_size_mb:.1f} MB")
        print()
        print("📊 Estadístiques:")
        print(f"   • Total missatges: {len(messages)}")
        print(f"   • Total adjunts: {sum(len(msg.attachments) for msg in messages)}")
        print(f"   • Adjunts trobats: {len(attachment_map)}")
        print(f"   • Participants únics: {len(set(msg.sender for msg in messages))}")
        print(f"   • Chunks generats: {total_chunks}")
        print()
        print("🌐 Per visualitzar el xat:")
        print(f"   Obre el fitxer '{args.output}' al teu navegador")
        print()
        print("✨ Característiques:")
        print("   • Càrrega progressiva per chunks")
        print("   • Virtual scrolling per rendiment òptim")
        print("   • Cerca en temps real")
        print("   • Adjunts integrats (imatges, vídeos, àudios)")
        print("   • Sense dependències externes ni CORS")
        print("   • Compatible amb tots els navegadors moderns")
        print("   • Barra de progrés de càrrega")

    except Exception as e:
        print(f"❌ Error durant la generació: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
