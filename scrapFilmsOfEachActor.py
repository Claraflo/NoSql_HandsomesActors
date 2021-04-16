from collections.abc import Iterable
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

def cleanDate(date):
    if(date.find('None')!=-1): return date
    for i in date :
        if not i.isdigit():
            date=date.replace(i,'')
    return date


# Ouverture du fichier contenant les noms des acteurs
flag = True
try:
    namesActors = open('listeNomsActeurs.txt', 'r')
except(IOError):
    print('fichier non ouvert')
    flag = False

if (flag == True):

    namesActors.seek(0,0)
    lines = namesActors.readlines()

    # configuration du navigateur
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options, executable_path="C:\\fireDriver\\chromedriver.exe")
    driver.implicitly_wait(30)
    print("driver init")

    count = 0
    for line in lines :

        line = line.strip().replace('\n','')


        # Appeler l’application web
        driver.get("http://www.qwant.fr")
        search_bar = driver.find_element_by_name('q')
        search_bar.clear()
        search=line+' IMBD'
        search_bar.send_keys(search)
        search_bar.send_keys(Keys.RETURN)
        print("recherche effectue")

        links = driver.find_elements_by_xpath("//a[@class='external Stack-module__VerticalStack___2NDle Stack-module__Spacexxs___3wU9G']")[:5]
        print(links)

        url=''
        for link in links:
            print(link)
            if link.text.find("IMDb")!=-1:
                url = link.text.split("\n")[1]
                break

        if url=='':
            continue

        print("J'arrive sur la page imdb")

        driver.get("https://www."+url)
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')

        actorSection = soup.find('div',{'id' : 'filmo-head-actor'})
        movies = actorSection.find_next_sibling('div')
        movies = movies.find_all('div')

        filmo = open('filmographie/'+line.replace(' ','_')+'.txt','w')

        for movie in movies :
            if isinstance(movie.get("class"),Iterable):
                if "".join(movie.get("class"))!='filmo-episodes':
                    if(movie.text.find("TV Series")==-1):
                        date = movie.find('span','year_column')
                        name = movie.find_all('a')
                        if(date!=None) :
                            dateDisplay = date.text[2:]
                            if(dateDisplay=='\n'):
                                dateDisplay= 'None '
                        else : dateDisplay = 'None '
                        if(name!=None and len(name)>0) :
                            nameDisplay = name[0].text
                        else : nameDisplay = 'None'
                        link= name[0]['href']
                        filmo.write(cleanDate(dateDisplay[:-1])+';'+nameDisplay+';'+link+'\n')
        count += 1
        print("J'ai fini de recuperer la liste de film. j'ai fait "+str(count)+" acteurs de la liste.")


        filmo.close()

    driver.quit()
    namesActors.close()
