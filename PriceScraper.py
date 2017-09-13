from bs4 import BeautifulSoup
from urllib.request import urlopen

def retrieveHTML(url):
    return BeautifulSoup(urlopen(url), 'html.parser')