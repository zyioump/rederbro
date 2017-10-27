from rederbro.server.server import Server
from rederbro.utils.serialManager import SerialManager
import serial
import math
import time

class SensorsServer(Server):
    """
    A server who manage sensors :
                            --> gps
                            --> compas
    """

    def turnAutomode(self, state):
        """
        Turn automode on or off (state).

        Auto mode will take a picture every self.distace meter.
        """
        self.logger.info("Auto mode turned {}".format(state))
        self.auto_mode = True if state == "on" else False

    def setDistance(self, distance):
        """
        Set distance between picture in auto mode.

        This method don't turn on auto mode.
        """
        self.distance = distance
        self.logger.info("Distance between photo set to {}".format(self.distance))

    def getDistance(self, cordA, cordB):
        cordA = [math.radians(cordA[0]), math.radians(cordA[1])]
        cordB = [math.radians(cordB[0]), math.radians(cordB[1])]

        distanceBetweenPoint = self.earth_radius * (math.pi/2 - math.asin( math.sin(cordB[0]) * math.sin(cordA[0]) + math.cos(cordB[1] - cordA[1]) * math.cos(cordB[0]) * math.cos(cordA[0])))

        distanceBetweenPoint = math.degrees(distanceBetweenPoint)
        self.logger.info("Distance between now and last cord : {}".format(distanceBetweenPoint))
        return distanceBetweenPoint

    def toDegCord(self):
        """
        Return latitude and longitude in degree.

        google earth and some other thing prefer degree cordinate.
        """
        lat = self.lastCord[0]
        lon = self.lastCord[1]
        # ensure that we have data to work with
        if lat is not None and lon is not None and len(lat) > 0 and len(lon) > 0:
            try:
                if lat[-1] == "N":  # define the signe
                    lat = float(lat[:-1])/100.0
                else:
                    lat = -float(lat[:-1])/100.0

                if lon[-1] == "W":  # define the signe
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

        return 0, 0  # mean it didin't work

    def getCord(self):
        self.logger.info("Get cordonate")
        if self.fakeMode:
            self.lastCord = [0, 0, 0]
            self.logger.info("Cordonate : {} (fake mode)".format(self.lastCord))

        else:
            checkNB = int(self.time_out/0.5)

            for i in range(checkNB):
                error, answer = self.gps.waitAnswer("")
                answer = answer.split(",")
                if answer[0] == "$GPGGA":
                    error = False
                    break

            if not error:
                #$GPGGA,<time>,<lat>,<N/S>,<lon>,<E/W>,<positionnement type>,<satelite number>,<HDOP>,<alt>,<other thing>
                self.lastSat = answer[7]
                self.lastCord = [answer[2]+answer[3], answer[4]+answer[5], answer[9]]
                self.lastTime = answer[1]
                self.lastHdop = answer[8]

                self.toDegCord()

                self.logger.info("Current cordonate : {}".format(self.lastCord))

            else:
                self.lastCord = [0, 0, 0]
                self.logger.error("Failed to get new cordonate")

        return self.lastCord

    def checkAutoMode(self):
        if self.auto_mode:
            self.getCord()
            lastDistance = self.getDistance(self.lastPhotoCord, self.lastCord)
            if lastDistance >= self.distance:
                self.lastPhotoCord = self.lastCord
                self.logger.info("Take picture (auto mode)")

    def start(self):
        """
        Method called by server command
        """
        self.logger.warning("Server started")
        while self.running:
            self.checkCommand()
            self.checkAutoMode()
            time.sleep(self.delay)

    def __init__(self, config):
        Server.__init__(self, config, "sensors")

        self.lastSat = 0
        self.lastCord = [0, 0, 0]
        self.lastPhotoCord = [0, 0, 0]
        self.lastTime = 0
        self.lastHdop = 0

        self.earth_radius = 6372.795477598 * 1000

        self.command = {\
            "debug": (self.setDebug, True),\
            "fake": (self.setFakeMode, True),\
            "automode": (self.turnAutomode, True),\
            "distance": (self.setDistance, True),\
            "cord": (self.getCord, False)\
        }

        self.distance = 5
        self.auto_mode = False

        self.time_out = config["gps"]["time_out"]

        try:
            self.gps = SerialManager(self.config, self.logger, "gps")
        except:
            self.setFakeMode("on")
