from abc import ABC, abstractmethod
from lxml import etree
from pathlib import Path


class ReadDOM(ABC):
    
    @abstractmethod
    def readFromFile(self, path: Path) -> etree._ElementTree:
        pass

    @abstractmethod
    def readFromString(self, string: str) -> etree._ElementTree:
        pass