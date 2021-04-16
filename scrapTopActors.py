import requests
from bs4 import BeautifulSoup
import random


#Fichier permettant la recuperation des noms des acteurs d'un top IMBD

USER_AGENTS = [
    ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'),
    ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0')  # firefox
]

#Url de la liste des plus beaux acteurs à scrapper
url = "https://www.imdb.com/list/ls040780783/"

#constitution de ma requet HTML
ind = random.randint(0, len(USER_AGENTS) - 1)
headers = {'User-Agent': USER_AGENTS[ind]}
response = requests.get(url, headers=headers, timeout = 10)

#Recupération des résultats dans un objet soup.
soup = BeautifulSoup(response.text,'html.parser')

#Isolation de la liste des elements HTML contenant le nom des acteurs.
actors = soup.find_all('h3','lister-item-header')

#Création d'un fichier de sauvegarde
f = open('listeNomsActeurs.txt','w')

#Boucle pour stocker les noms dans un fichier
for actor in actors :
    name = actor.find('a').text
    f.write(name)

#Fermeture du fichier

f.close()