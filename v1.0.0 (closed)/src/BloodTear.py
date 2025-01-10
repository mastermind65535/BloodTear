# Core Engine
from Engine import Windows
from Engine import Linux
from Engine import Android
from Engine import MacOS
from Engine import iOS

# Parser Engine
from Engine.Arch import x86
from Engine.Arch import x64
from Engine.Arch import arm
from Engine.Arch import arm64

# Decompile Engine
from Engine.Decompiler import C
from Engine.Decompiler import CSharp
from Engine.Decompiler import Python
from Engine.Decompiler import PythonByte
from Engine.Decompiler import Java

# Extra
from Engine.Universal import StringParser
from Engine.Universal import DataParser
from Engine.Universal import Analyzer

import logging
import traceback
import os
import sys
import subprocess
import tempfile
import argparse

if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'): current_file_path = os.path.abspath(sys.executable)
    else: current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    __RUN_DIR = current_dir
    _PARSER = argparse.ArgumentParser(
        prog="BloodTear",
        description="Advanced Decompiler & Disassembler",
        epilog="Disclaimer: This software is intended to be used for legal activities and educational purposes only.\nAny legal responsibility arising from the misuse of this software is solely on the user."
    )
    _PARSER.add_argument("--minlen", type=int, help="Set minimum length for string detection.", default=4)
    _PARSER.add_argument("--verbose", help="Print verbose", default=False, action='store_true')
    _PARSER.add_argument("--force", help="Force action and ignore warnings", default=False, action='store_true')
    _PARSER.add_argument("-l", "--list", help="List information", choices=["string", "variable", "function", "pyc"])
    _PARSER.add_argument("-f", "--find", help="Find information")
    _PARSER.add_argument("-o", "--output", type=str, help="Save output to the certain file")
    _PARSER.add_argument("-d", "--decompile", type=str, help="Decompile the executable file", choices=["c", "csharp", "java", "py", "pyc", "pyc-dis"])
    _PARSER.add_argument("-s", "--scan", type=bool, help="Scan the executable file", action="store_true")
    _PARSER.add_argument("--pyc", type=str, help="Set target pyc file")
    _PARSER.add_argument('filename')

    if len(sys.argv[0]) <= 1:
        _PARSER.print_help()
        sys.exit(0)

    _ARGS = _PARSER.parse_args()

    logger = logging.getLogger("BloodTear")
    _LEVEL = logging.INFO
    _FORMAT = '%(message)s'
    if (_ARGS.verbose == True): 
        _LEVEL = logging.DEBUG
    logging.basicConfig(format=_FORMAT, level=_LEVEL)


    if (_ARGS.output != None):
        if not str(_ARGS.output).split(".")[-1] in ["txt", "log"] and _ARGS.force == False:
            logger.warning("You must use either .txt or .log file! Use --force option to force using this extension as a log file.")
            sys.exit()
        with open(_ARGS.output, "w") as INIT_LOG: INIT_LOG.write("")
        INIT_LOG.close()
        FILE_LOGGER = logging.FileHandler(_ARGS.output)
        FILE_LOGGER.setLevel(_LEVEL)
        FILE_LOGGER.setFormatter(logging.Formatter(_FORMAT))
        logger.addHandler(FILE_LOGGER)
    
    logger.debug(_ARGS)

    try:
        __EXTAR = _ARGS.filename
        __FILE_DATA = DataParser.Parser(__EXTAR)
        fileBytes = __FILE_DATA.readBytes()

        if (_ARGS.list == "string"):
            minLen = _ARGS.minlen
            __STRING_TABLE = StringParser.Parser(fileBytes, min_length=minLen)
            table = __STRING_TABLE.parse_all()
            if (_ARGS.find != None): table = __STRING_TABLE.find_all(_ARGS.find)
            if len(table) == 0:
                logger.info("[-] No items found")
                sys.exit(0)
            maxValue = [item[0] for item in table][-1]
            logger.info(f"{'[File Offset]'.ljust(20)}[String]")
            for offset, string in table:
                pad = "0" * ((len(str(maxValue))+6))
                logger.info(f"{f'{pad[len(str(offset)):]}{offset}:'.ljust(20)}{string}")

        elif (_ARGS.scan == True):
            UniversalEngine = Analyzer.Analyze(__EXTAR)
            __EXOPS = UniversalEngine.getOS()
            if __EXOPS == "Windows":
                WinEngine = Windows.WindowsEngine(__EXTAR)
                __EXARC = WinEngine.getArch()
                match __EXARC:
                    case "x64":
                        pass

        # Decompile

        elif (_ARGS.list == "pyc"):
            DecompileEngine = Python.Loader(__EXTAR, __RUN_DIR)
            PYC_Files = DecompileEngine.parse_PYC()
            for file in PYC_Files:
                logger.info(file)

        elif (_ARGS.decompile == "py"):
            DecompileEngine = Python.Loader(__EXTAR, __RUN_DIR)
            PYC_Files = DecompileEngine.parse_PYC()
            if (_ARGS.pyc == None):
                for file in PYC_Files:
                    logger.info("-" * 20 + str(file).upper() + "-" * 20)
                    logger.info(PYC_Files[file])
            else:
                logger.info(PYC_Files[_ARGS.pyc])

        elif (_ARGS.decompile == "pyc"):
            DecompileEngine = PythonByte.Loader(__EXTAR, __RUN_DIR)
            PYC_Files = DecompileEngine.parse_PYC()
            if (_ARGS.pyc == None):
                for file in PYC_Files:
                    logger.info("-" * 20 + str(file).upper() + "-" * 20)
                    logger.info(PYC_Files[file])
            else:
                logger.info(PYC_Files[_ARGS.pyc])

    except Exception as e:
        logger.critical(f"Fatal Error: {e}")
        logger.debug(traceback.format_exc())