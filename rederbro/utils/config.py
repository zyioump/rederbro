import json
import os

class Config():
    def __init__(self):
        self.configFile = os.path.dirname(os.path.abspath(__file__))+"/../config.json"
        self.config = self.loadConf()

        #list of all command
        self.mainCommand = ["server", "sensors", "gopro"]

        #commandArgs --> a dict who contain all sub command of a command and if it take an argument
        # a : ((b, c), (d, f), ...)
        # a --> command name
        # b --> sub command name
        # c --> if sub command take an argument
        # d --> sub command name
        # f --> if sub command take an argument
        # ...
        # if sub commmand take an argument it must be on-->True or off-->False
        self.commandArgs = {"gopro" : (("takepic", False), ("relay", True), ("debug", True), ("fake", True), ("", True), ("clear", False)), "sensors" : (("debug", True), ("fake", True)), "server" : (("main", True), ("sensors", True), ("gopro", True))}

    def loadConf(self):
        """
        Load conf and convert it in dict
        """
        if self.configFile is not "":
            with open(self.configFile, 'r') as conf:
                config = json.load(conf)
        return config

    def checkargs(self, args):
        """
        Check if args given by docopt are usable and convert them in an usable tuple
        """

        #see self.commandArgs doc to understand
        for command in self.mainCommand:
            #check if this command is set in docopt argument
            if args[command]:
                for subcommand in self.commandArgs[command]:
                    #check if sub command is set in docopt argument
                    #args[0] can be empty when there are no sub commmand
                    if subcommand[0] is "" or args[subcommand[0]]:
                        #some sub command take no argument like takepic
                        if not subcommand[1]:
                            #return value --> (a (b, c))
                            # a --> command name
                            # b --> sub command name or command name when sub command name is empty
                            # c --> argument of sub command here True cause sub command take no argument
                            return (command, (subcommand[0] if subcommand[0] is not "" else command, True))
                        else:
                            #when sub command take argument we must check if on or off is set in docopt argument
                            if args["on"] or args["off"]:
                                #return value --> (a (b, c))
                                # a --> command name
                                # b --> sub command name or command name when sub command name is empty
                                # c --> argument of sub command here value of "on" in docopt argument
                                return (command, (subcommand[0] if subcommand[0] is not "" else command, args["on"]))

    def getConf(self):
        return self.config
