from threading import Thread

class AcceptConnection(Thread):
    def __init__(self, socket, logger):
        Thread.__init__(self)
        self.connected = False
        self.alreadyUsed = False
        self.socket = socket
        self.logger = logger
        self.data = []
        self.logger.info("New thread created to accept connection")

    def isConnected(self):
        return self.connected

    def isAlreadyUsed(self):
        return self.alreadyUsed

    def getAndClearData(self):
        returnData = self.data
        self.data = []

        return returnData

    def run(self):
        client , address = self.socket.accept()
        self.logger.warning("{} is now connected !".format(address[0]))
        self.connected = True
        self.alreadyUsed = True

        run = True

        while run:
            answer = client.recv(255).decode()

            if answer is not "":
                self.data.append(answer)
            else:
                run = False

        client.close()
        self.logger.warning("{} is now disconnected !".format(address[0]))
        self.connected = False
