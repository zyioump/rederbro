from rederbro.server.server import Server
import os
import json
import time

class CampaignServer(Server):
    def add_picture(self, picInfo):        
        cord = json.loads(self.pipes["cord"].readText()[-1])
        self.pipes["cord"].clean()

        toPut = [picInfo["time"], cord["lat"], cord["lon"], cord["alt"], cord["head"], picInfo["goproFailed"]]
        text = ""
        for thing in toPut:
            text += str(thing)
            text += "; "

        text = text[:-2]

        self.logger.info(text+" put in csv campaign file")

        with open(self.currentCampaignPath, "a") as csv:
            csv.write(text+"\n")

    def newCampaign(self, args):
        self.attachCampaign(args)

        with open(self.currentCampaignPath, "w") as csv:
            csv.write("time; lat; lon; alt; rad; goProFailed\n")

        self.logger.info(args+" campaign created")

    def attachCampaign(self, args):
        self.currentCampaignPath = self.baseCampaignPath + args + ".csv"
        self.logger.info("Campaign attached to "+args)

    def __init__(self, config):
        #Use the __init__ of the server class
        Server.__init__(self, config, "campaign")

        self.baseCampaignPath = os.path.dirname(os.path.abspath(__file__))+"/../../campaign/"

        self.newCampaign("pictureInfo")

        #dict who link a command to a method
        # a : (b, c)
        # a --> command name
        # b --> method who can treat the command
        # c --> if there are argument for the method
        self.command = {\
            "add_picture" : (self.add_picture, True),\
            "new" : (self.newCampaign, True),\
            "attach" : (self.attachCampaign, True)\
        }
