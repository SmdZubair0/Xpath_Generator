from generator import CreateLocator
from readers import ReadDOM
from typing import List

class GenerateLocator:
    def __init__(self,
                 strategy : List[CreateLocator],
                 element : ReadDOM,
                 )