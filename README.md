# NavMind
A RAG (Retrieval-Augmented Generation) based application that tracks and retrieves browser history using semantic search capabilities.

## Overview

Browser Retriever is a sophisticated system that:
1. Captures and stores URLs visited in the browser
2. Implements a vector database (FAISS) for efficient semantic search
3. Provides a Chrome extension interface for user interaction
4. Automatically opens and highlights relevant URLs based on semantic search results

## Architecture

The application consists of two main components:

### 1. Server Component
- **app.py**: Flask server handling API requests and browser automation
- **memory.py**: FAISS-based vector storage and retrieval system
- **agent.py**: Core processing logic for handling user queries
- **perception.py**: URL capture and processing module
- **decision.py**: Decision-making logic for search results
- **action.py**: Browser automation actions

### 2. Chrome Extension
- **popup.html**: User interface for the extension
- **popup.js**: Client-side logic for extension functionality
- **manifest.json**: Extension configuration

## Features

- Real-time URL tracking and storage
- Semantic search capabilities using FAISS
- Automatic URL retrieval and highlighting
- Chrome extension integration
- Efficient vector-based storage and retrieval

## Installation

### Prerequisites
- Python 3.8+
- Chrome browser
- Ollama (for embeddings)

### Server Setup
1. Create a virtual environment:
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the server:
```bash
python server/app.py
```

### Chrome Extension Setup
1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" and select the `extension` directory

## Usage

1. Install and activate the Chrome extension
2. Click the extension icon to open the popup interface
3. Enter your search query
4. The system will automatically:
   - Search through stored URLs
   - Open the most relevant URL
   - Highlight the matching text

## Technical Details

### Vector Storage
- Uses FAISS for efficient similarity search
- Implements embeddings using Ollama's nomic-embed-text model
- Stores metadata including timestamps, tags, and session information

### Browser Integration
- Uses AppleScript for browser automation (macOS)
- Implements text highlighting using JavaScript injection
- Maintains session-based tracking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
