from motor.motor_asyncio import AsyncIOMotorClient

Mongo_URI = "mongodb+srv://tahagill99:N8FadUL9LvSu85dB@cluster0.cajih.mongodb.net/dummy_gene"
client = AsyncIOMotorClient(Mongo_URI)
db = client.dummy_gene

genes_collection = db.dummy01
user_collection = db.dummy_users
