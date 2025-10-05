#!/bin/bash
# Script to test the progressive server with the real example

set -e

echo "🧪 Testing WhatsApp Chat Reader with Real Example"
echo "=================================================="
echo ""

# Check if test data exists
if [ ! -f "tests/real-example-test/_chat.txt" ]; then
    echo "❌ Error: Test data not found at tests/real-example-test/_chat.txt"
    exit 1
fi

echo "✅ Test data found"
echo ""

# Check dependencies
echo "📦 Checking dependencies..."
python3 -c "import flask" 2>/dev/null || {
    echo "❌ Flask not installed. Installing..."
    pip install flask flask-cors
}
python3 -c "import flask_cors" 2>/dev/null || {
    echo "❌ Flask-CORS not installed. Installing..."
    pip install flask-cors
}
echo "✅ Dependencies installed"
echo ""

# Get file stats
FILE_SIZE=$(du -h tests/real-example-test/_chat.txt | cut -f1)
LINE_COUNT=$(wc -l < tests/real-example-test/_chat.txt)
ATTACHMENT_COUNT=$(ls tests/real-example-test/ | grep -v "_chat.txt" | wc -l)

echo "📊 Test Data Statistics:"
echo "   - Chat file size: $FILE_SIZE"
echo "   - Total lines: $LINE_COUNT"
echo "   - Attachment files: $ATTACHMENT_COUNT"
echo ""

# Ask user what to do
echo "What would you like to do?"
echo "  1) Run automated tests"
echo "  2) Start server and browse manually"
echo "  3) Both (run tests then start server)"
echo ""
read -p "Choice (1/2/3): " choice

case $choice in
    1|3)
        echo ""
        echo "🧪 Running automated tests..."
        echo ""
        python3 -m pytest tests/test_real_example.py -v
        echo ""
        echo "✅ All tests passed!"
        
        if [ "$choice" != "3" ]; then
            exit 0
        fi
        echo ""
        ;;
    2)
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

# Start server
PORT=8080
echo "🚀 Starting server on port $PORT..."
echo ""
echo "   URL: http://localhost:$PORT"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""

python3 progressive_server.py \
    "tests/real-example-test/_chat.txt" \
    --attachments "tests/real-example-test" \
    --chat-name "Real Example Test Chat" \
    --port $PORT \
    --host 127.0.0.1
