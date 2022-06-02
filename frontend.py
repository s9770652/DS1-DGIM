"""Provides an interface to analyse the correlation between mushroom odour and edibility."""

__author__ = "Zeno Adrian Weil"

import streamlit as st
import backend
from random import shuffle

ODOUR_ABBREVS = {
    'Almond': 'a', 'Anise': 'l', 'Creosote': 'c', 'Fishy': 'y', 'Foul': 'f',
    'Musty': 'm', 'None': 'n', 'Pungent': 'p', 'Spicy': 's'
}


# Configuration and header
st.set_page_config(page_title="DGIM", page_icon='\U0001F344')  # mushroom favicon

st.markdown('<style>p{text-align: justify;}</style>', unsafe_allow_html=True)

st.title("Topic 4: One-Hot Encoding and DGIM")
st.write("One-hot encoding denotes the technique of replacing a categorical \
attribute with *k* possible values by a binary *k*-ary tuple where the *i*-th \
element is 1 if and only if the attribute was set to the *i*-th value. \
The Datar-Gionis-Indyk-Motwani algorithm is a technique to estimate \
the number of ones in the last *N* bits of a binary string. \
This program demonstrates the DGIM algorithm on a data set of mushrooms. \
It estimates the number of edible and poisonous mushrooms for a chosen odour and \
compares it to the real count.")

# Options
odour = st.selectbox(
    "Please select an odour:",
    ["Almond", "Anise", "Creosote", "Fishy", "Foul", "Musty", "None", "Pungent", "Spicy"],
    6
)

N = st.select_slider("Please select a value for N:", [2**i for i in range(4, 12)], 256)

error_rate = st.slider(
    "Please select a maximum absolute value for the error rate of the DGIM algorithm:",
    min_value=1, max_value=100, value=50, step=1, format='%d%%'
)

col_s1, col_s2 = st.columns([8.25, 1])  # widen left column to 'justify' button on the right
randomise = col_s1.checkbox("Shuffle data", True)
col_s2.button("Rerun")

data = backend.read_data()
titles = ("Edible Mushrooms", "Poisonous Mushrooms")
for i in range(2):
    # Count/estimate occurrences
    if randomise:
        shuffle(data[i])
    data[i] = backend.isolate_column(data[i], ODOUR_ABBREVS[odour])
    real = backend.real_count(data[i], N)
    dgim, buckets = backend.dgim_count(data[i], N, error_rate/100)
    # Display results for poisonous mushrooms
    st.write("######", titles[i])
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Real count", real)
    col2.metric("Estimated count", dgim)
    if real == 0:  # avoids division by zero
        col3.metric("Error", "0.0%")
    else:
        col3.metric("Error", str(round(100*(dgim-real)/real, 2)) + "%")
    col4.metric("Number of buckets", buckets)
