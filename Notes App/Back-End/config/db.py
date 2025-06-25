from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  

db_url = os.getenv("DATABASE_URL")


conn = MongoClient(db_url)
