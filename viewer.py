from dataclasses import dataclass
import streamlit as st
import json
import numpy as np
import pandas as pd

# st.title("Title")
# st.header("Header")
# st.subheader("Subheader")

@st.cache
def load_data():
    tf = open("config/job_group.json", "r")
    load_json = json.load(tf)
    return load_json

job_group = load_data()

for i in job_group.items():
    st.subheader(i[0])
    for j in i[1]:
        st.write(j['title'])

    break


# 버튼
if st.button("click button"):
    st.write("Data Loading..")


# 체크박스    
checkbox_btn = st.checkbox('Checktbox Button')
if checkbox_btn:
    st.write('Great!')
