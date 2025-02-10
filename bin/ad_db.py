from pymongo import MongoClient
from bson.objectid import ObjectId

# Replace 'your_mongodb_uri' with your actual MongoDB URI
client = MongoClient('mongodb+srv://tahagill99:N8FadUL9LvSu85dB@cluster0.cajih.mongodb.net/dummy_gene')

# Replace 'your_database_name' and 'your_collection_name' with your actual database and collection names
db = client['dummy_gene']
collection = db['dummy01']

# Generate 10 additional entries for the MongoDB collection with the specified fields.
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

# Insert the additional data into the collection
result = collection.insert_many(additional_data)

# Print the IDs of the inserted documents
print("Inserted document IDs:", result.inserted_ids)

# Close the MongoDB connection
client.close()
