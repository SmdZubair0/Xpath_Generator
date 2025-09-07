from .CreateLocator import LocatorStrategy
from typing import List

class IdLocator(LocatorStrategy):
    def create(self, element, elememt_dom) -> dict[str, List]:

        loc : dict[str, List] = {
            'type' : 'id',
            'locators' : []
        }
        
        for id in element.attrib.get('id'):
            loc['locators'].append(
                {
                    'locators' : {
                        'id' : id,
                        'cssSelector' : f"#{id}",
                        'xpath' : f"//*[@{id}]"
                    }
                }
            )
        
        return loc