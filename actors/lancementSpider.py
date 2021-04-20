import os
from time import sleep

listNameFile = os.listdir('actors/spiders/filmographie/')


for name in listNameFile :
	com ='scrapy crawl actorSpider -a url=../filmographie/'+name+' -o ../resultats/'+name[:-4]+'.json'
	os.system(com)
	
