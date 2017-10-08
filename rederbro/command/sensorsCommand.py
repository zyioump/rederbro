from rederbro.command.command import Command
import json

class SensorsCommand(Command):
    def run(self, args):
        # args --> (a, b)
        # a --> sub command name
        # b --> sub command argument (True or False)

        # type --> command name
        # command --> sub command name + On or Off
        msg = {"type": "sensors", "command" : args[0]+"On" if args[1] is True else args[0]+"Off"}

        #send command to server using socket
        self.sendMsg(json.dumps(msg))
