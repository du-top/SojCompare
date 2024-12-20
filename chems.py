import os
from CodeParser import ByondParser
from wikirequest import WikiRequest
import wikitextparser as wtp
from chem import Chem
from chem import Reaction
from wikicreator import Wikicreator
import re
from Comparison import Comparison

class ChemsComparison(Comparison):
    def __init__(self):
        super().__init__()
        self.temp_dir = 'chems'
        self.source_dir = 'code/modules/reagents/reagents'
        self.wiki_title = 'Guide_to_Chemistry'
        self.recipe_temp_dir = 'chem_recipes'
        self.recipe_source_dir = 'code/modules/reagents/recipes'

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
        
        all_code_chems = []
        relevant = {"datum/reagent/medicine", "datum/reagent/drug", "datum/reagent/stim", "datum/reagent/toxin", "datum/reagent/other", "datum/reagent/acid", "datum/reagent/nanites"}

        for c in all_classes:
            if any(c.name.startswith(rel) for rel in relevant) == False:
                continue

            if "name" in c.properties:
                chem = Chem()
                chem.name = c.properties["name"].strip("'")

                if chem.name == '':
                    continue # Without name it's not a real chem (probably base class)

                if "description" in c.properties:
                    chem.description = c.properties["description"].strip('"')
                if "color" in c.properties:
                    chem.color = c.properties["color"].strip('"')
                if "overdose" in c.properties:
                    chem.overdose = c.properties["overdose"]
                if "metabolism" in c.properties:
                    chem.metabolism = c.properties["metabolism"]
                chem.id = c.properties["id"].strip("'")
                chem.source = c.name
                all_code_chems.append(chem)

        recipe_files = { "chem_recipes\\recipes.dm", "chem_recipes\\recipes_nanites_paints.dm"}

        all_recipe_classes = []

        for recipe_file in recipe_files:
            if os.path.isfile(recipe_file):
                print("Processing file:", recipe_file)
                file = open(recipe_file)
                code = file.read()
                parser = ByondParser()
                all_recipe_classes.extend(parser.parse(code).classes)

        all_other_reactions = []

        for recipe_class in all_recipe_classes:
            matching_chem = None
            if recipe_class.properties["result"] == "null":
                reaction_method = next((method for method in recipe_class.methods if method.name == "on_reaction"), None)
                if reaction_method is not None:
                    all_other_reactions.append(recipe_class)
            else:
                matching_chem = next((chem for chem in all_code_chems if chem.id == recipe_class.properties["result"]), None)
            if matching_chem is None:
                continue

            matching_chem.put_recipe(recipe_class)

        for reaction in all_other_reactions:
            new_reaction = Reaction()
            new_reaction.name = reaction.name.split('/')[-1]
            recipe = {}
            for match in re.findall("\"(.+?)\"\s=\s([0-9.]+)", reaction.properties["required_reagents"]):
                recipe[match[0]] = match[1]

            new_reaction.recipe = recipe
            all_code_chems.append(new_reaction)
            
        return all_code_chems

    def parse_wiki(self):
        parsed = self.get_wiki_content()

        all_wiki_chems = []

        for section in parsed.sections:
            for table in section.tables:
                row_index = 0
                for row in table.data():          
                    row_index += 1
                    if row_index == 1:
                        continue

                    if len(row) == 5:
                        all_wiki_chems.append(self.create_medication(row))
                    elif len(row) == 3:
                        all_wiki_chems.append(self.create_reaction(row))

        return all_wiki_chems

    def create_medication(self, row):
        med = Chem()
        name = row[0]
        match = re.search("(.*?)<", name)
        if match is not None:
            med.name = match.groups()[0]

        return med
    
    def create_reaction(self, row):
        reaction = Reaction()
        name = row[0]

        comment_match = re.search('<!--nameInCode:(.*?)-->', name)
        if comment_match is not None:			
            reaction.name = comment_match.groups()[0]

            return reaction

        match = re.search("(.*?)<", name)
        if match is not None:
            reaction.name = match.groups()[0]
            return reaction

        reaction.name = name
        return reaction

