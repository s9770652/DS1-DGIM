"""Provides an interface to analyse the correlation between mushroom odour and edibility."""

__author__ = "Zeno Adrian Weil"

import streamlit as st
import backend
from random import shuffle

ODOUR_ABBRVS = {
    'Almond': 'a', 'Anise': 'l', 'Creosote': 'c', 'Fishy': 'y', 'Foul': 'f',
    'Musty': 'm', 'None': 'n', 'Pungent': 'p', 'Spicy': 's'
}


# Configuration and header
st.set_page_config(page_title="DGIM", page_icon='\U0001F344')  # mushroom favicon
st.title("Topic 4: One-Hot Encoding and DGIM")
st.write("One-hot encoding denotes the technique of replacing a categorical \
attribute with *k* possible values by binary *k*-ary tuple where the *i*-th \
element is 1 if and only if the attribute was set to the *i*-th value. \
The Datar-Gionis-Indyk-Motwani algorithm is a technique to estimate \
the number of ones in the last *N* bits of a binary string. \
This program demonstrates the DGIM algorithm on a data set of mushrooms. \
It estimates the edible and poisonous mushrooms of a chosen odour and compares \
it to the real count.")

# Options
odour = st.selectbox(
    "Please select an odour:",
    ["Almond", "Anise", "Creosote", "Fishy", "Foul",
     "Musty", "None", "Pungent", "Spicy"],
    6
)

N = st.select_slider(
    "Please select a value for N:",
    [2**i for i in range(4, 12)],
    256
)

error_rate = st.slider(
    "Please select a maximum absolute value for the error rate of the DGIM algorithm:",
    min_value=1, max_value=100, value=50, step=1, format='%f%%'
)

col_s1, col_s2 = st.columns([8.25, 1])  # widen left column to 'justify' button on the right
randomise = col_s1.checkbox("Shuffle data", True)
col_s2.button("Rerun")

# Read odours and count/estimate occurrences
edible, poisonous = backend.read_data()
if randomise:
    shuffle(edible)
    shuffle(poisonous)
edible = backend.isolate_column(edible, ODOUR_ABBRVS[odour])
poisonous = backend.isolate_column(poisonous, ODOUR_ABBRVS[odour])
real_e = backend.real_count(edible, N)
dgim_e, buckets_e = backend.dgim_count(edible, N, error_rate/100)
real_p = backend.real_count(poisonous, N)
dgim_p, buckets_p = backend.dgim_count(poisonous, N, error_rate/100)

# Display results for edible mushrooms
st.write("###### Edible Mushrooms")
col_e1, col_e2, col_e3, col_e4 = st.columns(4)
col_e1.metric("Real count", real_e)
col_e2.metric("Estimated count", dgim_e)
if real_e == 0:  # avoids division by zero
    col_e3.metric("Error", "0.0%")
else:
    col_e3.metric("Error", str(round(100*(dgim_e-real_e)/real_e, 2)) + "%")
col_e4.metric("Number of buckets", buckets_e)

# Display results for poisonous mushrooms
st.write("###### Poisonous Mushrooms")
col_p1, col_p2, col_p3, col_p4 = st.columns(4)
col_p1.metric("Real count", real_p)
col_p2.metric("Estimated count", dgim_p)
if real_p == 0:
    col_p3.metric("Error", "0.0%")
else:
    col_p3.metric("Error", str(round(100*(dgim_p-real_p)/real_p, 2)) + "%")
col_p4.metric("Number of buckets", buckets_p)
