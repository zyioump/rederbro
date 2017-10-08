from rederbro.server.server import Server

import time

class SensorsServer(Server):
    def start(self):
        self.logger.info("Server started")
        while self.running:
            time.sleep(self.delay)
