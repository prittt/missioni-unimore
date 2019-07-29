import re
import requests
from bs4 import BeautifulSoup


def get_prezzo_carburante():
    # Set the URL you want to webscrape from
    url = 'https://dgsaie.mise.gov.it/prezzi_carburanti_settimanali.php?lang=it_IT'
    # Connect to the URL
    response = requests.get(url)
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")
    prezzo = soup.find('table', class_="table table-sm table-borderless mx-auto").findAll(
        'tr', class_="bg-light")[0].find('strong').text
    prezzo = re.sub('\.+', '', prezzo)
    prezzo = re.sub(',+', '.', prezzo)
    prezzo = float(prezzo) / 1000
    return prezzo
