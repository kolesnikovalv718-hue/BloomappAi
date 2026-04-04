import streamlit as st

st.set_page_config(page_title="Bloom App", layout="wide")

page = st.sidebar.radio("Выберите страницу:", ["Редактор задач", "Обучение модели", "Статистика"])

if page == "Редактор задач":
    import pages.1_tasks_editor as tasks_editor
elif page == "Обучение модели":
    import pages.2_train_model as train_model
elif page == "Статистика":
    import pages.3_statistics as statistics
