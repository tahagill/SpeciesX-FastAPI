from pymongo import MongoClient
from bson.objectid import ObjectId

# --------------------------
# MongoDB Connection
# --------------------------
# Replace with your MongoDB connection string
MONGODB_URI = "mongodb+srv://tahagill99:N8FadUL9LvSu85dB@cluster0.cajih.mongodb.net/dummy_gene"

# Initialize MongoDB client
client = MongoClient(MONGODB_URI)

# Select the database and collection
db = client['dummy_gene']
collection = db['dummy01']

# --------------------------
# Additional Data to Insert
# --------------------------
# List of additional entries for the MongoDB collection
additional_data = [
    {
        "_id": ObjectId("670cf1a52ec30dff7613614a"),
        "species_name": "Homo sapiens",
        "dna_sequence": "AGCTAGCTAGCTAGCTAGCTAGGT",
        "description": "Human genome segment"
    },
    {
        "_id": ObjectId("670cf1a52ec30dff7613614b"),
        "species_name": "Canis lupus familiaris",
        "dna_sequence": "CGTACGTAGCTAGTAGCTAGCTA",
        "description": "Dog genome segment"
    },
    {
        "_id": ObjectId("670cf1a52ec30dff7613614c"),
        "species_name": "Felis catus",
        "dna_sequence": "TACGATCGATCGATCGATCGATG",
        "description": "Cat genome segment"
    },
    {
        "_id": ObjectId("670cf1a52ec30dff7613614d"),
        "species_name": "Gallus gallus",
        "dna_sequence": "AGCTCGTAGCTAGCTAGCTCGA",
        "description": "Chicken genome segment"
    },
    {
        "_id": ObjectId("670cf1a52ec30dff7613614e"),
        "species_name": "Bos taurus",
        "dna_sequence": "CGTAGCTAGCATCGTACGTAGCA",
        "description": "Cow genome segment"
    },
    {
        "_id": ObjectId("670cf1a52ec30dff7613614f"),
        "species_name": "Ovis aries",
        "dna_sequence": "TAGCTAGCTAGCTGACGTCGTA",
        "description": "Sheep genome segment"
    },
    {
        "_id": ObjectId("670cf1a52ec30dff76136150"),
        "species_name": "Sus scrofa",
        "dna_sequence": "GCTAGCTAGCATGCTAGCTAGC",
        "description": "Pig genome segment"
    },
    {
        "_id": ObjectId("670cf1a52ec30dff76136151"),
        "species_name": "Equus ferus caballus",
        "dna_sequence": "AGCTAGCTAGCTACGTACGCTA",
        "description": "Horse genome segment"
    },
    {
        "_id": ObjectId("670cf1a52ec30dff76136152"),
        "species_name": "Rattus norvegicus",
        "dna_sequence": "TACGTACGTAGCTAGCTAGCTA",
        "description": "Rat genome segment"
    },
    {
        "_id": ObjectId("670cf1a52ec30dff76136153"),
        "species_name": "Mus musculus domesticus",
        "dna_sequence": "GGTACGTAGCTAGGCTAGCGTA",
        "description": "Domestic mouse genome segment"
    }
]

# --------------------------
# Insert Data into MongoDB
# --------------------------
# Insert the additional data into the collection
try:
    result = collection.insert_many(additional_data)
    print("Data inserted successfully! Inserted IDs:", result.inserted_ids)
except Exception as e:
    print(f"Error inserting data: {e}")

# --------------------------
# Close MongoDB Connection
# --------------------------
# Close the MongoDB client connection
client.close()