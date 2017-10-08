from rederbro.command.command import Command
import json

class SensorsCommand(Command):
    def run(self, args):
        msg = {"type": "sensors", "command" : args[0]+"On" if args[1] is True else args[0]+"Off"}
        self.sendMsg(json.dumps(msg))
