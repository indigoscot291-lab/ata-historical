import streamlit as st
from pymongo import MongoClient
import pandas as pd

# ---------------------------------------------------------
#  CONNECT TO MONGODB
# ---------------------------------------------------------

@st.cache_resource
def get_mongo():
    uri = st.secrets["MONGO_URI"]
    return MongoClient(uri)

client = get_mongo()

# Your database + collection
db = client["ATA"]
titles = db["ATA-State-Titles-25-26"]


# ---------------------------------------------------------
#  CASE-INSENSITIVE SEARCH HELPERS
# ---------------------------------------------------------

def ci_exact(field: str, value: str):
    """Case-insensitive exact match."""
    return {
        field: {
            "$regex": f"^{value}$",
            "$options": "i"
        }
    }

def ci_contains(field: str, value: str):
    """Case-insensitive substring match."""
    return {
        field: {
            "$regex": value,
            "$options": "i"
        }
    }


# ---------------------------------------------------------
#  SEARCH FUNCTIONS (CASE-INSENSITIVE)
# ---------------------------------------------------------

def search_by_name(name: str):
    return list(titles.find(ci_exact("Name", name)))

def search_by_name_contains(text: str):
    return list(titles.find(ci_contains("Name", text)))

def search_by_town(town: str):
    return list(titles.find(ci_exact("Town", town)))

def search_by_state(state: str):
    return list(titles.find(ci_exact("State", state)))

def search_by_division(division: str):
    return list(titles.find(ci_exact("Division", division)))

def search_by_event(event: str):
    return list(titles.find(ci_contains("Events", event)))

def search_multi(name=None, town=None, state=None, division=None, event=None):
    query = {}

    if name:
        query.update(ci_contains("Name", name))

    if town:
        query.update(ci_contains("Town", town))

    if state:
        query.update(ci_exact("State", state))

    if division:
        query.update(ci_contains("Division", division))

    if event:
        query.update(ci_contains("Events", event))

    return list(titles.find(query))


# ---------------------------------------------------------
#  STREAMLIT DISPLAY HELPER
# ---------------------------------------------------------

def show_results(docs):
    if not docs:
        st.write("No results found.")
        return

    df = pd.DataFrame(docs)
    df = df.drop(columns=["_id"], errors="ignore")
    st.dataframe(df)


# ---------------------------------------------------------
#  STREAMLIT UI
# ---------------------------------------------------------

st.title("ATA MongoDB Search")

st.write("Search the ATA State Titles database (2025–2026).")

# Input field
name = st.text_input("Search by Name (case-insensitive)")

# Run search
if name:
    results = search_by_name_contains(name)
    show_results(results)


