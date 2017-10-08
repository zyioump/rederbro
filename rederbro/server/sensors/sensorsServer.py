from rederbro.server.server import Server

import time

class SensorsServer(Server):
    def __init__(self):
        Server.__init__(self, config, "sensors")

    def start(self):
        self.logger.info("Server started")
        while self.running:
            time.sleep(self.delay)
