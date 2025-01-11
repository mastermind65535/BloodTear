import pefile

class WindowsEngine:
    def __init__(self, __FILE:str):
        self.__EXTAR = str(__FILE)
        self.__EXOBJ = pefile.PE(self.__EXTAR)

    def getArch(self): 
        arch = self.__EXOBJ.FILE_HEADER.dump_dict()["Machine"]["Value"]
        match hex(arch):
            case 0x8664: return "x64"
            case 0x014C: return "x86"
            case 0x01C0: return "arm"
            case 0xAA64: return "arm64"
            case _: return "Unknown"

    def parse_DOS(self): return self.__EXOBJ.DOS_HEADER.dump_dict()
    def parse_NT(self): return self.__EXOBJ.NT_HEADERS.dump_dict()
    def parse_File(self): return self.__EXOBJ.FILE_HEADER.dump_dict()
    def parse_Optional(self): return self.__EXOBJ.OPTIONAL_HEADER.dump_dict()