from .ReadDOM import ReadDOM
from typing import Optional
from lxml import etree
from pathlib import Path

class ReadXML(ReadDOM):
    
    def readFromFile(self, path: Path) -> etree._ElementTree:
        return etree.parse(path).getroot()
    
    def readFromString(self, string: str) -> etree._ElementTree:
        element = etree.fromstring(string)
        return etree.ElementTree(element).getroot()
