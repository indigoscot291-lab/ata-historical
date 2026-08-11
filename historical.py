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
#  MULTI-FIELD SEARCH (Name, Town, State, Division)
# ---------------------------------------------------------

def search_multi(name=None, town=None, state=None, division=None):
    query = {}

    if name:
        query.update(ci_contains("Name", name))

    if town:
        query.update(ci_contains("Town", town))

    if state:
        query.update(ci_exact("State", state))

    if division:
        query.update(ci_contains("Division", division))

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
    st.dataframe(df, use_container_width=True)


# ---------------------------------------------------------
#  STREAMLIT UI — PRIMARY FIELD SELECTOR
# ---------------------------------------------------------

st.title("ATA MongoDB Search")
st.write("Search the ATA State Titles database (2025–2026).")

# User chooses the main search field
mode = st.radio(
    "Search by:",
    ["Town", "Name", "State", "Division"]
)

# Primary field input
primary_value = st.text_input(f"{mode} contains")

# Optional filters for the other three fields
optional_filters = {}
for field in ["Town", "Name", "State", "Division"]:
    if field != mode:
        optional_filters[field] = st.text_input(f"{field} contains (optional)")

# Run search
if st.button("Search"):
    results = search_multi(
        name = primary_value if mode == "Name" else optional_filters["Name"],
        town = primary_value if mode == "Town" else optional_filters["Town"],
        state = primary_value if mode == "State" else optional_filters["State"],
        division = primary_value if mode == "Division" else optional_filters["Division"]
    )
    show_results(results)
