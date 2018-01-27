import zmq


class MainServer():
    def __init__(self, config):
        self.config = config
        self.context = zmq.Context()
        bind_address = "tcp://{}:{}"

        self.client = self.context.socket(zmq.PULL)
        self.client.bind(bind_address.format(self.config["server"]["bind_address"], self.config["server"]["client_server_port"]))

        self.worker = self.context.socket(zmq.PUB)
        self.worker.bind(bind_address.format(self.config["server"]["bind_address"], self.config["server"]["worker_server_port"]))

    def start(self):
        zmq.device(zmq.FORWARDER, self.client, self.worker)
