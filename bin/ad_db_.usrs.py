from pymongo import MongoClient

# --------------------------
# MongoDB Connection
# --------------------------
# Replace with your MongoDB connection string
MONGODB_URI = "mongodb+srv://tahagill99:N8FadUL9LvSu85dB@cluster0.cajih.mongodb.net/dummy_gene"

# Initialize MongoDB client
client = MongoClient(MONGODB_URI)

# Select the database and collection
db = client['dummy_gene']
collection = db['dummy_users']

# --------------------------
# Fake User Data
# --------------------------
# List of fake user data (without email)
fake_users_db = [
    {
        "username": "john_doe",
        "full_name": "John Doe",
        "disabled": False,  # Corrected to Python's False
        "hashed_password": "$2b$12$C6eW/6U4GxL0Oix0H.Xe/OUV1B1Z75jZcrxozgUM9KiT8wA9dVi9K"  # bcrypt hashed password
    },
    {
        "username": "jane_smith",
        "full_name": "Jane Smith",
        "disabled": True,  # Corrected to Python's True
        "hashed_password": "$2b$12$C6eW/6U4GxL0Oix0H.Xe/OUV1B1Z75jZcrxozgUM9KiT8wA9dVi9K"
    },
    {
        "username": "alice_wonder",
        "full_name": "Alice Wonderland",
        "disabled": False,  # Corrected to Python's False
        "hashed_password": "$2b$12$C6eW/6U4GxL0Oix0H.Xe/OUV1B1Z75jZcrxozgUM9KiT8wA9dVi9K"
    }
]

# --------------------------
# Insert Data into MongoDB
# --------------------------
# Insert the fake user data into the collection
try:
    result = collection.insert_many(fake_users_db)
    print("Data inserted successfully! Inserted IDs:", result.inserted_ids)
except Exception as e:
    print(f"Error inserting data: {e}")

# --------------------------
# Close MongoDB Connection
# --------------------------
# Close the MongoDB client connection
client.close()