import os
import requests
import feedparser
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

FEED_URL = "https://docs.cloud.google.com/feeds/bigquery-release-notes.xml"

def fetch_and_parse_feed():
    try:
        response = requests.get(FEED_URL, timeout=15)
        response.raise_for_status()
        
        # Parse XML using feedparser
        feed = feedparser.parse(response.content)
        
        updates = []
        
        for entry_idx, entry in enumerate(feed.entries):
            date_str = entry.title  # e.g., "June 17, 2026"
            link = entry.link
            updated_iso = entry.updated if hasattr(entry, 'updated') else ""
            
            # The HTML content is usually in entry.content[0].value or entry.summary
            html_content = ""
            if hasattr(entry, 'content') and len(entry.content) > 0:
                html_content = entry.content[0].value
            elif hasattr(entry, 'summary'):
                html_content = entry.summary
                
            if not html_content:
                continue
                
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Split the HTML content by h3 headers to separate individual updates
            current_type = "Feature"
            current_elements = []
            
            # Helper to create an update item
            def add_update_item(elements, utype, idx):
                if not elements:
                    return
                content_html = "".join(str(el) for el in elements)
                # Parse content html again to clean and extract plain text for tweeting
                item_soup = BeautifulSoup(content_html, 'html.parser')
                plain_text = item_soup.get_text().strip()
                
                # Make a safe ID for UI selection and anchoring
                safe_date_id = date_str.lower().replace(',', '').replace(' ', '_')
                item_id = f"note_{entry_idx}_{idx}"
                
                # Try to extract the first paragraph for short tweets
                p_tag = item_soup.find('p')
                short_text = p_tag.get_text().strip() if p_tag else plain_text
                if len(short_text) > 180:
                    short_text = short_text[:177] + "..."
                
                updates.append({
                    "id": item_id,
                    "date": date_str,
                    "iso_date": updated_iso,
                    "type": utype,
                    "content": content_html,
                    "text": plain_text,
                    "short_text": short_text,
                    "link": f"{link}#{safe_date_id}"
                })

            sub_idx = 0
            for child in soup.children:
                if child.name == 'h3':
                    # Save the accumulated elements for the previous header
                    if current_elements:
                        add_update_item(current_elements, current_type, sub_idx)
                        sub_idx += 1
                        current_elements = []
                    current_type = child.get_text().strip()
                else:
                    if str(child).strip():
                        current_elements.append(child)
                        
            # Save the last accumulated block
            if current_elements:
                add_update_item(current_elements, current_type, sub_idx)
                
        return updates, None
    except Exception as e:
        return [], str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/notes')
def get_notes():
    updates, error = fetch_and_parse_feed()
    if error:
        return jsonify({"success": False, "error": error}), 500
    return jsonify({"success": True, "updates": updates})

if __name__ == '__main__':
    # Use port 5000 as default or read from environment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
