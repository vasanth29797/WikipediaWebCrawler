import urllib
import time
import requests
from bs4 import BeautifulSoup

search_history = ["https://en.wikipedia.org/wiki/Frankfurt"]
target_url = "https://en.wikipedia.org/wiki/Philosophy"

def find_first_url(current_url):
    response = requests.get(current_url)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.find(id = "mw-content-text").find(class_ = "mw-parser-output")

    relative_url = None

    for element in content_div.find_all("p", recursive = False):
        if element.find("a", recursive = False):
            relative_url = element.find("a", recursive = False).get("href")
            break

    if not relative_url:
        return

    first_url = urllib.parse.urljoin("https://en.wikipedia.org/", relative_url)
    return first_url

def continue_crawl(search_history, target_url, max_steps = 25):
    if search_history[-1] == target_url:
        print("The most recent article in the search_history is the target article.")
        return False
    elif len(search_history) > max_steps:
        print("The list is more than 25 urls long.")
        return False
    elif search_history[-1] in search_history[:-1]:
        print("The list has a cycle in it.")
        return False
    else:
        return True

while continue_crawl(search_history, target_url):
    current_url = search_history[-1]
    print(current_url)
    first_url = find_first_url(current_url)

    if not first_url:
        print("We've reached the article with no link. Aborting search...")
        break

    search_history.append(first_url)
    time.sleep(2)