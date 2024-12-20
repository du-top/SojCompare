import re
from Comparison import Entity

class Chem(Entity):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.id = ""
        self.source = ""
        self.recipe = None
        self.metabolism = ""
        self.overdose = ""
        self.description = ""
        self.color = "#000000"

    def put_recipe(self, recipe):
        self.recipe = {}
        for match in re.findall("\"(.+?)\"\s=\s([0-9.]+)", recipe.properties["required_reagents"]):
            self.recipe[match[0]] = match[1]
        self.additional_info = 'Has Recipe'

    def to_string(self):
        return self.name

    def equal_to(self, other):
        return self.name.lower() == other.name.lower()

class Reaction(Entity):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.recipe = None

    def to_string(self):
        return self.name

    def equal_to(self, other):
        return self.name.lower() == other.name.lower()