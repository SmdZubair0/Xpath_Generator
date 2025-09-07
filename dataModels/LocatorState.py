from typing import TypedDict, List
from lxml import etree

class LocatorState(TypedDict):
    raw_element : str # element
    raw_element_dom : str # element with its siblings and parent
    dom : etree._ElementTree
    element : etree._ElementTree
    element_dom : etree._ElementTree
    name : str
    locator : List[str]
    type : List[str]