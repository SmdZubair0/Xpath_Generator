import sys
from lxml import etree
from StyleXL import StyleXL

from Utils import (
    get_dom,
    Xpath_generator
)
from bs4 import BeautifulSoup
from pathlib import Path

url = input("Enter url : ")

soup = get_dom(url,timeout=35)
if soup is None:
    sys.exit(1000)

generator = Xpath_generator(soup.body)
generator.generate_xpath()


generator.get_file(Path(r"dummy.xlsx"))

st = StyleXL(Path(r"dummy.xlsx"))
st.color_header()
st.column_alignment()
st.border()
st.save_file(Path(r"dummy.xlsx"))

ele = input("Enter element to get xpath : ")
print(generator.get_xpath(BeautifulSoup(ele, 'html.parser').contents[0]))