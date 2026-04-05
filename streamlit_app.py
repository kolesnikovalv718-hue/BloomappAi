import streamlit as st
import task1
import task2

page = st.sidebar.selectbox("Выбор", ["Задание 1", "Задание 2"])

if page == "Задание 1":
    task1.run()
if page == "Задание 2":
    task1.run()
