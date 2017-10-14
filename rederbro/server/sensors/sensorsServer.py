from rederbro.server.server import Server
import serial

import time

class SensorsServer(Server):
    def turnAutomode(self, state):
        self.logger.info("Auto mode turned {}".format(state))

    def setDistance(self, distance):
        self.distance = distance
        self.logger.info("Distance between photo set to {}".format(self.distance))

    def toDegCord(self):#google earth and some other thing prefer degree coordinate
        """
        return latitude and longitude in degree
        """
        lat = self.lastCord[0]
        lon = self.lastCord[1]
        if lat !=None and lon != None and len(lat)>0 and len(lon)>0:#ensure that we have data to work with
            try :
                if lat[-1]=="N":#define the signe
                    lat = float(lat[:-1])/100.0
                else:
                    lat = -float(lat[:-1])/100.0

                if lon[-1]=="W":#define the signe
                    lon = -float(lon[:-1])/100.0
                else:
                    lon = float(lon[:-1])/100.0
            except (TypeError, ValueError):
                return None, None
            lat_deg = int(lat)
            lat_min = (100.0*(float(lat)-lat_deg))/60
            lat = lat_deg+lat_min

            lon_deg = int(lon)
            lon_min = (100.0*(float(lon)-lon_deg))/60
            lon = lon_deg+lon_min

            self.lastCord[0] = lat
            self.lastCord[1] = lon
            return self.lastCord

        return 0, 0#mean it didin't work

    def getCoord(self):
        self.logger.info("Get coordonate")
        if self.fakeMode:
            self.lastCord = [0, 0 , 0]
            self.logger.info("Coordonate : {} (fake mode)".format(self.lastCord))
            return self.lastCord

        else:
            trame = [""]
            while trame[0] != "$GPGGA":
                msg = ""
                while not "\r\n" in msg:
                    msg += self.serial.read().decode()

                trame = msg.split(",")

            #$GGA,<time>,<lat>,<N/S>,<long>,<E/W>,<GPS-QUAL>,<satelite>,<hdop>,<alt>,<mode>,<otherthing>
            self.lastSat = trame[7]
            self.lastCord = [(trame[2]+trame[3]), (trame[4]+trame[5]), trame[9]]
            self.lastTime = trame[1]
            self.lastHdop = trame[8]

            self.toDegCord()

            self.logger.info("Coordonate : {}".format(self.lastCord))
            return self.lastCord

    def __init__(self, config):
        Server.__init__(self, config, "sensors")

        self.lastSat = 0
        self.lastCord = [0, 0, 0]
        self.lastTime = 0
        self.lastHdop = 0

        self.command = {\
            "debug" : (self.setDebug, True),\
            "fake" : (self.setFakeMode, True),\
            "automode" : (self.turnAutomode, True),\
            "distance" : (self.setDistance, True),\
            "getCoord" : (self.getCoord, False)\
        }

        self.distance = 5

        try:
            self.serial = serial.Serial(port=self.config["gps"]["serial"], baudrate=115200, timeout=1)
        except:
            self.setFakeMode(True)
