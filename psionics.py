import os
import re

from CodeParser import ByondParser
from Comparison import Comparison
from Comparison import ComparisonResult
from Comparison import Entity

class Power (Entity):
    def __init__(self):
        super().__init__()
        self.category = ''
        self.name = ''
        self.desc = ''
        # self.source = ''

    def to_string(self):
        return self.name

    def equal_to(self, other):
        return self.name.lower() == other.name.lower()

class PsionicsComparison(Comparison):
    def __init__(self):
        super().__init__()
        self.temp_dir = 'psion_powers'
        self.source_dir = 'code/modules/psionics/psion_powers'
        self.wiki_title = 'Psionics'                

    def parse_source(self):
        self.download()

        all_procs = []

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
                procs = parser.parse(code).procs
                for proc in procs:
                    all_procs.append((proc, filename))
        
        all_powers = []
        for c in all_procs:
            if c[0].code == "":
                continue

            power = Power()

            power.category = c[1]

            name_match = re.search('set name = "(.*)"', c[0].code)
            if name_match is None:
                continue # Not a real power
            else:
                power.name = name_match[1]

            desc_match = re.search('set desc = "(.*)"', c[0].code)
            if desc_match is not None:
                power.desc = desc_match[1]
    
            if power.name != "":
                self.verbose_message(f'{power.name} ({c[0].name})')
            else:
                self.verbose_message(f'no name in {c[0].name}')

            all_powers.append(power)

        return all_powers
    
    def parse_wiki(self):
        parsed = self.get_wiki_content()

        all_wiki_powers = []
        for section in parsed.sections:
            if section.level != 3:
                continue # ignore the perks, which are on level 2

            for table in section.tables:
                row_index = 0
                for row in table.data():
                    row_index += 1

                    firstcell = table.cells(row_index-1,0)
                    if firstcell.is_header:
                        continue

                    if len(row) < 3:
                        continue

                    power = Power()
                    power.name = row[0]
                    power.desc = row[1]
                    #power.category = section.name
                    all_wiki_powers.append(power)

        return all_wiki_powers

    def create_wiki_entry(self, power):
        output = []
        output.append('|-')    
        output.append(f'|{power.name}')
        output.append(f'|{power.desc}')

        return "\n".join(output)




