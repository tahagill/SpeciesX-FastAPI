from motor.motor_asyncio import AsyncIOMotorClient

# --------------------------
# MongoDB Connection
# --------------------------
# Replace with your MongoDB connection string
MONGODB_URI = "mongodb+srv://tahagill99:N8FadUL9LvSu85dB@cluster0.cajih.mongodb.net/dummy_gene"

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)

# Select the database
db = client.dummy_gene

# --------------------------
# Collections
# --------------------------
# Reference to the 'dummy01' collection for genes
genes_collection = db.dummy01

# Reference to the 'dummy_users' collection for users
user_collection = db.dummy_users