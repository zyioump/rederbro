from rederbro.command.command import Command
import json

class GoproCommand(Command):
    def run(self, args):
        # args --> (a, b)
        # a --> sub command name
        # b --> sub command argument (True or False)

        # type --> command name
        # command --> sub command name + On or Off
        msg = {"type": "gopro", "command" : args[0]+"On" if args[1] is True else args[0]+"Off"}

        #send command to server using socket
        self.sendMsg(json.dumps(msg))
