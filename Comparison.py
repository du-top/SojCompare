import os
from typing import List
from githubdownload import GithubDownload
from wikirequest import WikiRequest
import wikitextparser as wtp

class ComparisonResult:
    def __init__(self):
        self.all_code_entries: List[Entity] = []
        self.all_wiki_entries: List[Entity] = []
        self.not_in_wiki_entries: List[Entity] = []
        self.not_in_code_entries: List[Entity] = []
        self.created_wiki_entries: List[str] = []

class Comparison:
    def __init__(self):
        self.verbose = True
        self.temp_dir = ''
        self.source_dir = ''
        self.wiki_title = ''
        self.ignored_files = []
        self.github_token = self.get_github_token()
        self.canCreateOutput = False

    def get_github_token(self):
        path = 'githubtoken'
        if os.path.exists(path) and os.path.isfile(path):
            file = open(path)
            return file.read()
        else:
            return None

    def compare(self):
        return_value = ComparisonResult() 
        return_value.all_code_entries = self.parse_source()
        return_value.all_wiki_entries = self.parse_wiki()

        for code_entry in return_value.all_code_entries:
            if any(code_entry.equal_to(wiki_entry) for wiki_entry in return_value.all_wiki_entries) == False:
                created_entry = self.create_wiki_entry(code_entry)
                if created_entry is not None:
                    return_value.created_wiki_entries.append(created_entry)
                return_value.not_in_wiki_entries.append(code_entry)

        for wiki_entry in return_value.all_wiki_entries:
            if any(wiki_entry.equal_to(code_entry) for code_entry in return_value.all_code_entries) == False:
                return_value.not_in_code_entries.append(wiki_entry)

        return return_value

    def download(self, source_dir = None, dir = None):
        if dir is None:
            dir = self.temp_dir

        if source_dir is None:
            source_dir = self.source_dir

        if os.path.exists(dir):
            self.verbose_message(f"Directory {dir} exists, no download.")
        else:
            downloader = GithubDownload(self.github_token)
            downloader.download_directory_from_github('sojourn-13', 'sojourn-station', 'master', source_dir, dir)

    def parse_source(self):
        return []

    def parse_wiki(self):
        return []

    def get_wiki_content(self):
        request = WikiRequest()
        wiki_content = request.fetch_wiki_page_content(self.wiki_title)

        return wtp.parse(wiki_content)

    def create_wiki_entry(self, power):
        return ''

    def verbose_message(self, message):
        if self.verbose == False:
            return

        print(message)

    def create_output(self, result):
        return

class Entity:
    def __init__(self):
        self.additional_info = ''

    def to_string(self):
        return ''

    def equal_to(self, other):
        return self.to_string() == other.to_string()