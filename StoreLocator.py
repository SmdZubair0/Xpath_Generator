from abc import ABC, abstractmethod
from pathlib import Path

class StoreLocator(ABC):
    @abstractmethod
    def save(filepath : Path):
        pass

class StoreJSON(StoreLocator):

    def save(filepath):
        pass

class StoreCSV(StoreLocator):
    def save(filepath):
        pass