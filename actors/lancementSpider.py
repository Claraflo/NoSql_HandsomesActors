import os
from time import sleep

listNameFile = os.listdir('actors/spiders/filmographie/')


for name in listNameFile :
	com ='scrapy crawl actorSpider -a url=actors/spiders/filmographie/'+name+' -o actors/spiders/resultats/'+name[:-4]+'.json'
	os.system(com)
	
