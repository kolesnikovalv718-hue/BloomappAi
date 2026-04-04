import streamlit as st

# Настройка страницы
st.set_page_config(page_title="Bloom App", layout="wide")

# Выбор страницы через Sidebar
page = st.sidebar.radio(
    "Выберите страницу:",
    ["Редактор задач", "Обучение модели", "Статистика"]
)

# Импорт соответствующей страницы
if page == "Редактор задач":
    import pages.tasks_editor_1 as tasks_editor
elif page == "Обучение модели":
    import pages.train_model_2 as train_model
elif page == "Статистика":
    import pages.statistics_3 as statistics
