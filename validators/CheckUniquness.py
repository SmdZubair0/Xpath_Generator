from lxml import etree
from abc import ABC, abstractmethod

class CheckUniquness(ABC):

    def __init__(self, dom : etree._ElementTree):
        self.dom = dom

    @abstractmethod
    def check(locator:str) -> bool:
        pass

class CheckUniqunessInHTML(CheckUniquness):

    def __init__(self, dom : etree._ElementTree):
        self.dom = dom

    def check(locator : str) -> bool:
        pass

class CheckUniqunessInXML(CheckUniquness):

    def __init__(self, dom : etree._ElementTree):
        self.dom = dom

    def check(locator : str) -> bool:
        pass