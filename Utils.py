import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree

def get_dom(
        url,
        header = None,
        parser = 'html.parser',
        timeout = 5
):
    """
        get_dom()
        params :
            url : url of the website you want to fetch
            header : pass headers if you want any, by default None
            parser:  type of parser you want to use, by default 'html.parser'
            timeout : maximum seconds to wait for the response, by default 5
        output:
            returns DOM of the webpage as an BeautifulSoup object.
    """
    soup = None
    try:
        response = requests.get(
            url,
            headers=header,
            timeout=timeout
        )                                             # to get response from the given url
        response.raise_for_status()                   # raise exception if failed to get response

        print("URL fetched successfully")

        soup = BeautifulSoup(response.content, parser)  # generate soup object for the response content
    except:
        print("Provide proper URL / headers ...")
    
    return soup                                         # return soup




class Xpath_generator():
    """
        Xpath_generator() - class
        This class is to generate xpaths for all the elements present in the given beautifulSoup object.
        
        Methods:
            constructor : takes soup object as parameter and initialize required members
            get_elements: returns a list of all elements in the soup object
            generate_ids: generates unique id for each element as a key-value pair.
            check_uniqueness: return true if the path generated is unique.
            generate_optimal_path: generate path using indexed approach
            generate_tree: generate path using parent elements
            find_second_attribute: generate path using combination of attributes
            find_class_path: generate path using class attribute
            find_name_path: generate path using name attribute
            generate_path: for each element select the method to generate optimal path
            generate_xpath: generate xpath for each element by iterating over them
            get_all_xpaths: return dictionary containing all xpaths
            get_xpath: returns xpath for the given tag
            get_file : stores the output in a file at given destination.
    """
    def __init__(self, soup):
        """
            Constructor of class Xpath_generator
            params:
                soup : BeautifulSoup object having DOM of the given page
            output:
                None
        """
        self.ELEMENT_IDS = {}  # store unique IDs for all elements
        self.XPATHS = {}       # store unique Xpaths for all elements
        self.soup = soup       # the soup object received as parameter
        self.tree = etree.HTML(str(soup))   # stores XML parse tree for the given soup
        self.elements = self.get_elements()  # store all elements in the form of list
        self.generate_ids()  # generate unique IDs fpr all elements

    def get_elements(self):
        """
            params:
                None
            output:
                list of all elements
        """
        return self.soup.find_all(True)
    
    def generate_ids(self):
        """
            params:
                None
            output:
                None
        """
        id = 1
        for element in self.elements:
            self.ELEMENT_IDS[element] = id
            id += 1

    def check_uniqueness(self, xpath):
        """
            params:
                xpath : xpath generated
            output:
                True : if xpath is unique
                False : otherwise
        """
        if self.tree.xpath(f"count({xpath})") == 1:
            return True
        return False
    
    def generate_optimal_path(self, element):
        """
            params:
                element : element for which the xpath should be generated
            output:
                path : returns generated xpath
        """
        path = ""
        while element:
            siblings = self.soup.find_previous_siblings(element.name)
            ele_index = len(siblings) + 1 if siblings else 1

            path = f"//{element.name}[{ele_index}]" + path

            element = element.parent
            if not element.parent or element.parent.name == 'html':
                break
        
        return path
            

    def generate_tree(self, element):
        """
            params:
                element : element for which the xpath should be generated
            output:
                path : returns generated xpath
        """
        if element.parent in self.ELEMENT_IDS.keys() and self.ELEMENT_IDS[element.parent] in self.XPATHS.keys():
            path = None
            if self.XPATHS[self.ELEMENT_IDS[element.parent]][0] != '/':
                path = f"//{element.parent.name}[@id = '{element.parent.get('id')}']/{element.name}"
            path = f"{self.XPATHS[self.ELEMENT_IDS[element.parent]]}/{element.name}"
            if self.check_uniqueness(xpath=path):
                return path
            return self.generate_optimal_path(element)
        else:
            path = f"//{element.name}"
            if self.check_uniqueness(path):
                return path
            return self.generate_optimal_path(element)
    
    def find_second_attribute(self, attrs, element, first_attr):
        """
            params:
                attrs : dict of all attributes of the element
                element : element for which the xpath should be generated
                first_attr : the attribute which is already taken.
            output:
                path : returns generated xpath
        """
        if len(attrs) > 1:
            conditions = []
            for attr, value in attrs.items():
                if attr != first_attr:
                    if isinstance(value, list):
                        value = ' '.join(value)
                    conditions.append(f"contains(@{attr}, \"{value}\")")
            path = f"//{element.name}[{' and '.join(conditions)}]"

            if self.check_uniqueness(path):
                return path

        text = element.text
        if text:
            # path = f"//{element.name}[contains(text(), '{repr(text[:20])}')]"
            path = f"//{element.name}[contains(text(), "
            if "'" in text and '"' in text:
                path += "concat(" + ", ".join(f"'{part}'" if '"' in part else f'"{part}"' for part in text.split("'")) + "))]"
            elif "'" in text:
                path += f'"{text}")]'
            else:
                path += f"'{text}')]"
            if self.check_uniqueness(path):
                return path
        return self.generate_tree(element)

        
    def find_class_path(self, attrs, element):
        """
            params:
                attrs : dict of all attributes of that element
                element : element for which the xpath should be generated
            output:
                path : returns generated xpath
        """
        attribute_values = ' '.join(attrs['class'])
        if len(self.soup.find_all(class_=attribute_values)) == 1:
            return f"//{element.name}[contains(@class, '{attribute_values}')]"
        else:
            return self.find_second_attribute(attrs, element, "class")
            
    
    def find_name_path(self, attrs, element):
        """
            params:
                attrs : dict of all attributes of that element
                element : element for which the xpath should be generated
            output:
                path : returns generated xpath
        """
        attribute_value = attrs['name']
        if len(self.soup.find_all(attrs={'name' : attribute_value})) == 1:
            return f"//{element.name}[@name = '{attribute_value}']"
        else:
            return self.find_second_attribute(attrs,element,'name')


    def generate_path(self, element):
        """
            params:
                element : element for which the xpath should be generated
            output:
                path : returns generated xpath
        """
        attrs = {k: v for k, v in element.attrs.items() if ':' not in k}
        eid = self.ELEMENT_IDS[element]
        
        if 'id' in attrs.keys():  # If id is present simply take ID
            self.XPATHS[eid] = attrs['id']
            # self.XPATHS[eid] = f"//*[@id='{attrs['id']}']"
        
        elif 'name' in attrs.keys():
            self.XPATHS[eid] = self.find_name_path(attrs, element=element)        
                        
        elif 'class' in attrs.keys(): # If class is present check if itself can become locator
            self.XPATHS[eid] = self.find_class_path(attrs,element=element)
        
        elif element.text:
            text = element.text
            # xpath = f"//{element.name}[contains(text(), '{repr(element.text[:20])}')]"
            xpath = f"//{element.name}[contains(text(), "
            if "'" in text and '"' in text:
                xpath += "concat(" + ", ".join(f"'{part}'" if '"' in part else f'"{part}"' for part in text.split("'")) + "))]"
            elif "'" in text:
                xpath += f'"{text}")]'
            else:
                xpath += f"'{text}')]"
            if self.check_uniqueness(xpath):
                xpath = xpath
            else:
                self.XPATHS[eid] = self.generate_tree(element)
        
        else:
            self.XPATHS[eid] = self.generate_tree(element)
    
    def generate_xpath(self):
        """
            Iterate over each element and find xpath for it.
        """
        for element in self.elements:
            self.generate_path(element)
        print("Xpaths Generated successfully")
    
    def get_all_xpaths(self):
        """
            return all Xpaths
        """
        return self.XPATHS
    
    def get_xpath(self, tag):
        """
            params:
                tag : a beautiful soup object for which it should find XPath
            output:
                xpath : returns generated xpath
        """
        eid = self.ELEMENT_IDS[tag]
        if eid in self.XPATHS.keys():
            return self.XPATHS[eid]
        return None
    
    def get_file(self, filename):
        """
            params:
                filename : path of the file where the data should be stored
        """
        file = {
            "element_id" : [],
            "element" : [],
            "xpath" : []
        }
        for ele, eid in self.ELEMENT_IDS.items():
            file['element'].append(ele)
            file['element_id'].append(eid)
            file['xpath'].append(self.XPATHS[eid] if eid in self.XPATHS.keys() else pd.NA)

        df = pd.DataFrame(file)
        df.to_excel(filename, index=False)
