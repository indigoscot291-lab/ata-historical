import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import io
import concurrent.futures
from pymongo import MongoClient

@st.cache_resource
def get_mongo():
    uri = st.secrets["MONGO_URI"]
    return MongoClient(uri)
