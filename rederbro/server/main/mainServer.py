import socket
import time
import os
import logging
import json

from rederbro.server.main.acceptConnection import AcceptConnection
from rederbro.utils.dataSend import DataSend

from logging.handlers import RotatingFileHandler

class MainServer():
    def __init__(self, config):
        self.config = config
        self.socketThreads = []
        self.running = True
        self.threadFree = False

        #get some info from the config
        maxConnection = config["server"]["max_connection"]
        port = config["server"]["server_port"]
        bindAddress = config["server"]["bind_address"]

        #bind the server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((bindAddress, port))
        self.socket.listen(maxConnection)

        self.commands = []

        #init logger
        self.logFile = os.path.dirname(os.path.abspath(__file__))+"/../../log/main_server.log"

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('main %(asctime)s :: %(levelname)s :: %(message)s')

        file_handler = RotatingFileHandler(self.logFile, 'a', 1000000, 1)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        self.delay = self.config["server"]["delay"]

        #init all pipe to sub server using datasend
        self.pipes = {"gopro" : DataSend(os.path.dirname(os.path.abspath(__file__))+"/../gopro/gopro.pipe", "client"), "sensors" : DataSend(os.path.dirname(os.path.abspath(__file__))+"/../sensors/sensors.pipe", "client")}

    def start(self):
        self.logger.warning('Server started')
        while self.running:
            goodThread = 0
            toRms = []

            for i in range(0, len(self.socketThreads)):
                if not self.socketThreads[i].isConnected():
                    if self.socketThreads[i].isAlreadyUsed():
                        #when someone already used this thread we must kill him
                        toRms.append(i)
                    if not self.socketThreads[i].isAlreadyUsed():
                        #when nobody already use this thread
                        goodThread += 1

                datas = self.socketThreads[i].getAndClearData()

                #if data is not empty append them in our command list
                if len(datas) is not 0:
                    for data in datas:
                        self.commands.append(data)

            #remove and kill all thread who are already used
            for toRm in toRms:
                del self.socketThreads[toRm]
                self.logger.info("A thread as been deleted")
                self.logger.info("{} thread alive".format(len(self.socketThreads)))

            if goodThread is 0:
                self.threadFree = False


            if self.threadFree is False:
                #if no thread si free
                #we must create another to accept connection
                acceptConnection = AcceptConnection(self.socket, self.logger)
                acceptConnection.start()

                self.socketThreads.append(acceptConnection)
                self.threadFree = True
                self.logger.info("{} thread alive".format(len(self.socketThreads)))


            #treat all command send by client
            for command in self.commands:
                try:
                    #convert command in json
                    command = json.loads(command)

                    #send commmand to the pipe of the type using datasend
                    self.pipes[command["type"]].writeLine(json.dumps({"command" : command["command"], "args": command["args"]}))
                    self.logger.info("New command : {}".format(command))
                except Exception as e:
                    #when command receive is not a json
                    #we can't treat him
                    self.logger.error("Unexpecting command")
                    self.logger.error(e)

            #clean all command already treated
            self.commands = []

            time.sleep(self.delay)
