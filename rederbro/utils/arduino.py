import serial
import time

class Arduino():
    """
    This class allow you to send msg to an arduino and wait her answer
    """

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

        self.serial = serial.Serial(config["arduino"]["serial"], timeout=0.5)
        self.time_out = config["arduino"]["time_out"]

    def sendMsg(self, msg, correctAnswer):
        """
        Send msg to the arduino
        This method with send the msg and wait the answer.
        It will return if the answer send by arduino is not correctAnswer and return the bad anwswer or None
        """

        #send msg to arduino
        #msg must be convert in byte
        self.serial.write(msg.encode())
        self.logger.debug("{} send to arduino".format(msg.encode()))

        #Wait for the answer of arduino  if the answer of arduino is not correctAnswer error will be True
        #BadAnswer will be answer send by arduino
        error, badAnswer = self.waitAnswer(correctAnswer)

        return (error, badAnswer)

    def waitAnswer(self, correctAnswer, timeout=0):
        """
        Wait the answer of the arduino with an time out
        Check if it is correct or not and return it
        """
        if timeout == 0:
            checkNB = int(self.time_out / 0.5)
        else:
            checkNB = int(timeout / 0.5)
        #we will check checkNB time the answer before time out


        for i in range(checkNB):
            answer = self.serial.readline()
            self.logger.debug("{} receive from arduino".format(answer))

            #if the answer is realy an answer
            if answer != b'':
                #stop waiting for an answer
                break

        if answer == b'':
            self.logger.debug("Timed out")

        #the answer must be decode cause arduino send byte
        answer = answer.decode()

        error = True

        if answer == correctAnswer:
            error = False

        return (error, answer)

    def clear(self):
        self.logger.info("Start clear serial")
        error, answer = self.waitAnswer("", timeout=2)
        self.logger.debug("{} was in serial".format(answer))
        self.logger.info("Serial cleared")
