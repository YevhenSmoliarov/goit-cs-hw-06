import os
import socket
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from datetime import datetime
import json

# Статичні файли
STATIC_DIR = './front-init'

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Маршрутизація
        if self.path == "/":
            self.path = "/index.html"
        elif self.path == "/message":
            self.path = "/message.html"
        elif self.path.startswith("/static"):
            self.path = self.path.replace("/static", "")
        else:
            self.path = "/error.html"

        try:
            # Сервінг HTML та статичних файлів
            super().do_GET()
        except Exception as e:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        if self.path == "/submit-message":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_params = parse_qs(post_data.decode('utf-8'))
            
            # Зберігаємо дані форми
            message_data = {
                'date': datetime.now().isoformat(),
                'username': post_params['username'][0],
                'message': post_params['message'][0]
            }

            # Відправляємо дані Socket-серверу
            send_to_socket_server(message_data)

            # Перенаправлення назад на форму
            self.send_response(303)
            self.send_header('Location', '/message')
            self.end_headers()

# Запуск вебсерверу
def run_web_server():
    port = 3000
    httpd = HTTPServer(('', port), MyHandler)
    print(f"Запуск HTTP-сервера на порту {port}")
    httpd.serve_forever()

# Socket-сервер
def send_to_socket_server(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('localhost', 5000))
        sock.sendall(json.dumps(data).encode('utf-8'))

def run_socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind(('localhost', 5000))
        server_sock.listen()

        while True:
            client_sock, addr = server_sock.accept()
            with client_sock:
                data = client_sock.recv(1024)
                if data:
                    message_data = json.loads(data.decode('utf-8'))
                    print(f"Отримано повідомлення: {message_data}")
                    # Зберігаємо у MongoDB (псевдо-код)
                    # save_to_mongodb(message_data)

if __name__ == "__main__":
    # Запуск вебсерверу та Socket-сервера у різних потоках
    threading.Thread(target=run_web_server).start()
    threading.Thread(target=run_socket_server).start()
