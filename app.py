from support import get_states, get_district, get_full_data, filter_data
import streamlit as st
import os
from datetime import date as dt
state_id, state_names = get_states()
st.set_page_config(page_title="CoWin Checker", page_icon="favicon.ico")
st.title("CoWin Vaccine Availability Checker")
st.write("Made by Aditya Rangarajan")
state_name = st.sidebar.selectbox(label= "Choose a state : ", options = ["Choose an option"]+ state_names)
try:
    state_id = state_id[state_names.index(state_name)]
except :
    state_id = None
if state_id != None:
    district_id, district_names = get_district(state_id)
    district_name = st.sidebar.selectbox(label= "Choose a district : ", options = ["Choose an option"]+ district_names)
    try:
        district_id = district_id[district_names.index(district_name)]
    except :
        district_id = None
    if district_id != None:
        date = st.sidebar.date_input("Pick a date: ")
        date = str(date)
        d_sp = date.split("-")
        date = f"{d_sp[2]}-{d_sp[1]}-{d_sp[0]}"
        data = get_full_data(district_id, date)
        try:
            min_age = int(st.sidebar.text_input("Enter your age: "))
        except:
            min_age = None
        if min_age != None:
            if (min_age < 18):
                st.text("Sorry! You can not be vaccinated below the age of 18.")
            elif (min_age >= 18 and min_age < 45):
                min_age = 18
            elif (min_age >=45):
                min_age = 45
        st.table(filter_data(data, min_age))