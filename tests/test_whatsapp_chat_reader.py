"""
Tests per WhatsApp Chat Reader
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from whatsapp_chat_reader import WhatsAppParser, HTMLGenerator, WhatsAppMessage
from datetime import datetime

class TestWhatsAppParser(unittest.TestCase):

    def setUp(self):
        self.parser = WhatsAppParser()

    def test_parse_simple_message(self):
        """Test parsing a simple message"""
        chat_content = "[8/5/21 16:39:00] Marc: Hola, com estàs?"

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(chat_content)
            temp_file = f.name

        try:
            messages = self.parser.parse_chat_file(temp_file)
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].sender, "Marc")
            self.assertEqual(messages[0].content, "Hola, com estàs?")
            self.assertEqual(len(messages[0].attachments), 0)
        finally:
            os.unlink(temp_file)

    def test_parse_message_with_attachment(self):
        """Test parsing a message with attachment"""
        chat_content = """[8/5/21 16:38:19] Marc: Mira aquesta foto
‎[8/5/21 16:38:19] Marc: ‎<adjunt: foto.jpg>"""

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(chat_content)
            temp_file = f.name

        try:
            messages = self.parser.parse_chat_file(temp_file)
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].sender, "Marc")
            self.assertEqual(messages[0].content, "Mira aquesta foto")
            self.assertEqual(len(messages[0].attachments), 1)
            self.assertEqual(messages[0].attachments[0], "foto.jpg")
        finally:
            os.unlink(temp_file)

    def test_parse_multiple_messages(self):
        """Test parsing multiple messages"""
        chat_content = """[8/5/21 16:38:19] Marc: Primer missatge
[8/5/21 16:39:00] Noemí: Segon missatge
[8/5/21 16:40:00] Marc: Tercer missatge"""

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(chat_content)
            temp_file = f.name

        try:
            messages = self.parser.parse_chat_file(temp_file)
            self.assertEqual(len(messages), 3)
            self.assertEqual(messages[0].sender, "Marc")
            self.assertEqual(messages[1].sender, "Noemí")
            self.assertEqual(messages[2].sender, "Marc")
        finally:
            os.unlink(temp_file)

class TestHTMLGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = HTMLGenerator()

    def test_generate_html_basic(self):
        """Test basic HTML generation"""
        messages = [
            WhatsAppMessage(
                timestamp=datetime(2021, 5, 8, 16, 39, 0),
                sender="Marc",
                content="Hola, com estàs?",
                attachments=[]
            )
        ]

        html = self.generator.generate_html(messages, {}, "Test Chat")

        self.assertIn("Test Chat", html)
        self.assertIn("Marc", html)
        self.assertIn("Hola, com estàs?", html)
        self.assertIn("<!DOCTYPE html>", html)

    def test_extract_urls(self):
        """Test URL extraction"""
        text = "Mira aquest enllaç: https://example.com i aquest altre: http://test.com"
        result = self.generator.extract_urls(text)

        self.assertIn('<a href="https://example.com"', result)
        self.assertIn('<a href="http://test.com"', result)

if __name__ == '__main__':
    unittest.main()
