import os

# Создать папку pages, если её нет
if not os.path.exists("pages"):
    os.makedirs("pages")

# Создать пустой __init__.py, если его нет
init_file = os.path.join("pages", "__init__.py")
if not os.path.exists(init_file):
    with open(init_file, "w", encoding="utf-8") as f:
        f.write("# Пакет pages")


import streamlit as st

st.set_page_config(page_title="Bloom App", layout="wide")

page = st.sidebar.radio("Выберите страницу:", ["Редактор задач", "Обучение модели", "Статистика"])

if page == "Редактор задач":
    import pages.tasks_editor_1 as tasks_editor
elif page == "Обучение модели":
    import pages.train_model_2 as train_model
elif page == "Статистика":
    import pages.statistics_3 as statistics
    

