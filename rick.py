import requests
import re
import phrases


def find(url):
    source = str(requests.get(url).content).lower()
    allphrases = phrases.rickrolls
    return bool(re.findall("|".join(allphrases), source, re.MULTILINE))
