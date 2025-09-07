from .CreateLocator import LocatorStrategy

class XPathLocator(LocatorStrategy):
    def create(self, locator: str) -> dict:
        return {"locator": locator, "type": "xpath"}