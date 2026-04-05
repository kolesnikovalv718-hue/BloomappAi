import streamlit as st

# сначала только Streamlit
st.set_page_config(page_title="Меню", layout="wide")

page = st.sidebar.selectbox("Выбор", ["Главная", "Задание 1", "Задание 2"])

# вывод главной сразу
if page == "Главная":
    st.title("Главная")
    st.write("Выбери задание слева 👈")

# импорт и запуск заданий только после выбора
elif page == "Задание 1":
    import task1
    task1.run()

elif page == "Задание 2":
    import task2
    task2.run()
