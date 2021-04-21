import pandas as pd
from pymongo import MongoClient
import json
import os


client = MongoClient('127.0.0.1:27017')
db = client['projectActors']
col = db['movies']



print('nombre d\'insertions :',)