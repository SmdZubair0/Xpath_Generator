import sys
from Utils import (
    get_dom,
    Xpath_generator
)

url = input("Enter url : ")

soup = get_dom(url)
if soup is None:
    sys.exit(1000)

generator = Xpath_generator(soup.body)
print(generator.generate_xpath())