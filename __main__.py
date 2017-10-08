from docopt import docopt
from rederbro.utils.config import Config
from rederbro.command.command import Command
from rederbro.command.serverCommand import ServerCommand
from rederbro.command.goproCommand import GoproCommand
from rederbro.command.sensorsCommand import SensorsCommand

__doc__ ="""Open path view rederbro

Usage:
  opv server main on
  opv server gopro on
  opv server sensors on
  opv gopro relay on
  opv gopro relay off
  opv gopro on
  opv gopro off
  opv gopro takepic
  opv gopro debug on
  opv gopro debug off
  opv gopro fake off
  opv gopro fake on
  opv sensors debug on
  opv sensors debug off
  opv sensors fake on
  opv sensors fake off

Options:
  -h --help     Show this screen.

"""

command_list = {"server" : ServerCommand, "gopro": GoproCommand, "sensors" :  SensorsCommand}

config = Config().getConf()

def main():
    args = docopt(__doc__)
    parsedArgs = Config().checkargs(args)
    launchCommand(parsedArgs)

def launchCommand(args):
    command_list[args[0]](config).run(args[1])


if __name__ == "__main__":
    main()
