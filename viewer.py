from dataclasses import dataclass
import streamlit as st
import json
import numpy as np
import pandas as pd
import SessionState

session_state = SessionState.get(button_1=False)

# st.title("Title")
# st.header("Header")
# st.subheader("Subheader")

#@st.cache
def load_data():
    tf = open("config/job_group.json", "r")
    load_json = json.load(tf)
    return load_json

job_group = load_data()

def test_func():
    pass
    

for x, i in enumerate(job_group.items()):

    with st.form(key=str(x)):
        bool_new_data = False
        for ii in i[1]:
            if ii['status'] == 'wait':
                bool_new_data = True
                break

        if bool_new_data:
            # 회사명
            st.subheader(i[0])

            for y, j in enumerate(i[1]):
                
                col1, col2, col3, col4 = st.columns([1.8,0.2,0.2,0.2])
            
                # 채용공고명
                col1.write(j['title'])

                with col2:
                    if st.form_submit_button(label="SAVE", on_click=test_func):
                    #if st.form_submit_button(label="SAVE", on_click=test_func, key=str(x)+str(y)+('save')):
                        j['status'] = 'save'

                        tf = open('config/job_group.json', 'w')
                        json.dump(job_group, tf)
                        tf.close()
                        #st.success('SAVE')

                with col3:
                    if st.form_submit_button(label="PASS", on_click=test_func):
                    #if st.form_submit_button(label="PASS", on_click=test_func, key=str(x)+str(y)+('pass')):
                        j['status'] = 'pass'

                        tf = open('config/job_group.json', 'w')
                        json.dump(job_group, tf)
                        tf.close()
                    
                        #st.error("PASS")

                with col4:
                    #if st.form_submit_button(label="HOLD", on_click=test_func, key=str(x)+str(y)+('hold')):
                    if st.form_submit_button(label="HOLD", on_click=test_func):
                        pass
                        #st.info("HOLD")
    

    # if x > 10:
    #     break



