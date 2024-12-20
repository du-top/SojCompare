import os
import re
from CodeParser import ByondParser
from wikirequest import WikiRequest
from Comparison import Comparison
from Comparison import ComparisonResult
from Comparison import Entity

import wikitextparser as wtp

class Perk(Entity):
    def __init__(self, id:str = "", name:str="", desc:str="", source:str=""):
        super().__init__()
        self.id = id
        self.name = name
        self.desc = desc
        self.source = source

    def to_string(self):
        return self.name

    def equal_to(self, other):
        return self.name.lower() == other.name.lower()

class PerksComparison(Comparison):
    def __init__(self):
        super().__init__()
        self.temp_dir = 'perks'
        self.source_dir = 'code/datums/perks'
        self.wiki_title = 'Perks'
        self.ignored_files = {
            'perk.dm', # base class
            'cooldown.dm', # Not actually perks
            'imprinter_perks.dm' # admin-assigned (I think)
            }

    def parse_source(self):
        self.download()

        all_perks = []

        for filename in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, filename)    
        
            if os.path.isfile(file_path):                  
                if any(filename == ignored_file for ignored_file in self.ignored_files):
                    self.verbose_message(f"Ignoring {filename}")
                    continue

                self.verbose_message(f"Processing file {filename}:")                
                parser = StateParser()
                all_perks.extend(parser.parse(file_path))
        
        return all_perks

    def parse_wiki(self):
        parsed = self.get_wiki_content()

        wiki_perks = []
        for section in parsed.sections:    
            self.verbose_message(f"section {section.title} has {len(section.tables)} tables and {len(section.sections)} sections")
            if section.level != 3: # hack because I'll get the same table from sections level 1 and two, too
                continue

            row_index = 0
            for table in section.tables:
                for row in table.data():
                    row_index += 1

                    firstcell = table.cells(row_index-1,0)
                    if firstcell.is_header:
                        continue

                    if len(row) < 2:
                        continue

                    perk = Perk()
                    perk.name = row[0].strip("'")
                   
                    comment_match = re.search('<!--nameInCode:(.*?)-->', perk.name)
                    if comment_match is not None:
                        perk.name = comment_match.groups()[0]

                    if perk.name.find("'''") >= 0:
                        perk.name = perk.name[0:perk.name.index("'''")]

                    perk.desc = row[1].strip()
                    perk.source = section.title # bad
                    wiki_perks.append(perk)

        return wiki_perks

    def create_wiki_entry(self, perk):
        output = []
        output.append('|-')    
        output.append(f"|'''{perk.name}'''")
        output.append(f'|{perk.desc}')
        output.append(f'|{perk.source}')

        return "\n".join(output)

class Parser:
    def parse(self, path):
        all_perks = []
        return all_perks

class StateParser(Parser):

    def parse(self, path):
        all_perks = []
        file = open(path)
        code = file.read()
        parser = ByondParser()
        classes = parser.parse(code).classes
        
        for c in classes:
            if c.name == "":
                continue
        
            if not "name" in c.properties:
                continue

            perk = Perk(c.name)
            perk.source = path

            if "name" in c.properties and c.properties["name"]:
                perk.name = c.properties["name"]
            
            if "desc" in c.properties and c.properties["desc"]:
                perk.desc = c.properties["desc"]

            all_perks.append(perk)

        return all_perks