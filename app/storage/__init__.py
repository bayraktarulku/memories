from pymongo import MongoClient
from config import DB_NAME
c = MongoClient()
db = c[DB_NAME]