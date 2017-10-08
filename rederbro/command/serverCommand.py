from rederbro.command.command import Command
from rederbro.server.main.mainServer import MainServer
from rederbro.server.gopro.goproServer import GoproServer
from rederbro.server.sensors.sensorsServer import SensorsServer

class ServerCommand(Command):
    def run(self, args):
        self.server = {"main" : MainServer, "sensors" : SensorsServer, "gopro" : GoproServer}
        if args[1]:
            serverClass = self.server[args[0]](self.config, args[0])
            serverClass.start()
