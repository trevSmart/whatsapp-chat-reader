#!/usr/bin/env python3
"""
Test script for validating the progressive server with real example data.
This test validates the functionality with the large test dataset in tests/real-example-test/
"""

import unittest
import os
import sys
import time
import subprocess
import requests
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class TestRealExample(unittest.TestCase):
    """Test the progressive server with real example data."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment - start the server."""
        cls.test_dir = Path(__file__).parent / "real-example-test"
        cls.chat_file = cls.test_dir / "_chat.txt"
        cls.port = 8765  # Use different port to avoid conflicts
        cls.base_url = f"http://localhost:{cls.port}"
        
        # Verify test files exist
        if not cls.chat_file.exists():
            raise FileNotFoundError(f"Test chat file not found: {cls.chat_file}")
        
        if not cls.test_dir.exists():
            raise FileNotFoundError(f"Test directory not found: {cls.test_dir}")
        
        # Start the server
        cls.server_process = subprocess.Popen(
            [
                sys.executable,
                "progressive_server.py",
                str(cls.chat_file),
                "--attachments", str(cls.test_dir),
                "--chat-name", "Test Chat",
                "--port", str(cls.port),
                "--host", "127.0.0.1"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path(__file__).parent.parent
        )
        
        # Wait for server to start
        max_retries = 30
        for i in range(max_retries):
            try:
                response = requests.get(f"{cls.base_url}/api/stats", timeout=1)
                if response.status_code == 200:
                    print(f"✅ Server started successfully on port {cls.port}")
                    break
            except requests.exceptions.ConnectionError:
                time.sleep(1)
        else:
            cls.server_process.kill()
            raise RuntimeError("Server failed to start within timeout")
    
    @classmethod
    def tearDownClass(cls):
        """Stop the server."""
        if hasattr(cls, 'server_process'):
            cls.server_process.terminate()
            cls.server_process.wait(timeout=5)
            print("🛑 Server stopped")
    
    def test_chat_file_exists(self):
        """Test that the chat file exists and has content."""
        self.assertTrue(self.chat_file.exists(), "Chat file should exist")
        
        file_size = self.chat_file.stat().st_size
        self.assertGreater(file_size, 1024 * 1024, "Chat file should be > 1MB")
        
        with open(self.chat_file, 'r', encoding='utf-8') as f:
            lines = sum(1 for _ in f)
        
        self.assertGreater(lines, 10000, "Chat file should have > 10,000 lines")
        print(f"📊 Chat file: {file_size / (1024*1024):.1f} MB, {lines} lines")
    
    def test_attachments_directory(self):
        """Test that attachments directory exists and has files."""
        self.assertTrue(self.test_dir.exists(), "Attachments directory should exist")
        
        attachment_files = list(self.test_dir.glob("*"))
        # Exclude _chat.txt from count
        attachment_files = [f for f in attachment_files if f.name != "_chat.txt"]
        
        self.assertGreater(len(attachment_files), 100, "Should have > 100 attachment files")
        print(f"📎 Found {len(attachment_files)} attachment files")
    
    def test_api_stats(self):
        """Test the /api/stats endpoint."""
        response = requests.get(f"{self.base_url}/api/stats")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('file_size', data)
        self.assertIn('file_size_mb', data)
        self.assertIn('attachment_dir', data)
        
        self.assertGreater(data['file_size_mb'], 1.0, "File should be > 1 MB")
        print(f"📊 Stats: {data['file_size_mb']:.1f} MB")
    
    def test_api_messages_first_chunk(self):
        """Test getting the first chunk of messages."""
        response = requests.get(f"{self.base_url}/api/messages?offset=0&limit=50")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('messages', data)
        self.assertIn('has_more', data)
        self.assertIn('total_messages', data)
        
        self.assertEqual(len(data['messages']), 50, "Should return 50 messages")
        self.assertTrue(data['has_more'], "Should have more messages")
        self.assertGreater(data['total_messages'], 10000, "Should have > 10,000 total messages")
        
        print(f"💬 Total messages: {data['total_messages']}")
        print(f"📝 First chunk: {len(data['messages'])} messages")
    
    def test_api_messages_middle_chunk(self):
        """Test getting a chunk from the middle of the chat."""
        response = requests.get(f"{self.base_url}/api/messages?offset=1000&limit=100")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data['messages']), 100, "Should return 100 messages")
        self.assertTrue(data['has_more'], "Should have more messages")
        self.assertEqual(data['offset'], 1000, "Offset should be 1000")
    
    def test_api_messages_last_chunk(self):
        """Test getting the last chunk of messages."""
        # First get total count
        response = requests.get(f"{self.base_url}/api/messages?offset=0&limit=1")
        data = response.json()
        total = data['total_messages']
        
        # Get last chunk
        offset = max(0, total - 50)
        response = requests.get(f"{self.base_url}/api/messages?offset={offset}&limit=50")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertFalse(data['has_more'], "Last chunk should not have more messages")
    
    def test_message_structure(self):
        """Test that messages have the correct structure."""
        response = requests.get(f"{self.base_url}/api/messages?offset=0&limit=10")
        data = response.json()
        
        for message in data['messages']:
            self.assertIn('timestamp', message)
            self.assertIn('sender', message)
            self.assertIn('content', message)
            self.assertIn('is_system_message', message)
            self.assertIn('attachments', message)
            
            self.assertIsInstance(message['timestamp'], str)
            self.assertIsInstance(message['sender'], str)
            self.assertIsInstance(message['content'], str)
            self.assertIsInstance(message['is_system_message'], bool)
            self.assertIsInstance(message['attachments'], list)
    
    def test_message_with_attachments(self):
        """Test that messages with attachments are processed correctly."""
        # Get first chunk which should have messages with attachments
        response = requests.get(f"{self.base_url}/api/messages?offset=0&limit=100")
        data = response.json()
        
        messages_with_attachments = [m for m in data['messages'] if m['attachments']]
        self.assertGreater(len(messages_with_attachments), 0, "Should have messages with attachments")
        
        # Check first attachment structure
        first_msg_with_attachment = messages_with_attachments[0]
        attachment = first_msg_with_attachment['attachments'][0]
        
        self.assertIn('name', attachment)
        self.assertIn('type', attachment)
        self.assertIn('exists', attachment)
        self.assertIn('size', attachment)
        
        print(f"📎 Found {len(messages_with_attachments)} messages with attachments in first 100")
    
    def test_attachment_serving(self):
        """Test that attachments can be served."""
        # Get a message with an attachment
        response = requests.get(f"{self.base_url}/api/messages?offset=0&limit=100")
        data = response.json()
        
        messages_with_attachments = [m for m in data['messages'] 
                                     if m['attachments'] and m['attachments'][0]['exists']]
        
        if messages_with_attachments:
            attachment = messages_with_attachments[0]['attachments'][0]
            attachment_name = attachment['name']
            
            # Try to fetch the attachment
            response = requests.get(f"{self.base_url}/api/attachment/{attachment_name}")
            self.assertEqual(response.status_code, 200, f"Should serve attachment {attachment_name}")
            self.assertGreater(len(response.content), 0, "Attachment should have content")
            
            print(f"✅ Successfully served attachment: {attachment_name} ({len(response.content)} bytes)")
    
    def test_html_file_generated(self):
        """Test that the HTML file was generated."""
        html_file = Path(__file__).parent.parent / "chat_progressive.html"
        self.assertTrue(html_file.exists(), "HTML file should be generated")
        
        file_size = html_file.stat().st_size
        self.assertGreater(file_size, 1024, "HTML file should be > 1KB")
        print(f"📄 HTML file size: {file_size / 1024:.1f} KB")
    
    def test_root_endpoint(self):
        """Test that the root endpoint serves the HTML."""
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.headers.get('Content-Type', ''))
        self.assertIn('<!DOCTYPE html>', response.text)
        self.assertIn('Test Chat', response.text)
        print(f"✅ HTML served from root endpoint ({len(response.text)} bytes)")


if __name__ == '__main__':
    print("🧪 Testing WhatsApp Chat Reader with Real Example Data")
    print("=" * 70)
    print()
    
    # Run tests
    unittest.main(verbosity=2)
