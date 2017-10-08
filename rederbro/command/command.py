import socket

class Command():
    def __init__(self, config):
        self.config = config
        self.server_url = config["server"]["server_url"]
        self.server_port = config["server"]["server_port"]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendMsg(self, args):
        """
        Used to send a msg to main server using url and port found in config
        msg must be a string who contain a json to be undertand by the server
        """
        try:
            self.socket.connect((self.server_url, self.server_port))
            #msg must be convert in byte before being send
            self.socket.send(args.encode())
            self.socket.close()
        except ConnectionRefusedError:
            print("Server isn't running")

    def run(self, args):
        """
        Method called by main class
        Must be overwrited
        """
        pass
