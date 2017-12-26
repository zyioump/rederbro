from rederbro.server.worker import Worker
from rederbro.utils.serialManager import SerialManager
from rederbro.command.command import Command
import time
import json

try:
    import RPi.GPIO as GPIO
except:
    pass


class GoproServer(Worker):
    """
    """
    def clear(self):
        if self.fakeMode:
            self.logger.info("Arduino serial cleared")
        else:
            self.arduino.clear()

    def turnGopro(self, state, full=True):
        """
        Switch gopro to state value
        """
        self.logger.info("Turn gopro {}".format(state))

        if self.relayOn:
            # relay must be on before switch on gopro
            if self.fakeMode:
                # when fake mode is on
                self.goproOn = state
                self.logger.info("Turned gopro {} (fake mode)".format(state))

            else:
                #when fake mode is off
                if state == "on":
                    #turn on
                    error, answer = self.arduino.sendMsg("I", "ON")

                    if error:
                        self.logger.error("Failed to turn gopro on")
                        self.goproOn = False
                        return self.goproOn

                    else:
                        if full:
                            error = self.changeMode(force=True)

                            if error:
                                self.logger.error("Failed to turn gopro on")
                                self.goproOn = False
                                return self.goproOn

                            else:
                                self.logger.info("Gopro turned on (full mode)")
                                self.goproOn = True
                                return self.goproOn

                        else:
                            self.logger.info("Gopro turned on (not full mode)")
                            self.goproOn = True
                            return self.goproOn

                else:
                    #turn off
                    if not self.goproOn:
                        self.turnGopro(True, full=False)

                    error, answer = self.arduino.sendMsg("O", "OFF")

                    if error:
                        self.logger.error("Failed to turn gopro off")
                        self.goproOn = True
                        return self.goproOn

                    else:
                        self.logger.info("Gopro turned off")
                        self.goproOn = False
                        return self.goproOn
        else:
            self.logger.error("Failed to change gopro status cause relay is off")
            self.goproOn = False
            return self.goproOn


    def turnRelay(self, state):
        """
        Switch relay to state value
        """
        self.logger.info("Turn relay {}".format(state))

        if self.fakeMode:
            #when fake mode is on
            self.relayOn = state
            self.logger.info("Turned relay {} (fake mode)".format(state))

        else:
            #when fake mode is off
            if state == "on":
                GPIO.output(self.config["relay_pin"], GPIO.HIGH)
                self.relayOn = True
            else:
                GPIO.output(self.config["relay_pin"], GPIO.LOW)
                self.relayOn = False
                self.goproOn = False

            self.logger.info("Turned relay {}".format(state))

    def changeMode(self, force=False):
        """
        Ask arduino to set gopro mode to photo
        """
        self.logger.info("Change gopro mode to photo")

        if self.fakeMode:
            self.logger.info("Gopro mode is photo")
            return False
        else:
            if force or self.goproOn:
                error, answer = self.arduino.sendMsg("M", "PHOTO_MODE")

                if error:
                    self.logger.error("Failed to change gopro mode")
                    return True
                else:
                    self.logger.info("Gopro mode is photo")
                    return False
            else:
                self.logger.error("Failed to change gopro mode cause gopro is off")
                return True

    def askCampaign(self, goproFail):
        args = {}
        args["time"] = time.asctime()
        args["goproFail"] = goproFail
        msg = ("add_picture" , args)
        cmd = Command(self.config, "campaign")
        cmd.run(msg)


    def takePic(self, force=False):
        """
        Ask arduino to take picture
        """
        self.logger.info("Take picture")

        if force or self.goproOn:
            if self.fakeMode:
                self.logger.info("Gopro took picture (fake mode)")
                self.askCampaign("000000")
                return False

            errorNB = 0

            error, answer = self.arduino.sendMsg("T", "ID2")
            errorNB += 1 if error else 0

            error, answer =  self.arduino.waitAnswer("ID1s")
            errorNB += 1 if error else 0

            goproFail = [(), "000000"]
            if error:
                error, answer =  self.arduino.waitAnswer("")
                goproFail[1] = answer
                for i in range(len(answer)):
                    if answer[i] == "1":
                        goproFail[0].append(5-i)

                error, answer =  self.arduino.waitAnswer("ID1s")
                self.logger.error("Gopro {} failed to take picture".format(goproFail[0]))

            error, answer =  self.arduino.waitAnswer("TAKEN")
            errorNB += 1 if error else 0

            self.askCampaign(goproFail[1])

            if errorNB == 0:
                self.logger.info("All gopro took picture")
                return False
            else:
                self.logger.info("Gopro failed to took picture")
                return True
        else:
            self.logger.error("Gopro can't take picture cause gopro is off")
            return True

    def __init__(self, config):
        #Use the __init__ of the server class
        Worker.__init__(self, config, "gopro")


        try:
            #init arduino
            self.arduino = SerialManager(self.config, self.logger, "arduino")
            self.clear()
        except:
            self.logger.error("Can't connect to arduino")
            self.setFakeMode("on")

        try:
            #init GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(self.config["relay_pin"], GPIO.OUT)
        except:
            self.logger.error("Not on a rpi")
            if not self.fakeMode:
                self.setFakeMode("on")

        #switch off relay to be sure that gopro are off
        self.turnRelay(False)

        self.goproOn = False
        self.relayOn = False

        #dict who link a command to a method
        # a : (b, c)
        # a --> command name
        # b --> method who can treat the command
        # c --> if there are argument for the method
        self.command = {\
            "debug" : (self.setDebug, True),\
            "fake" : (self.setFakeMode, True),\
            "gopro" : (self.turnGopro, True),\
            "relay" : (self.turnRelay, True),\
            "takepic" : (self.takePic, False),\
            "clear" : (self.clear, False)\
        }
