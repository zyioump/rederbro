from threading import Thread

class AcceptConnection(Thread):
    """
    This thread allow you to accept a connection an receive command
    """

    def __init__(self, socket, logger):
        Thread.__init__(self)
        self.connected = False

        #this thread can be used only one time
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
        """
        Return data send by client and clean this data
        """
        returnData = self.data
        self.data = []

        return returnData

    def run(self):
        #wait for a connection
        client , address = self.socket.accept()
        self.logger.warning("{} is now connected !".format(address[0]))
        self.connected = True
        self.alreadyUsed = True

        run = True

        #while someone is connected
        while run:
            #wait for an msg
            msg = client.recv(255).decode()

            #when msg in not empty append him to our data
            if msg is not "":
                self.data.append(msg)
            else:
                run = False

        #when client is disconnected when must close the socket
        client.close()
        self.logger.warning("{} is now disconnected !".format(address[0]))
        self.connected = False
