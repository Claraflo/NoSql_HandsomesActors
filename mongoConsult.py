import pandas as pd
from pymongo import MongoClient
import json
import os
import pprint

#Connextion a la base
client = MongoClient('127.0.0.1:27017')
db = client['projectActors']
col = db['movies']

#Affichage des statistiques
print('**********************')
print('Connexion a mongo')
print('Noms des bases presentes : '+', '.join(client.list_database_names()))
print('Projet : db : projectActors, collection : movies')
print('Stat db : ',db.command("dbstats"))
print('**********************\n')


# Compte le nombre de colonnes enregistrees
document = col.count_documents({})
print(document,'colonnes sont enregistrees.')

# Affichage du nombre de films presents reellement en eliminant les doublons
document = col.distinct("title") 
count = len(document)
print('Il y a',count,'films presents.')


#Suppression des doublons
cursor = col.aggregate([
	{"$group" : {"_id" : "$title", "unique_ids": {"$addToSet": "$_id"},"count":{"$sum":1}}},
	{"$match": {"count": { "$gte": 2 }}}					
	])

response = []
for doc in cursor:
    del doc["unique_ids"][0]
    for id in doc["unique_ids"]:
        response.append(id)

col.delete_many({"_id": {"$in": response}})



