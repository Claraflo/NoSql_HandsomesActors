import pandas as pd
from pymongo import MongoClient
import json
import os


client = MongoClient('127.0.0.1:27017')
db = client['projectActors']
col = db['movies']


listNameFile = os.listdir('resultats/')

for nameFile in listNameFile:

	f = open('resultats/'+nameFile,'r', encoding='utf-8')

	f.seek(0,0)
	lines = f.readlines()

	for line in lines:
		if line[0]!='[' and line!=']':
			line=line.strip()
			if line[-1]==',':
				line=line[:-1]

			insert = json.loads(line)
			col.insert_one(insert)



