# About
This project compares the source code of the Sojourn-13 project 
(https://github.com/sojourn-13/sojourn-station) with its Wiki 
(https://sojourn13.space/wiki/Main_Page) in certain topics, to make sure 
that the documentation there is up to date. This comparison 
consists of

- Perks
- Chemicals
- Psionic Powers
- Drinks

After the comparison, it shows what items exist in code, but 
not in the wiki, and what items exist in the wiki, but aren't
in the code (anymore?).

To achieve this, certain parts of the sojourn-13 source code
are downloaded from github and parsed. Then certain wiki pages 
are downloaded and also parsed. The results are then examined 
and compared.

# Requirements
- Python
- PyGithub (https://pygithub.readthedocs.io/), ```pip install pygithub```
- Requests (https://pypi.org/project/requests/), ```pip install requests```
- WikiTextParser (https://pypi.org/project/wikitextparser), ```pip install wikitextparser```

# Usage
Call ```CodeWikiComparison.py```

# Github token
To speed up the download from the source files from github, 
a Github token can be placed in a text file named "githubtoken"
and placed in the directory next to the CodeWikiComparison.py
file.

# Limitations
The project is the first Python project by the author, expect it 
to be _bad_. Especially the parser of the code files is everything
but universal. It worked for the certain set of files, but could 
trip over any (Dreammaker) language specific detail. It's bad. It
works right now, but it's bad. Baaad.

Changes in the wiki articles could cause the project to seize
functioning. This is especially the case when the articles are 
moved or renamed, but restructurings in them could be too much 
as well.

The project needs permission to create files and subdirectories
in the directory in which it runs in.

# Implementation
The main file ```CodeWikiComparison.py``` initializes and calls different implementations of the ```Comparison``` class.
They all compare the source code with a wiki page. Some provide more functions as that.

## Psionics
Creates and compares instances of the ```Power``` class.

## Perks
Creates and compares instances of the ```Perk``` class.

## Chems
Creates and compares instances of the ```Chem``` class.
When the code is analyzed, another part of the code is downloaded and analyzed. That part contains the recipes to create chemicals.
Only the ones with a recipe are relevant for the wiki. A text file with chemicals with recipe that are not defined in the wiki will
be output to the file chems_output.txt in the correct wiki format.

## Drinks
Creates and compares instances of the ```Drink``` class.
When the code is analyzed, another part of the code is downloaded and anlyzed. That part contains the recipes to create drinks.
A text file with drinks that are not defined in the wiki will be output to the file drinks_output.txt, in the correct wiki format,
although some columns of the wiki tables won't be used (strength in non-alocholic drinks, some descriptions).

# Planned features
There were first steps to create wiki table entries for missing
entities, but it's not included yet.

