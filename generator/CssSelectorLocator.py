from .CreateLocator import LocatorStrategy
from lxml import etree
from typing import List

class DomExplorer:
    """
    ToDo: add this as a utils so that it can be used in xpath too
    """
    
    def __init__(self):
        pass

    def find_all_parents(self, element, element_dom):
        # Parent selectors
        parents = [element_dom] # since it is already a parent
        parents.append(self.find_parent(element, element_dom))
        
        # Reverse so top parent comes first
        parents = parents[::-1]

        return parents


    def find_parent(self, el, root):
        el_str = etree.tostring(el) 
        for i in root:  # iterate over child
            for j in i.iter():  # recursively search for the element in the child
                if etree.tostring(j) == el_str:   # searching using strings cause both are different objects (created seperately)
                    return i
        return None
    

    def get_siblings(parent, element):
        # since parent will always have atmost one  element before required element as per elmenet_dom
        for i in parent:
            if (etree.tostring(i) != etree.tostring(element)):
                return i
            break
        return None



class CssSelectorHelper:

    def __init__(self):
        self.selectors = set()
        self.dom_explorer = DomExplorer()

    def find_parent_locator(self, parent, ele_selector):
        """
            find selectors for element using its parent's locator
            - parent - parent element
            - ele_selector - elements css locators
        """
        direct_parent_selector = []
        direct_parent = self.get_basic_selectors(parent)

        # selectors using direct parents
        for i in direct_parent:
            for j in ele_selector:
                direct_parent_selector.append(f"{i} > {j}")
        
        return direct_parent_selector
    
    def find_sibling_locator(self, parent, ele_selector):
        """
            find selectors for element using its parent's locator
            - parent - parent element
            - ele_selector - elements css locators
        """
        direct_sibling = self.dom_explorer.get_siblings(parent)
        direct_sibling_locator = self.get_basic_selectors(direct_sibling)

        direct_sibling_selectors = []

        # select direct sibling locator
        for i in direct_sibling_locator:
            for j in ele_selector:
                direct_sibling_selectors.append(f"{i} + {j}")
        
        return direct_sibling_selectors

        
    def run(self, element, element_dom):

        parents = self.dom_explorer.find_all_parents(element, element_dom)

        # basic locatos specific to element
        ele_selector = self.get_basic_selectors(element)
        # locator using direct parent and element
        direct_parent_selector = self.find_parent_locator(parents[0], ele_selector)
        # locator usgin direct sibling of element
        direct_sibling_selector = self.find_sibling_locator(parents[0], ele_selector)
        # locator using indirect parent of element
        indirect_parent_selector = self.find_parent_locator(parents[1], direct_parent_selector)
        # locator using parent's sibling
        parent_sibling_selector = self.find_sibling_locator(parents[1], direct_parent_selector)
                
        self.selectors.update(ele_selector)
        self.selectors.update(direct_parent_selector)
        self.selectors.update(direct_sibling_selector)
        self.selectors.update(indirect_parent_selector)
        self.selectors.update(parent_sibling_selector)
        
        return self.selectors

    
    def get_basic_selectors(self, el):
        """
        Generate basic CSS selectors for an element:
        - id
        - class (single + combinations)
        - tag + class
        - attributes like name, type, aria-label, alt
        """
        selectors = []
        tag = el.tag

        # ID selector
        for id in (el.attrib.get('id') or "").split():
            selectors.append(f"{tag}#{id}")   # tag + id

        # Class selectors (single + combos)
        classes = (el.attrib.get('class') or "").split()

        # Single class
        for c in classes:
            selectors.append(f".{c}")
            selectors.append(f"{tag}.{c}")

        # Attribute selectors (common ones)
        for attr in ['name', 'type', 'value', 'placeholder', 'aria-label', 'alt', 'title', 'role']:
            if attr in el.attrib and el.attrib[attr].strip():
                selectors.append(f"[{attr}='{el.attrib[attr]}']")
                selectors.append(f"{tag}[{attr}='{el.attrib[attr]}']")

        return selectors



class CssSelectorLocator(LocatorStrategy):

    def __init__(self):
        self.generator = CssSelectorHelper()

    def create(self, element, element_dom) -> dict:
        """
            element: etree.Element (clicked element)
            element_dom: shallow etree tree containing element + 2 parents + siblings
            returns: set of possible CSS selectors
        """

        loc : dict[str, List] = {
            'type' : 'cssSelector',
            'locators' : []
        }

        locators = self.generator.run(element, element_dom)

        for i in locators:
            loc['locators'].append(i)

        return loc