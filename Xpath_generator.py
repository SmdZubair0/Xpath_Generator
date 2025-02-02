import sys
from Utils import (
    get_dom,
    Xpath_generator
)
from bs4 import BeautifulSoup
from pathlib import Path

url = input("Enter url : ")

soup = get_dom(url)
if soup is None:
    sys.exit(1000)

generator = Xpath_generator(soup.body)
generator.generate_xpath()

generator.get_csv(Path(r"dummy.csv"))