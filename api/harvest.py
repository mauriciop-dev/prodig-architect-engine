from http.server import BaseHTTPRequestHandler
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Brave API requires a key
        api_key = os.environ.get('BRAVE_API_KEY')
        if not api_key:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'BRAVE_API_KEY not configured'}).encode())
            return

        # Simplified harvest logic: search for latest AI news from specific sources
        queries = ["Google Cloud AI news", "n8n AI automation updates", "Gemini AI latest features"]
        all_results = []

        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": api_key
        }

        for query in queries:
            try:
                response = requests.get(
                    f"https://api.search.brave.com/res/v1/web/search?q={query}",
                    headers=headers
                )
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('web', {}).get('results', [])[:2]
                    for r in results:
                        all_results.append({
                            'title': r.get('title'),
                            'url': r.get('url'),
                            'description': r.get('description')
                        })
            except Exception as e:
                print(f"Error searching for {query}: {e}")

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'results': all_results}).encode())
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
