import streamlit as st
import pymongo
from pymongo import MongoClient
import traceback

print("\n=== DEBUG: STARTING ===")

# 0. Load URI safely
try:
    uri = st.secrets["MONGO_URI"]
    print("URI LOADED:", uri)
except Exception as e:
    print("ERROR: Could not load st.secrets['MONGO_URI']")
    print(e)
    traceback.print_exc()
    raise SystemExit("Stopping: MONGO_URI not loaded")

# 1. DNS / SRV resolution
print("\n=== DEBUG: DNS / SRV ===")
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    print("DNS OK: SRV resolved")
except Exception as e:
    print("DNS ERROR:", e)
    traceback.print_exc()

# 2. Cluster handshake (TLS, firewall, routing)
print("\n=== DEBUG: CLUSTER HANDSHAKE ===")
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    info = client.server_info()
    print("Handshake OK:", info)
except Exception as e:
    print("Handshake ERROR:", e)
    traceback.print_exc()

# 3. Authentication test
print("\n=== DEBUG: AUTHENTICATION ===")
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    print("PING:", client.admin.command("ping"))
except Exception as e:
    print("AUTH ERROR:", e)
    traceback.print_exc()

# 4. List databases
print("\n=== DEBUG: DATABASE LIST ===")
try:
    print("Databases:", client.list_database_names())
except Exception as e:
    print("DB LIST ERROR:", e)
    traceback.print_exc()

# 5. ATA database
print("\n=== DEBUG: ATA DB ===")
try:
    db = client["ATA"]
    print("Collections:", db.list_collection_names())
except Exception as e:
    print("ATA ERROR:", e)
    traceback.print_exc()

# 6. titles collection
print("\n=== DEBUG: TITLES COLLECTION ===")
try:
    titles = db["titles"]
    print("Count:", titles.count_documents({}))
except Exception as e:
    print("TITLES ERROR:", e)
    traceback.print_exc()
