import os
import re

from . import config


class ModuleWalker:
    def __init__(self, modulePath):
        self.modulePath = modulePath
        self.exclusionList = set()
        self._populateExclusionList()

    def generateMapFile(self, mapFilePath) -> str:
        with open(mapFilePath, "a", encoding="utf-8") as map:
            for item in self.exclusionList:
                if "=" not in item:
                    map.write(f"{item}={item}\n")

        return os.path.abspath(mapFilePath)

    def _populateExclusionList(self) -> None:
        if os.path.isfile(self.modulePath):
            self._processFile(self.modulePath)
        elif os.path.isdir(self.modulePath):
            for root, _, files in os.walk(self.modulePath):
                for filename in files:
                    if self._isTopModule(filename):
                        filePath = os.path.join(root, filename)
                        self._processFile(filePath)

    def _processFile(self, filePath) -> None:
        with open(filePath, "r", encoding="utf-8") as topModule:
            for line in topModule:
                line = line.strip()
                if self._isInputOutputLine(line):
                    self._processInputOutputLine(line)
                    continue
                if self._isLocalParamLine(line):
                    self._processLocalParamLine(line)
                    continue

    def _isTopModule(self, filename) -> bool:
        if os.path.basename(filename) in config.rtl_top_modules:
            return True
        return False

    def _processInputOutputLine(self, line) -> None:
        pattern = r"(?:input|output\s+logic)?\s*(?:\[\d+:\d+\]\s*)?(?:CL\d+_)?(\w+?)(?:_\d+)?(?:_[ie]\d+)?\s*[,;]"
        match = re.match(pattern, line)
        if match:
            self.exclusionList.add(match.group(1))

    def _processLocalParamLine(self, line) -> None:
        pattern = (
            r"\blocalparam\s+(?:CL\d+_I\d+_|CL\d+_E\d+_|CL\d+_)?(\w+)\s*=\s*[\d.]+\s*;"
        )
        matches = re.findall(pattern, line)
        for paramMatch in matches:
            self.exclusionList.add(paramMatch)

    def _isInputOutputLine(self, line) -> bool:
        return re.search(r"\b(input|output)\b", line) is not None

    def _isLocalParamLine(self, line) -> bool:
        return "localparam" in line
