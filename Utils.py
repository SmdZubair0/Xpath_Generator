import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def get_dom(
        url,
        header = None,
        parser = 'html.parser',
        timeout = 5
):
    soup = None
    try:
        response = requests.get(url,headers=header,
        timeout=timeout)
        response.raise_for_status()

        print("URL fetched successfully")

        soup = BeautifulSoup(response.content, parser)
    except:
        print("Provide proper URL / headers ...")
    
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
    
    def find_second_attribute(self, attrs, element):
        if len(attrs) > 1:
            conditions = []
            for attr, value in attrs.items():
                if attr != 'name':
                    if isinstance(value, list):
                        value = ' '.join(value)
                    conditions.append(f"@{attr} = '{value}'")
            return f"//{element.name}[{' and '.join(conditions)}]"
        else:
            text = element.get_text(strip=True)
            if text:
                return f"//{element.name}[contains(text(), '{text[:20]}')]"
            else:
                return self.generate_tree(element)

        
    def find_class_path(self, attrs, element):
        attribute_values = ' '.join(attrs['class'])
        if len(self.soup.find_all(class_=attribute_values)) == 1:
            return f"//{element.name}[contains(@class, '{attribute_values}')]"
        else:
            return self.find_second_attribute(attrs, element)
            
    
    def find_name_path(self, attrs, element):
        attribute_value = attrs['name']
        if len(self.soup.find_all(attrs={'name' : attribute_value})) == 1:
            return f"//{element.name}[@name = '{attribute_value}']"
        else:
            return self.find_second_attribute(attrs,element)


    def generate_path(self, element):
        attrs = element.attrs
        eid = self.ELEMENT_IDS[element]
        
        if 'id' in attrs.keys():  # If id is present simply take ID
            self.XPATHS[eid] = attrs['id']
            # self.XPATHS[eid] = f"//*[@id='{attrs['id']}']"
        
        elif 'name' in attrs.keys():
            self.XPATHS[eid] = self.find_name_path(attrs, element=element)        
                        
        elif 'class' in attrs.keys(): # If class is present check if itself can become locator
            self.XPATHS[eid] = self.find_class_path(attrs,element=element)
        else:
            self.XPATHS[eid] = self.generate_tree(element)
    
    def generate_xpath(self):
        for element in self.elements:
            self.generate_path(element)
        print("Xpaths Generated successfully")
    
    def get_all_xpaths(self):
        return self.XPATHS
    
    def get_xpath(self, tag):
        eid = self.ELEMENT_IDS[tag]
        if eid in self.XPATHS.keys():
            return self.XPATHS[id]
        return None
    
    def get_csv(self, filename):
        file = {
            "element_id" : [],
            "element" : [],
            "xpath" : []
        }
        for ele, eid in self.ELEMENT_IDS.items():
            file['element'].append(ele)
            file['element_id'].append(eid)
            file['xpath'].append(self.XPATHS[eid])

        df = pd.DataFrame(file)
        df.to_csv(filename, index=False)
