from scrapy import Request, Spider
from bs4 import BeautifulSoup
import requests
import os



class SpiderReviewsAllocine(Spider):
	
	##Attribues de classe
	name = "actorSpider" # Nom du spider
	start_urls=[] # URL de la page à scraper
	file='' #nom de fichier contenant la filmographie de l'acteur


	##Constructeur
	def __init__(self,**kwargs):

		self.file=os.path.abspath(kwargs.get('url')) #fichier contenant la filmographie de l'acteur passé en argument (fichier lancementSpider.py)

		f=open(self.file,'r')
		f.seek(0,0) 

		lines= f.readlines()

		#Remplissage la liste start_url contenant l'ensemble des URL de chaque film de la filmographie de l'acteur.
		for line in lines:
			link=line.split(';')[2]
			link= 'https://www.imdb.com'+link
			self.start_urls.append(link)
		f.close()


	##Passe l'URL à l'engine
	def start_requests(self):
		for url in self.start_urls : 
			yield Request(url=url, callback=self.parse_films)
 

	##Recupere la page téléchargée du dowloader par le bien de l'engine pour la parser.
	def parse_films(self, response):

		
		# Recuperation dans un objet soup de la réponse HTML
		soup = BeautifulSoup(response.text, 'html.parser')

		#Creation du dictionnaire à retourner
		statMovie = {}

		if soup:
			
			f=open(self.file,'r')
			f.seek(0,0)
			
			movies=f.readlines()
			flagOpenFile = False

			#######################################
			#Recuperation du titre et de la date###
			#######################################

			for movie in movies:###
				movie= movie.split(';')
				if(str(response.url).find(movie[2].strip())!=-1):
					statMovie['title']=movie[1]
					statMovie['year']=movie[0]
					flagOpenFile = True
					break

			if not flagOpenFile :
				containName = soup.find("div",{'class':'titleBar'}).find("h1")
				statMovie['title'] = containName.contents[0]

				containDate = soup.find("div",{'class':'titleBar'}).find("h1").find("a")
				if containDate != None:
					statMovie['year'] = containDate.contents[0]
				else:
					statMovie['year'] = "None"


			##########################
			# recuperation du genre###
			##########################

			sectionGenre = soup.find_all('h4', 'inline')

			
			if (sectionGenre != None):
				for section in sectionGenre:
					if (section.text == 'Genres:'):
						sectionParent = section.parent
						sectionParent = sectionParent.find_all('a')
						genre = [i.text for i in sectionParent]
			else:
				genre = []
			
			statMovie['genre']=genre


			#############################
			# Recuperation de la duree###
			#############################

			sectionDuree = soup.find_all('h4', 'inline')
			runtime = 'None'

			if (sectionDuree != None):
				for section in sectionGenre:
					if (section.text == 'Runtime:'):
						sectionParent = section.parent
						sectionParent = sectionParent.find('time')
						runtime = sectionParent.text
						runtime = runtime.split()[0]
			else:
				runtime = 'None'

			statMovie['runtime']=runtime


			##############################################
			# Recuperation du realisateur et du casting###
			##############################################

			director = []
			casts = ''

			directorPage = "fullcredits#directors/" 
			writerPage = "fullcredits#writers/"

			sectionCredit = soup.find_all('h4', 'inline')

			if (sectionCredit != None):
				for section in sectionCredit:

					if (section.text == 'Director:')|(section.text == 'Directors:'):
						sectionParent = section.parent
						sectionParent = sectionParent.find_all('a')  

						if sectionParent[len(sectionParent)-1].get('href') == directorPage:
							sectionParent.pop(len(sectionParent)-1)
					
						director = [i.text for i in sectionParent]

			response = requests.get(str(response.url)+"fullcredits")

			castPage = BeautifulSoup(response.text,'html.parser')    
			castList = castPage.select("table.cast_list tr td")

			for cast in castList:
				if cast.get("class") is None:
					casts = casts + cast.text.replace("\n","").strip() + ','
			casts = casts[:-1]
			casting = [i for i in casts.split(',')]

			statMovie['director']= director
			statMovie['casting']= casting

			############################
			# Recuperation de la note###
			############################

			note = 'None'

			try:
				note = soup.find('span', {'itemprop': 'ratingValue'}).text
			except Exception:
				note = 'None'

			statMovie['score']= note


			#############################################
			# Recuperation  du budget, benefices et des pays###
			#############################################


			sectionBoxOffice = soup.find('div',{'id':'titleDetails'})
			sectionBoxOffice = sectionBoxOffice.find_all('div','txt-block') 
			budget = 'None'
			benefice = 'None'
			country = 'None'

			for info in sectionBoxOffice:
				if info.h4 != None :
					if info.h4.contents[0] == "Country:":
						country = info.a.contents[0]

					if info.h4.contents[0] == "Budget:":
						containBudget = info.text
						containBudget = containBudget[9:]
						splitBudget = containBudget.split("\n", 1)
						budget = splitBudget[0]

					if info.h4.contents[0] == "Cumulative Worldwide Gross:":
						containBenefice = info.text
						benefice = containBenefice[30:]

			statMovie['country']=country
			statMovie['budget']=budget
			statMovie['benefice']=benefice.replace(' ','')


			f.close()

		# dictionnaire : title,year,genre,runtime,director,casting,score,country,budget,benefice,cast
		# Fichier json dans dossier resultats
		yield statMovie

