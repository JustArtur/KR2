import socket

HOST = '127.0.0.1'
PORT = 3000


class ServerSocket():
    def __init__(self, HOST, PORT):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        print("Server started!")
        self.calc = Calculator()
        self.accept_connection()
        self.recieve_data()

    def accept_connection(self):
        self.server.listen()
        self.conn, adr = self.server.accept()
        print(f"Successfully connected to {adr}")

    def recieve_data(self):
        print('Waiting for data!')
        while True:
            data = self.conn.recv(1024)
            print("Get data!")
            self._data_decode(data)

    def send_data(self, data):
        self.conn.send(data.encode())
        print(f"Sending {data}")

    def _data_decode(self, data):
        data = data.decode()
        print(f"Get {data}")
        if data == 'hist':
            self.send_data(self.calc.return_history())
        else:
            result = self.calc.calculation(data)
            self.send_data(result)


class Calculator():
    def __init__(self):
        self.history = []

    def return_history(self):
        return '\n'.join(self.history)

    def calculation(self, data):
        result = str(eval(data))
        self._save_in_history(data, result)
        print(f"Returning {result}")
        return result

    def _save_in_history(self, expressionn, result):
        self.history.append(expressionn + '=' + result)


if __name__ == '__main__':
    s = ServerSocket(HOST, PORT)
