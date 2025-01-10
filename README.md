# BloodTear
Advanced Decompiler & Disassembler


## Version: v1.0.0
### Python Decompile
> Decompile using [pycdc & pycdas](https://github.com/zrax/pycdc)<br>
> Extract using [python-decompile3](https://github.com/rocky/python-decompile3)<br>
```Python
# Engine.Decompiler.Python

class Loader:
    def __init__(self, __FILE:str, __RUN_DIR:str):
        self.__FILE = str(__FILE)
        self.__OUTPUT_OBJ = tempfile.TemporaryDirectory()
        self.__OUTPUT = self.__OUTPUT_OBJ.name
        self.__RUN_DIR = str(__RUN_DIR)

    def parse_PYC(self):
        pycFiles = {}
        logger.debug("[+] Loading extractor...")
        
        arch = PyInstArchive(self.__FILE)
        if arch.open():
            if arch.checkFile():
                if arch.getCArchiveInfo():
                    arch.parseTOC()
                    arch.extractFiles(self.__OUTPUT)
                    arch.close()
                    logger.debug('[+] Successfully extracted pyinstaller archive: {0}'.format(self.__FILE))
                    logger.debug('')
                    logger.debug('You can now use a python decompiler on the pyc files within the extracted directory')
            arch.close()
        
        os.chdir("..")
        logger.debug("[+] Loading pyc files...")
        logger.debug(self.__OUTPUT)
        for file in os.listdir(self.__OUTPUT):
            try:
                if file.split(".")[-1] != "pyc": continue
                logger.debug(f"[+] PYC Found: {file}")
                _cmd = f"\"{os.path.join(self.__RUN_DIR, 'bin\\pycdc.exe')}\" \"{os.path.join(self.__OUTPUT, file)}\""
                logger.debug(_cmd)
                result = subprocess.check_output(_cmd, text=True)
                pycFiles[file] = result
            except Exception as e:
                logger.debug(f"[-] Error: {e}")
                continue

        self.__OUTPUT_OBJ.cleanup()
        
        return pycFiles
```

### Executable String Parser
> Idea from [Detect It Easy](https://www.majorgeeks.com/files/details/detect_it_easy.html)<br>
> Idea from [BinText](https://www.majorgeeks.com/files/details/bintext.html)<br>
```Python
# Engine.Universal.StringParser

class Parser:
    def __init__(self, __bytes:bytes, min_length=4):
        self.__bytes = __bytes
        self.min_length = int(min_length)

    def parse_all(self):
        pattern = rb'[ -~]{' + str(self.min_length).encode() + rb',}'
        matches = re.finditer(pattern, self.__bytes)
        result = []
        for match in matches:
            offset = match.start()
            string = match.group().decode('ascii', errors='ignore')
            result.append((offset, string))
        return result
    
    def find_all(self, key:str):
        found = []
        for offset, item in self.parse_all():
            if key in item: found.append([offset, item])
            else: continue
        return found
```

### Windows Header Parser
> Header parsing via [pefile]()
```Python
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
```

### Legacy Projects|
| Project Name          | Project Description                       | URL                                                                              | Status        |
|-----------------------|-------------------------------------------|----------------------------------------------------------------------------------|---------------|
| BytesCracker v1.0.0   | Python Capstone Disassembler              | [ByteCracker v1.0.0 ~ v2.5.0](https://github.com/mastermind65535/ByteCracker)    | **Failed**    |
| BytesCracker v2.0.0   | C++ Windows x64 & x86 Machine Code Parser | [ByteCracker v1.0.0 ~ v2.5.0](https://github.com/mastermind65535/ByteCracker)    | **Failed**    |
| BytesCracker v2.5.0   | C++ Windows x64 & x86 Machine Code Parser | [ByteCracker v1.0.0 ~ v2.5.0](https://github.com/mastermind65535/ByteCracker)    | **Failed**    |
| HDE v4.8.2            | Advanced Python Decompile Engine          | N/A                                                                              | **Failed**    |
| HDE v1.0.0            | Compiler & Linker Detector                | N/A                                                                              | **Failed**    |
