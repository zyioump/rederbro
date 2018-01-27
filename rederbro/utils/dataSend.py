
class DataSend:
    """
    This class allow you to make communication between process it like a pipe
    """

    def __init__(self, fileLoc, typeWR):
        self.fileLoc = fileLoc
        # typeWR is "client" or "server"
        # "server" when we read text in pipe file
        # "client" when we just append text in pipe file
        self.typeWR = typeWR
        self.file = None
        self.clean()

    def open(self):
        """
        Open pipe file in append mode when type is client or in read mode when type is server
        """
        self.file = open(self.fileLoc, "a" if self.typeWR is "client" else "r")

    def close(self):
        """
        Close pipe file
        """
        self.file.close()

    def readText(self):
        """
        Read text in pipe file and convert him in list of line non empty, your type must be server
        """

        # open pipe file when he is not open
        if self.file is None or self.file.closed is True:
            self.open()

        # read pipe file
        text = self.file.read()
        # make a list of line in the pipe file
        text = text.split("\n")

        # this list will be the same of text list by without empty line
        greatText = []

        # put non empty line in greatText list
        for line in text:
            if line is not "":
                greatText.append(line)

        # close pipe file
        self.close()
        return greatText

    def writeLine(self, msg):
        """
        Write instruction in pipe file, your type must be client
        """
        # open pipe file when he is not open
        if self.file is None or self.file.closed is True:
            self.open()

        # write instruction in pipe file
        self.file.write(msg+"\n")

        # close pipe file
        self.close()

    def clean(self):
        """
        Just clear pipe file by opening him in write mode
        """

        open(self.fileLoc, 'w').close()
