from rederbro.command.command import Command
from rederbro.server.mainServer import MainServer
from rederbro.server.goproServer import GoproServer
from rederbro.server.sensorsServer import SensorsServer
from rederbro.server.campaignServer import CampaignServer


class ServerCommand(Command):
    def run(self, args):
        # args --> (a, b)
        # a --> sub command name
        # b --> sub command argument (True or False)

        self.server = {"main": MainServer, "sensors": SensorsServer, "gopro": GoproServer, "campaign": CampaignServer}

        # if sub command arg is True we launch the server
        if args[1]:
            serverClass = self.server[args[0]](self.config)
            serverClass.start()
