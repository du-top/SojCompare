from chems import ChemsComparison
from comparePerks import PerksComparison
from psionics import PsionicsComparison

comparers = {
    'Psionics': PsionicsComparison(),
    'Perks': PerksComparison(),
    'Chems': ChemsComparison()
    }
results = {}

for key, comparer in comparers.items():
    results[key] = comparer.compare()

for key, result in results.items():
    print()
    print(key)
    print(f'Items defined in code, but not in wiki ({len(result.not_in_wiki_entries)}):')
    for wiki_item in result.not_in_wiki_entries:
        if wiki_item.additional_info != '':
            print(f'{wiki_item.to_string()}: {wiki_item.additional_info}')
        else:
            print(wiki_item.to_string())

    print()
    print(f'Items defined in wiki, but not in code ({len(result.not_in_code_entries)}):')
    for code_item in result.not_in_code_entries:
        if code_item.additional_info != '':
            print(f'{code_item.to_string()}: {code_item.additional_info}')
        else:
            print(code_item.to_string())
    print()

