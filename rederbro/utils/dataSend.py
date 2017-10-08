class DataSend:
    def __init__(self, fileLoc, typeWR):
        self.fileLoc = fileLoc
        self.typeWR = typeWR
        self.file = None
        self.clean()

    def open(self):
        self.file = open(self.fileLoc, "a" if self.typeWR is "client" else "r")

    def close(self):
        self.file.close()

    def readText(self):
        if self.file is None or self.file.closed is True:
            self.open()

        text = self.file.read()
        text = text.split("\n")

        greatText = []

        for line in text:
            if line is not "":
                greatText.append(line)

        self.close()
        return greatText

    def writeLine(self, msg):
        if self.file is None or self.file.closed is True:
            self.open()

        self.file.write(msg+"\n")

        self.close()

    def clean(self):
        open(self.fileLoc, 'w').close()
