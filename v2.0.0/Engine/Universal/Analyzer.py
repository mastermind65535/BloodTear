from Engine.Universal import DataParser

class UnknownFormatError(Exception): pass

class Analyze:
    def __init__(self, __FILE:str):
        self.__EXTAR = str(__FILE)
        __FILE_DATA = DataParser.Parser(self.__EXTAR)
        self.fileBytes = __FILE_DATA.readBytes()

    def getOS(self):
        magicBytes = self.fileBytes[:4]
        if magicBytes == b'\x7fELF': return "Linux"
        elif magicBytes[:2] == b'MZ': return "Windows"
        elif magicBytes[:4] == b'\xca\xfe\xba\xbe': return "MacOS"
        else: raise UnknownFormatError(f"Unknown format (Magic Bytes: {magicBytes.hex()})")