from rederbro.command.command import Command
import json

class GoproCommand(Command):
    def run(self, args):
        msg = {"type": "gopro", "command" : args[0]+"On" if args[1] is True else args[0]+"Off"}
        self.sendMsg(json.dumps(msg))
