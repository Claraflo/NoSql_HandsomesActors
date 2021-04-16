import requests
from bs4 import BeautifulSoup
import random
import datetime


USER_AGENTS = [
    ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'),
    ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'),
    # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'),
    # chrome
    ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0')  # firefox
]


r = open('resultats.txt', 'a+')
f = open('C:/Users/clara/PycharmProjects/pythonProject2/filmo.txt', 'a+')

f.seek(0, 0)
lines = f.readlines()

for line in lines:
    movie = line.split(';')
    if movie[0] == 'None' or int(movie[0]) > int(datetime.datetime.now().year):
        continue

    url = 'https://www.imdb.com/' + movie[2]

    ind = random.randint(0, len(USER_AGENTS) - 1)
    # constitution de ma requet HTML
    headers = {'User-Agent': USER_AGENTS[ind]}
    response = requests.get(url, headers=headers, timeout=10)

    # Recuperation dans un objet soup
    soup = BeautifulSoup(response.text, 'html.parser')

    if soup:
        statMovie = []
        statMovie.append(movie[1])  # nom du film
        statMovie.append(movie[0])  # annee de sortie

        # recuperation du genre

        sectionGenre = soup.find_all('h4', 'inline')
        genre = 'None'
        if (sectionGenre != None):
            for section in sectionGenre:
                if (section.text == 'Genres:'):
                    sectionParent = section.parent
                    sectionParent = sectionParent.find_all('a')
                    genre = ",".join([i.text for i in sectionParent])
        else:
            genre = 'None'
        statMovie.append(genre)

        # Recuperation de la duree.
        duree = 'None'
        sectionDuree = soup.find_all('h4', 'inline')
        if (sectionDuree != None):
            for section in sectionGenre:
                if (section.text == 'Runtime:'):
                    sectionParent = section.parent
                    sectionParent = sectionParent.find('time')
                    duree = sectionParent.text
        else:
            duree = 'None'

        statMovie.append(duree)

        # Recuperation du real
        director = 'None'
        try:
            director = soup.find('div', 'credit_summary_item').text.split(':')[1].replace('\n', '')
        except:
            director = 'None'

        statMovie.append(director)

        # Recuperation de la note
        note = 'None'
        try:
            note = soup.find('span', {'itemprop': 'ratingValue'}).text
        except ValueError:
            note = 'None'

        statMovie.append(note)

        # Recuperation  du budget et des benefices
        budget = 'None'
        benef = 'None'
        sectionBoxOffice = soup.find('div', {'id': 'titleDetails'})
        if (sectionBoxOffice != None):
            sectionBoxOffice.find_all('div', 'txt-block')
            if (sectionBoxOffice != None):
                for section in sectionBoxOffice:
                    h4 = section.find('h4')
                    if (h4 != -1):
                        if (h4 != None and h4.text == 'Budget:'):
                            budget = "".join(section.text.replace('\n', '').split())
                        if (h4 != None and h4.text == 'Cumulative Worldwide Gross:'):
                            benef = "".join(section.text.replace('\n', '').split())
            else:
                budget = 'None'
                benef = 'None'
        else:
            budget = 'None'
            benef = 'None'

        statMovie.append(budget)
        statMovie.append(benef)

    res = ';'.join(statMovie) + '\n'
    r.write(res)

f.close()
r.close()
