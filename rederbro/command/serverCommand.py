from rederbro.command.command import Command
from rederbro.server.main.mainServer import MainServer
from rederbro.server.gopro.goproServer import GoproServer
from rederbro.server.sensors.sensorsServer import SensorsServer

class ServerCommand(Command):
    def run(self, args):
        # args --> (a, b)
        # a --> sub command name
        # b --> sub command argument (True or False)
         
        self.server = {"main" : MainServer, "sensors" : SensorsServer, "gopro" : GoproServer}


        # if sub command arg is True we launch th server
        if args[1]:
            serverClass = self.server[args[0]](self.config)
            serverClass.start()
