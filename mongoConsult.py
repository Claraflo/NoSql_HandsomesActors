import pandas as pd
from pymongo import MongoClient
import json
import os


client = MongoClient('127.0.0.1:27017')
db = client['projectActors']
col = db['movies']

print('**********************')
print('Connexion a mongo')
print('Noms des bases presentes : '+', '.join(client.list_database_names()))
print('Projet : db : projectActors, collection : movies')
print('Stat db : ',db.command("dbstats"))
print('**********************\n')


#Affiche toute la base
#cursor = col.find({})
#for document in cursor:
#	print(document)


document = col.count_documents({})
print(document,'lignes sont enregistrees')

#document = col.aggregate([{"$group" : {"_id" : "$title"}}])

document = col.distinct("title") 
count = len(document)

print('Il y a '+str(count)+' films.')
#for cursor in document:
#	print(cursor)

res = col.find({'title':'Once Upon a Time In Hollywood'})

for i in res :
	print(i)