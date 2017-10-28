from rederbro.command.command import Command
import json

class SensorsCommand(Command):
    def run(self, args):
        # args --> (a, b)
        # a --> sub command name
        # b --> sub command argument (True or False)

        # type --> command name
        # command --> sub command name + sub command args
        msg = {"type": "sensors", "command" : args[0], "args" : args[1]}

        #send command to server using socket
        self.sendMsg(json.dumps(msg))
