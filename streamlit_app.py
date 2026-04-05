import streamlit as st

# сначала только Streamlit
st.set_page_config(page_title="Меню", layout="wide")

page = st.sidebar.selectbox("Выбор", ["Главная", "Редактор задач", "Обучение модели"])

# вывод главной сразу
if page == "Главная":
    st.title("Главная")
    st.write("Выбери задание слева")

# импорт и запуск заданий только после выбора
elif page == "Редактор задач":
    import task1
    task1.run()

elif page == "Обучение модели":
    import task2
    task2.run()
