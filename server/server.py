# Standard Library Imports
import datetime
import hashlib
import json
import math
import os
import sys
import time
from pathlib import Path
import subprocess

# Third-Party Imports
import faiss
import numpy as np
import requests
from PIL import Image as PILImage
from tqdm import tqdm
from markitdown import MarkItDown

# MCP Package Imports
from mcp import types
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent

# Application specific imports
from models import RetrieveDocumentRequest

mcp = FastMCP("AI Browser Assistant")

EMBED_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"
CHUNK_SIZE = 256
CHUNK_OVERLAP = 40
ROOT = Path(__file__).parent.resolve()

def log(stage: str, msg: str):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [{stage}] {msg}")

def mcp_log(level: str, message: str) -> None:
    """Log a message to stderr to avoid interfering with JSON communication"""
    sys.stderr.write(f"{level}: {message}\n")
    sys.stderr.flush()

def get_embedding(text: str) -> np.ndarray:
    mcp_log("DEBUG", f"Requesting embedding for text (first 50 chars): {text[:50]}...")
    try:
        response = requests.post(EMBED_URL, json={"model": EMBED_MODEL, "prompt": text})
        response.raise_for_status()
        embedding = np.array(response.json()["embedding"], dtype=np.float32)
        mcp_log("DEBUG", f"Received embedding of length {len(embedding)}")
        return embedding
    except Exception as e:
        mcp_log("ERROR", f"Failed to get embedding: {e}")
        raise

@mcp.tool()
def retrieve_data(query: str):
    """
    Retrieve relevant document chunks from the FAISS vector database based on a user query.

    Args:
        query (str): A natural language query entered by the user.

    Returns:
        List[Dict] | List[str]: 
            - On success: A list of dictionaries, each containing a matched document chunk and metadata such as source and chunk ID.
            - On failure: A list with a single error string describing the issue.

    This function performs the following:
        1. Loads the FAISS index and associated metadata.
        2. Converts the query into a vector using `get_embedding`.
        3. Searches the FAISS index for the top-k most similar chunks.
        4. Returns the matched metadata.
    """
    mcp_log("SEARCH", f"Received query: {query}")

    try:
        mcp_log("INFO", "Loading FAISS index and metadata...")
        index_path = ROOT / "faiss_index" / "index.bin"
        metadata_path = ROOT / "faiss_index" / "metadata.json"
        
        index = faiss.read_index(str(index_path))
        metadata = json.loads(metadata_path.read_text())

        mcp_log("INFO", "Generating embedding for the query...")
        query_vec = get_embedding(query).reshape(1, -1)

        mcp_log("INFO", "Performing similarity search in FAISS index...")
        k = 2  # Number of top results to return
        distances, indices = index.search(query_vec, k)

        mcp_log("DEBUG", f"Search returned indices: {indices[0]}")
        results = []

        for idx in indices[0]:
            if idx < len(metadata):
                # mcp_log("+++++++++++++++++++++", "+++++++++++++++++++++")
                # mcp_log(f"Meta Data at {idx}", f"{metadata[idx]['url']}")
                # mcp_log("+++++++++++++++++++++", "+++++++++++++++++++++")
                results.append(metadata[idx]['url'])
            else:
                mcp_log("WARNING", f"Index {idx} is out of range in metadata")

        mcp_log("SUCCESS", f"Returning {len(results)} result(s)")
        return results

    except Exception as e:
        error_msg = f"ERROR: Failed to search: {str(e)}"
        mcp_log("ERROR", error_msg)
        return [error_msg]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run() # Run without transport for dev server
    else:
        # Start the server in a separate thread
        import threading
        server_thread = threading.Thread(target=lambda: mcp.run(transport="stdio"))
        server_thread.daemon = True
        server_thread.start()
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
