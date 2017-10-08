import socket

class Command():
    def __init__(self, config):
        self.config = config
        self.server_url = config["server"]["server_url"]
        self.server_port = config["server"]["server_port"]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendMsg(self, args):
        try:
            self.socket.connect((self.server_url, self.server_port))
            self.socket.send(args.encode())
            self.socket.close()
        except ConnectionRefusedError:
            print("Server isn't started")

    def run(self, args):
        pass
