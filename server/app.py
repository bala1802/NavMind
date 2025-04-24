from flask import Flask, request, jsonify
from flask_cors import CORS
import agent  # Import your existing agent.py
import subprocess
import ast
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/process', methods=['POST'])
def process_text():
    print("[INFO] Process Text in app.py initiated")
    data = request.json
    print(f"[`DEBUG] The data request received in `request` is {data}")
    text = data.get('text', '')
    print(f"[`DEBUG] The text present in the request is {text}")
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        # Call your agent's processing function
        # Modify this to match your agent.py's actual function
        result = agent.process_input(text)
        print(f"The Result in app.py is - {result}")
        print(f"Type of the Result in app.py is - {type(result)}")

        url = ast.literal_eval(result)[0]

        open_url_and_highlight_text(url=url, text_to_highlight=text)

        return jsonify({'response': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def open_url_and_highlight_text(url, text_to_highlight):
    print("[INFO] Opening the URL and Highlighting the text")
    print(f"[DEBUG] URL to be opened is {url} and the text to be highlighted is {text_to_highlight}")
    # JavaScript for highlighting the text — fixed version

    time.sleep(2)
    js = f"""
    var text = "{text_to_highlight}";
    function walk(node) {{
        if (node.nodeType === 3) {{
            var val = node.nodeValue;
            var idx = val.indexOf(text);
            if (idx > -1) {{
                var before = document.createTextNode(val.slice(0, idx));
                var after = document.createTextNode(val.slice(idx + text.length));
                var highlight = document.createElement("span");
                highlight.style.backgroundColor = "yellow";
                highlight.textContent = text;
                var parent = node.parentNode;
                parent.replaceChild(after, node);
                parent.insertBefore(highlight, after);
                parent.insertBefore(before, highlight);
                return true;
            }}
        }} else {{
            for (var i = 0; i < node.childNodes.length; i++) {{
                if (walk(node.childNodes[i])) return true;
            }}
        }}
        return false;
    }}
    walk(document.body);
    """
    # Escape for AppleScript
    js_escaped = js.replace('"', '\\"').replace('\n', '')

    applescript = f"""tell application "Google Chrome"
    if (count of windows) = 0 then
        make new window
    end if
    tell window 1
        set newTab to make new tab with properties {{URL:"{url}"}}
        set active tab index to (count of tabs)
    end tell
    delay 2
    tell active tab of window 1
        execute javascript "{js_escaped}"
    end tell
    activate
end tell"""

    subprocess.run(["osascript", "-e", applescript])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
