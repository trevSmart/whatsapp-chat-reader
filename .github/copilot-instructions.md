# GitHub Copilot Instructions for WhatsApp Chat Reader

## Project Overview

WhatsApp Chat Reader is a Python-based web application that processes exported WhatsApp chat files and generates interactive HTML visualizations with virtual scrolling and lazy loading for efficient handling of large chat histories (tens of thousands of messages).

### Key Technologies
- **Backend**: Python 3.8+, Flask, Flask-CORS
- **Frontend**: Vanilla JavaScript with virtual scrolling
- **Parser**: Custom WhatsApp TXT format parser

## Architecture

### Core Components
1. **Progressive Server** (`progressive_server.py`): Flask REST API serving message chunks
2. **Parser** (`src/whatsapp_chat_reader/parser.py`): Parses WhatsApp exported TXT files
3. **HTML Generator** (`src/whatsapp_chat_reader/progressive_virtual_generator.py`): Creates dynamic HTML with embedded JavaScript for virtual scrolling

### Data Flow
1. User exports WhatsApp chat → TXT file + attachments folder
2. Server reads TXT file progressively (not all at once)
3. API serves messages in chunks (default: 50 messages per request)
4. Frontend implements virtual scrolling (only renders visible messages)
5. Lazy loading for attachments (loaded on click)

## Development Guidelines

### Code Style
- Language: Catalan for user-facing strings, English for code/comments
- Python: Follow PEP 8, use type hints where possible
- JavaScript: ES6+ syntax, clear variable names
- Keep functions focused and small

### Testing Requirements
- **Test file**: Located in `tests/real-example-test/` with 3,400+ attachments and 25,835 messages
- **Run tests**: `make test-real` or `python -m pytest tests/test_real_example.py -v`
- **Manual server test**: `make test-server` to start server with test data
- Always test with large datasets to validate virtual scrolling and performance

### Build & Run
```bash
# Install in development mode
pip install -e .

# Run basic generator
whatsapp-chat-reader chat.txt

# Run progressive server (recommended for large chats)
python3 progressive_server.py chat.txt --attachments ./adjunts --chat-name "Chat Name" --port 8080

# Run all tests
make test

# Run with real example
make test-server
```

### Key Files
- `progressive_server.py`: Main server entry point
- `src/whatsapp_chat_reader/parser.py`: WhatsApp TXT parser (handles dates, attachments, system messages)
- `src/whatsapp_chat_reader/progressive_virtual_generator.py`: HTML/JS generator with virtual scrolling
- `AGENTS.md`: Comprehensive technical documentation (read this for deep dives)
- `TEST_RESULTS.md`: Test validation checklist

## Common Patterns

### Virtual Scrolling Implementation
- Uses debounce (300ms) to avoid excessive API calls during scroll
- Preserves scroll position during re-renders
- Maintains loaded attachment state across renders
- Renders only visible messages + buffer (10 before, 20 after)

### API Endpoints
- `GET /api/messages?offset=0&limit=50`: Get message chunk
- `GET /api/attachment/<filename>`: Serve attachment file
- `GET /api/stats`: Server statistics

### Parser Format
WhatsApp exports use format: `dd/mm/yy, HH:MM - Sender: Message`
- Supports multiline messages
- Detects attachments: `<omitido: image.jpg>`, `<attached: file.pdf>`
- System messages: Lines without sender info

## Common Pitfalls

1. **Memory Issues**: Don't load entire chat file at once - use chunked reading
2. **Scroll Performance**: Always implement debounce on scroll events
3. **Attachment Paths**: Match exact filenames from WhatsApp export (case-sensitive)
4. **Date Formats**: Support both `dd/mm/yy` and `dd/mm/yyyy` formats
5. **Encoding**: Try UTF-8 first, fallback to latin-1 if needed
6. **Virtual Scrolling State**: Always preserve loaded attachments state during re-render

## Testing Strategy

1. **Unit Tests**: Test parser with various message formats
2. **Integration Tests**: Test API endpoints with real data
3. **Performance Tests**: Use `tests/real-example-test/` with 25K+ messages
4. **Manual Testing**: Start server and verify UI functionality

## Contributing

- Keep changes minimal and focused
- Test with the real example dataset before submitting
- Update documentation if architecture changes
- Maintain backward compatibility with existing WhatsApp export formats

## Performance Benchmarks

- File size reduction: 831 MB → 4.7 MB (177x reduction)
- API requests: 90% reduction via debounce
- Memory: Only visible messages in DOM
- Supports: 25,000+ messages with smooth scrolling
