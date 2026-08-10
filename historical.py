import pymongo
from pymongo import MongoClient
import traceback

uri = st.secrets["MONGO_URI"]

print("\n=== DEBUG: RAW URI ===")
print(uri)

# 1. Test DNS / SRV resolution
print("\n=== DEBUG: DNS / SRV ===")
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    print("DNS OK: SRV resolved")
except Exception as e:
    print("DNS ERROR:", e)
    traceback.print_exc()

# 2. Test cluster handshake (no auth yet)
print("\n=== DEBUG: CLUSTER HANDSHAKE ===")
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    print("Handshake OK:", client.server_info())
except Exception as e:
    print("Handshake ERROR:", e)
    traceback.print_exc()

# 3. Test authentication explicitly
print("\n=== DEBUG: AUTHENTICATION ===")
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    print("PING:", client.admin.command("ping"))
except Exception as e:
    print("AUTH ERROR:", e)
    traceback.print_exc()

# 4. Test database existence
print("\n=== DEBUG: DATABASE LIST ===")
try:
    client = MongoClient(uri)
    print("Databases:", client.list_database_names())
except Exception as e:
    print("DB LIST ERROR:", e)
    traceback.print_exc()

# 5. Test ATA database existence
print("\n=== DEBUG: ATA DB ===")
try:
    db = client["ATA"]
    print("Collections:", db.list_collection_names())
except Exception as e:
    print("ATA ERROR:", e)
    traceback.print_exc()

# 6. Test titles collection existence
print("\n=== DEBUG: TITLES COLLECTION ===")
try:
    titles = db["titles"]
    print("Count:", titles.count_documents({}))
except Exception as e:
    print("TITLES ERROR:", e)
    traceback.print_exc()


