import streamlit as st

st.set_page_config(page_title="Bloom App", layout="wide")

page = st.sidebar.radio("Выберите страницу:", ["Редактор задач", "Обучение модели", "Статистика"])

if page == "Редактор задач":
    import pages.tasks_editor_1 as tasks_editor
elif page == "Обучение модели":
    import pages.train_model_2 as train_model
elif page == "Статистика":
    import pages.statistics_3 as statistics
    

