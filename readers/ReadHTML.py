from .ReadDOM import ReadDOM
from typing import Optional
from lxml import etree, html
from pathlib import Path

class ReadHTML(ReadDOM):

    def readFromFile(self, path: Path) -> etree._ElementTree:
        return html.parse(path).getroot()
    
    def readFromString(self, string: str) -> etree._ElementTree:
        element = html.fromstring(string)
        return etree.ElementTree(element).getroot()