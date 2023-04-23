### MongoDB Client ###

# Ejecución: mongosh > use local > show dbs ...
# Conexión: mongodb://localhost/ ó mongodb://localhost:27017/

from pymongo import MongoClient

# Conexión DB local
# db_client = MongoClient("mongodb://localhost:27017/").local

# Conexión DB Remota
# 1. Obtener Connection String : Mongo Atlas [GUI] > DataBase > Connect (Cluster) > Drivers > Add your connection string...
# 2.a. Conectarse a DB por terminal : mongosh "mongodb+srv://cluster0.sm9prhk.mongodb.net/<NOMBRE_DB>" --apiVersion 1 --username admin
# 2.b. Ver el estado de la DB en Mongo Atlas [GUI] : DataBase > Collections

connection_string = 'mongodb+srv://admin:admin123@cluster0.sm9prhk.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(connection_string)
db_client = client.test
users_collection = db_client.users
