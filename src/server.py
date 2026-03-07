# Импорт встроенной библиотеки для работы веб-сервера
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import time  # Не используется, но оставил из твоего (можно убрать)

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети

class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """

    def do_GET(self):
        try:
            # Получаем папку где лежит server.py
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Строим путь относительно server.py -> на уровень выше -> templates
            file_path = os.path.join(base_dir, '..', 'templates', 'contacts.html')

            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(html_content, "utf-8"))
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")

    def do_POST(self):
        """ Метод для обработки входящих POST-запросов """
        content_length = int(self.headers['Content-Length'])  # Размер тела запроса
        body = self.rfile.read(content_length)  # Читаем тело
        # Печатаем данные в консоль (декодируем UTF-8 для читаемости)
        print(f"Received POST data: {body.decode('utf-8')}")
        self.send_response(200)  # OK
        self.end_headers()  # Завершение

# Запуск сервера (if __name__ — стандарт, как "старт игры")
if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started at http://{hostName}:{serverPort}")
    try:
        webServer.serve_forever()  # Запуск (Ctrl+C для остановки)
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")