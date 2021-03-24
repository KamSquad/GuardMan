import json
import socket
import time


class Socket:
    def __init__(self, port):
        self.sock = None
        self.port = port
        self.conn = None
        self.addr = None
        self.create()

    def create(self):
        try:
            self.sock = socket.socket()
            self.sock.bind(('', self.port))
        except Exception as ex:
            print(ex, ', waiting 10 secs..')
            time.sleep(10)
            self.create()

    def listen(self):
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()

    def connect(self, port, host='localhost'):
        self.sock.connect((host, port))

    def get_data(self):
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            return json.loads(data)

    def get_answer(self, data):
        data = json.dumps(data).encode('utf-8')
        self.sock.send(data)
        ans = self.sock.recv(1024).decode('utf-8')
        if ans != '':
            ans = json.loads(ans)
        return ans

    def send_data_after_listen(self, data):
        data = json.dumps(data).encode('utf-8')
        self.conn.send(data)
        # self.close()

    def close(self):
        self.conn.close()
