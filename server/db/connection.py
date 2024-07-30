from dotenv import load_dotenv
import os

from .database import MongoDB

load_dotenv()
DB_URI = os.getenv('DB_URI')
DB_NAME = os.getenv('DB_NAME')

def get_mongo_db():
    """
    Creates and returns the MongoDB object

    Returns
    --------
    
        MongoDB object
    """
    db = MongoDB(DB_URI, DB_NAME)
    return db
