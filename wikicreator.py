from chem import Chem
import re

class Wikicreator:
    def __init__(self):
        self.chems = []

    def createRecipeEntry(self, chem: Chem):
        output = []
        output.append(f'!style=\'background-color:#B452CD;\'|{chem.name}<span id="{chem.name}" style="color:{chem.color};background-color:white">▮</span>')
        output.append(f'|{self.createRecipe(chem.recipe)}')
        output.append(f'|{chem.description}')
        output.append(f'|{chem.metabolism}')
        output.append(f'|{chem.overdose}')
        output.append('|-')

        return "\n".join(output)

    def createRecipe(self, recipe):
        if recipe is None:
            return ''
        
        output = []
        for ingred in recipe:
            output.append(f"{recipe[ingred]} part{'s' if recipe[ingred] == 0 else ''} {self.getchemname(ingred)}")
        return "<br>".join(output)

    def getchemname(self, name):
        result = next((chem for chem in self.chems if chem.id == name), None)
        if result is None:
            return name.capitalize()
        else:
            return f"[[#{result.name}|{result.name}]]"
