import requests
from bs4 import BeautifulSoup
import time

def get_dom(
        url,
        header = None,
        parser = 'html.parser'
):
    soup = None
    try:
        response = requests.get(url,headers=header)
        time.sleep(3)
    except:
        print("Provide proper URL / headers ...")

    if response and response.status_code == 200:
        soup = BeautifulSoup(response.content, parser)
        print("URL fetched successfully")
    else:
        print("Unable to fetch this url")
    
    return soup




class Xpath_generator():
    def __init__(self, soup):
        self.ELEMENT_IDS = {}
        self.XPATHS = {}
        self.soup = soup
        self.elements = self.get_elements(soup)
        self.generate_ids(self.elements)

    def get_elements(self,soup):
        return soup.find_all(True)
    
    def generate_ids(self, elements):
        id = 1
        for element in elements:
            self.ELEMENT_IDS[element] = id
            id += 1

    def generate_tree(self, element):
        if element.parent in self.ELEMENT_IDS.keys():
            if self.XPATHS[self.ELEMENT_IDS[element.parent]][0] != '/':
                return f"//{element.parent.name}[@id = '{element.parent.get('id')}']/{element.name}"
            return f"{self.XPATHS[self.ELEMENT_IDS[element.parent]]}/{element.name}"
        else:
            return f"//{element.name}"
        
    def find_class_path(self, attrs, element):
        attribute_values = attrs['class'][:3]
        if len(self.soup.find_all(attrs={'class' : attribute_values})) == 1:
            return f"//{element.name}[contains(@class, '{' '.join(attribute_values)}')]"
        else:
            if len(attrs) > 1:
                for attr in attrs.keys():
                    if attr != 'class':
                        attr_val = attrs[attr]
                        return f"//{element.name}[contains(@class, '{' '.join(attribute_values)}') and @{attr} = '{attr_val}']"
                        break
            else:
                text = element.find(text=True, recursive=False)
                if text and len(text) > 0:
                    return f"//{element.name}[contains(@class, '{' '.join(attribute_values)}') and contains(text(), '{text[:10]}')]"
                else:
                    return self.generate_tree(element)
    
    def find_name_path(self, attrs, element):
        attribute_value = attrs['name']
        if len(self.soup.find_all(attrs={'name' : attribute_value})) == 1:
            return f"//{element.name}[@name = '{attribute_value}')]"
        else:
            if len(attrs) > 1:
                for attr in attrs.keys():
                    if attr != 'name':
                        attr_val = attrs[attr]
                        if attr == 'class':
                            attr_val = " ".join(attr_val[:3])
                            return f"//{element.name}[@name = '{attribute_value}' and contains(@class, '{attr_val}')"
                        return f"//{element.name}[@name = '{attribute_value}' and @{attr} = '{attr_val}']"
                        break
            else:
                text = element.find(text=True, recursive=False)
                if text and len(text) > 0:
                    return f"//{element.name}[@name = '{attribute_value}') and contains(text(), '{text[:10]}')]"
                else:
                    return self.generate_tree(element)


    def generate_path(self, element):
        attrs = element.attrs
        eid = self.ELEMENT_IDS[element]
        
        if 'id' in attrs.keys():  # If id is present simply take ID
            self.XPATHS[eid] = attrs['id']
        
        elif 'name' in attrs.keys():
            self.XPATHS[eid] = self.find_name_path(attrs, element=element)        
                        
        elif 'class' in attrs.keys(): # If class is present check if itself can become locator
            self.XPATHS[eid] = self.find_class_path(attrs,element=element)
        else:
            self.XPATHS[eid] = self.generate_tree(element)
    
    def generate_xpath(self):
        for element in self.elements:
            self.generate_path(element)
        return self.XPATHS

