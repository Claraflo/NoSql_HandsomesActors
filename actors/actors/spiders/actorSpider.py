from scrapy import Request, Spider
from bs4 import BeautifulSoup
import os

class SpiderReviewsAllocine(Spider):
	# Nom du spider
	name = "actorSpider"
	# URL de la page à scraper
	start_urls=[]
	file=''

	def __init__(self,**kwargs):
	
		self.file=os.path.abspath(kwargs.get('url'))

		f=open(self.file,'r')
		f.seek(0,0)

		lines= f.readlines()

		for line in lines:
			link=line.split(';')[2]
			link= 'https://www.imdb.com'+link
			self.start_urls.append(link)
		f.close()


	def start_requests(self):
		for url in self.start_urls : 
			yield Request(url=url, callback=self.parse_films)
 

	def parse_films(self, response):

		# Recuperation dans un objet soup
		soup = BeautifulSoup(response.text, 'html.parser')

		if soup:
			statMovie = {}
			f=open(self.file,'r')
			f.seek(0,0)
			movies=f.readlines()

		for movie in movies:
			movie= movie.split(';')
			if(str(response.url).find(movie[2].strip())!=-1):
				statMovie['film']=movie[1]
				statMovie['annee']=movie[0]
				break


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
			statMovie['genre']=genre

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

		statMovie['duree']=duree

		# Recuperation du real
		director = 'None'
		try:
			director = soup.find('div', 'credit_summary_item').text.split(':')[1].replace('\n', '')
		except:
			director = 'None'

		statMovie['director']=director

		# Recuperation de la note
		note = 'None'
		try:
			note = soup.find('span', {'itemprop': 'ratingValue'}).text
		except ValueError:
			note = 'None'

		statMovie['note']=note

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


		statMovie['budget']=budget
		statMovie['benef']=benef

		f.close()
		yield statMovie


         
        