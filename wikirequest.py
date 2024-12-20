import requests

class WikiRequest:
    def fetch_wiki_page_content(self, page_title):
        url = "https://sojourn13.space/w/api.php"  # Sojourns's API endpoint
        params = {
            "action": "parse",
            "page": page_title,
            "prop": "wikitext",
            "format": "json"
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        content = data["parse"]["wikitext"]["*"]

        return content