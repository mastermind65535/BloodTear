import os

class Parser:
    def __init__(self, __FILE:str):
        self.__FILE = __FILE

    def readBytes(self):
        __FILE_STREAM = open(self.__FILE, "rb")
        _DATA = __FILE_STREAM.read()
        __FILE_STREAM.close()
        return _DATA