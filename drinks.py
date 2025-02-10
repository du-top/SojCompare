import os
import re

from CodeParser import ByondParser
from Comparison import Comparison
from Comparison import ComparisonResult
from Comparison import Entity

class Drink(Entity):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.recipe = None
        self.description = ''
        self.strength = ''

    def to_string(self):
        return self.name

    def equal_to(self, other):
        if self.to_string() == other.to_string():
            return True

        return self.to_string().lower() == other.to_string().lower()

    def put_recipe(self, recipe):
        self.recipe = {}
        for match in re.findall("\"(.+?)\"\s=\s([0-9.]+)", recipe.properties["required_reagents"]):
            self.recipe[match[0]] = match[1]
        self.additional_info = 'Has Recipe'

class DrinksComparison(Comparison):
    def __init__(self):
        super().__init__()
        self.temp_dir = 'drinks'
        self.source_dir = 'code/modules/reagents/reagents'
        self.wiki_title = 'Guide_to_Drinks'     
        self.recipe_source_dir = 'code/modules/reagents/recipes'
        self.recipe_temp_dir = 'drink_recipes'
        self.canCreateOutput = True

    def parse_source(self):
        self.download()
        self.download(self.recipe_source_dir, self.recipe_temp_dir)

        all_classes = []

        for filename in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, filename)    
        
            if os.path.isfile(file_path):                  
                if any(filename == ignored_file for ignored_file in self.ignored_files):
                    self.verbose_message(f"Ignoring {filename}")
                    continue

                self.verbose_message(f"Processing file {filename}:")                
                file = open(file_path)
                code = file.read()
                parser = ByondParser()
                classes = parser.parse(code).classes
                all_classes.extend(classes)

        all_drinks = []
        relevant = {"datum/reagent/ethanol", "datum/reagent/drink"}

        for c in all_classes:
            if any(c.name.startswith(rel) for rel in relevant) == False:
                continue

            if "name" in c.properties:
                drink = Drink()
                drink.name = c.properties["name"].strip("'")
                drink.id = c.properties["id"].strip("'")

                if "strength" in c.properties:
                    drink.strength = c.properties["strength"]
                else:
                    drink.strength = '0'

                if drink.name == '':
                    continue # Without name it's not a real drink

                drink.description = c.properties["description"].strip("'")
                all_drinks.append(drink)

        recipe_files = { "drink_recipes\\recipes_food_drinks.dm", "drink_recipes\\alchemy.dm" }

        all_recipe_classes = []

        for recipe_file in recipe_files:
            if os.path.isfile(recipe_file):
                print("Processing file:", recipe_file)
                file = open(recipe_file)
                code = file.read()
                parser = ByondParser()
                all_recipe_classes.extend(parser.parse(code).classes)
        
        for recipe_class in all_recipe_classes:
            matching_drink = None
            if recipe_class.properties["result"] == "null":
                reaction_method = next((method for method in recipe_class.methods if method.name == "on_reaction"), None)               
            else:
                matching_chem = next((drink for drink in all_drinks if drink.id == recipe_class.properties["result"]), None)
            if matching_chem is None:
                continue

            matching_chem.put_recipe(recipe_class)
        
        return all_drinks

    def parse_wiki(self):
        parsed = self.get_wiki_content()

        all_wiki_drinks = []

        for section in parsed.sections:
            for table in section.tables:
                row_index = 0
                for row in table.data():          
                    row_index += 1
                    if row_index == 1:
                        continue

                    if len(row) > 2:
                        drink = Drink()
                        drink.name = row[1].strip("'")
                        all_wiki_drinks.append(drink)
                    
        return all_wiki_drinks

    def create_wiki_entry(self, drink):
        output = []
        output.append(f'!')
        output.append(f"|'''{drink.name}'''")
        output.append(f'|{self.createRecipe(drink.recipe)}')
        output.append(f'|{drink.strength}')
        output.append(f'|{drink.description}')
        output.append('|-')

        return "\n".join(output)

    def create_output(self, result):
        with open('drinks_output.txt', 'w', encoding='utf-8') as file:
            for entry in result.created_wiki_entries:
                file.write(entry)
                file.write('\n')

    def createRecipe(self, recipe):
        if recipe is None:
            return ''
        
        output = []
        for ingred in recipe:
            output.append(f"{recipe[ingred]} part{'s' if recipe[ingred] == 0 else ''} {ingred}")
        return ", ".join(output)

