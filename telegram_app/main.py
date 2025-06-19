import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import asyncio
from notifier import main as bot_main

# Função para manter o Railway "acordado"
def manter_vivo():
    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Bot esta rodando com sucesso no Railway.')

    server = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
    print("🌐 Servidor HTTP de keep-alive iniciado na porta 8080")
    server.serve_forever()

if __name__ == "__main__":
    # Iniciar servidor HTTP em paralelo
    threading.Thread(target=manter_vivo, daemon=True).start()

    # Iniciar o bot
    asyncio.run(bot_main())
