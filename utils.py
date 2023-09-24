from pymongo import MongoClient
def get_db_handle(db_name, host, port, username, password):

 client = MongoClient("mongodb://localhost: 27017/")
 db= client['shopping']
 return db, client