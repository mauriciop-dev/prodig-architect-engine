from http.server import BaseHTTPRequestHandler
import json
import csv
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        csv_path = os.path.join(os.getcwd(), 'tech_stack_prodig.csv')
        tech_list = []
        
        try:
            if os.path.exists(csv_path):
                with open(csv_path, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        tech_list.append(row)
            else:
                # Fallback if file doesn't exist yet
                tech_list = [
                    {"Tecnología": "ProDig Engine", "Proveedor": "Internal", "Aplicación ProDig": "Core System"}
                ]

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(tech_list).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
