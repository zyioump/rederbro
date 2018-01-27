from rederbro.server.worker import Worker
import os
import zmq


class CampaignServer(Worker):
    def add_picture(self, picInfo):
        self.pictureNB += 1
        self.gps_infoReq.send_json({})
        gps = self.gps_infoReq.recv_json()
        text = "{}; {}; {}; {}; {}; {}; {}; {}\n".format(
            self.pictureNB,
            picInfo["time"],
            gps["lat"],
            gps["lon"],
            gps["alt"],
            gps["head"],
            gps["time"],
            picInfo["goproFail"]
        )

        self.logger.info("{} will be put in csv file".format(text))

        with open(self.currentCampaignPath, "a") as csv:
            csv.write(text)

    def newCampaign(self, args):
        self.attachCampaign(args)

        with open(self.currentCampaignPath, "w") as csv:
            csv.write("number; time; lat; lon; alt; rad; gps_time; goProFailed\n")

        self.logger.info(args+" campaign created")

    def attachCampaign(self, args):
        self.currentCampaignPath = self.baseCampaignPath + args + ".csv"
        self.logger.info("Campaign attached to "+args)

    def __init__(self, config):
        # Use the __init__ of the server class
        Worker.__init__(self, config, "campaign")

        self.baseCampaignPath = os.path.dirname(os.path.abspath(__file__))+"/../campaign/"

        self.newCampaign("pictureInfo")

        self.pictureNB = 0

        # dict who link a command to a method
        # a : (b, c)
        # a --> command name
        # b --> method who can treat the command
        # c --> if there are argument for the method
        self.command = {
            "add_picture": (self.add_picture, True),
            "new": (self.newCampaign, True),
            "attach": (self.attachCampaign, True)
        }

        urlGPS = "tcp://{}:{}".format(self.config["gps"]["server_url"], self.config["gps"]["rep_server_port"])

        self.gps_infoReq = self.context.socket(zmq.REQ)
        self.gps_infoReq.connect(urlGPS)
