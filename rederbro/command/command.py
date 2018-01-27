import zmq


class Command():
    def __init__(self, config, topic):
        self.config = config
        self.topic = topic
        self.server_url = config["server"]["server_url"]
        self.server_port = config["server"]["client_server_port"]
        self.url = "tcp://"+self.server_url+":"+str(self.server_port)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)

    def sendMsg(self, args):
        """
        Used to send a msg to main server using url and port found in config
        msg must be a string who contain a json to be undertand by the server
        """

        self.socket.connect(self.url)
        self.socket.send_json(args)

    def run(self, args):
        """
        Method called by main class
        Must be overwrited
        """
        msg = {}
        msg["command"] = args[0]
        msg["args"] = args[1]
        msg["topic"] = self.topic

        self.sendMsg(msg)
