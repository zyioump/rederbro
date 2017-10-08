import json
import os

class Config():
    def __init__(self):
        self.configFile = os.path.dirname(os.path.abspath(__file__))+"/../config.json"
        self.config = self.loadConf()
        self.mainCommand = ["server", "sensors", "gopro"]
        self.commandArgs = {"gopro" : (("takepic", False), ("relay", True), ("debug", True), ("fake", True), ("", True)), "sensors" : (("debug", True), ("fake", True)), "server" : (("main", True), ("sensors", True), ("gopro", True))}

    def loadConf(self):
        if self.configFile is not "":
            with open(self.configFile, 'r') as conf:
                config = json.load(conf)
        return config

    def checkargs(self, args):
        for command in self.mainCommand:
            if args[command]:
                for arg in self.commandArgs[command]:
                    if arg[0] is "" or args[arg[0]]:
                        if not arg[1]:
                            return (command, (arg[0], True))
                        else:
                            if args["on"] or args["off"]:
                                return (command, (arg[0] if arg[0] is not "" else command, args["on"]))

    def getConf(self):
        return self.config
