from http.server import BaseHTTPRequestHandler
import json
import os
import csv
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        user_message = data.get('message', '')
        
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'GROQ_API_KEY not configured'}).encode())
            return

        client = Groq(api_key=api_key)
        
        # Cargar contexto de tecnologías desde el CSV (RAG Simple)
        tech_context = ""
        csv_path = os.path.join(os.getcwd(), 'tech_stack_prodig.csv')
        if os.path.exists(csv_path):
            with open(csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                tech_list = [f"- {row['Tecnología']} ({row['Proveedor']}): {row['Aplicación ProDig']}" for row in reader]
                tech_context = "\n".join(tech_list)

        system_prompt = f"""
        Eres el Arquitecto de Software Senior de ProDig. 
        Tu misión es diseñar soluciones de alto nivel combinando tecnologías de IA y automatización.
        
        Cuentas con el siguiente inventario de tecnologías preferidas (IA Tools):
        {tech_context}
        
        Cuando el usuario te plantee una idea:
        1. Analiza la viabilidad técnica.
        2. Utiliza preferiblemente las herramientas de tu inventario si aplican.
        3. Propón una arquitectura ideal paso a paso.
        4. Explica el porqué de cada decisión.
        
        Mantén un tono profesional, experto y consultivo. Responde en Español.
        """

        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=1500,
            )
            
            response_text = completion.choices[0].message.content

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'response': response_text}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
            
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
