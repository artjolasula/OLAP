<<<<<<< HEAD
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("data/sales.csv")
=======
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("data/sales.csv")
>>>>>>> 511d4035445f4c79cd56b4dec149601410293d6a
    return df