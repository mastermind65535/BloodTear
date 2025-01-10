import re

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