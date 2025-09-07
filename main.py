from pathlib import Path
from typing import TypedDict

from generator import *
from readers import ReadDOM, ReadHTML
from dataModels import LocatorState
from lxml import etree
from validators import CheckUniqunessInHTML, CheckUniquness

def extract_element(state : LocatorState, reader: ReadDOM):
    """
        Take state object and ReadDOM object
        - convert and store raw_element to element
        - convert and store raw_element_dom to element dom
        - return state
    """
    state['element'] = reader.readFromString(state['raw_element'])
    state['element_dom'] = reader.readFromString(state['raw_element_dom'])
    return state

def generate_locator(state : LocatorState, strategies) -> LocatorState:
    for strategy in strategies:
        


if __name__ == "__main__":

    state : LocatorState  = LocatorState()
    reader : ReadDOM  = ReadHTML()

    filepath : Path = Path("C:\\Users\\smoha\\OneDrive\\Desktop\\xpathfinder\\dom.xml")
    state['dom'] = reader.readFromFile(filepath)

    state['raw_element'] = """<h3 id="1-what-is-automation-testing" class="a b c">1) What is Automation testing?</h3>"""
    state['raw_element_dom'] = """<div class="entry-content-wrap"><header class="entry-header post-title title-align-left title-tablet-align-inherit title-mobile-align-inherit"></header><div class="entry-content single-content"><h2 id="automation-testing-interview-questions-and-answers-for-freshers"></h2><h3 id="1-what-is-automation-testing">1) What is Automation testing?</h3><p></p></div></div>"""

    extract_element(state, reader)

    print(etree.tostring(state['element_dom']))
    print(etree.tostring(state['element']))

    # unique = CheckUniqunessInHTML(state['dom'])
    # generate_locator(state, unique)


    id = IdLocator()
    css = CssSelectorLocator()
    xpath = XPathLocator()

    strategies = [id, css, xpath]
    generate_locator(state, strategies)
