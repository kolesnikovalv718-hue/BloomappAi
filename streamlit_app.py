import streamlit as st
st.set_page_config(page_title="Меню", layout="wide")

page = st.sidebar.selectbox(
    "Выбор", 
    ["Главная", "Редактор задач", "Обучение модели",
     "Статистика модели", "Сохранение модели ",
     "ученик","экспорт проба","runtask"]
)

# вывод главной сразу
if page == "Главная":
    st.title("Главная")
    st.write("Выбери задание слева")

#запуск заданий только после выбора
elif page == "Редактор задач":
    import task1
    task1.run()

elif page == "Обучение модели":
    import task2
    task2.run()

elif page == "Статистика модели":
    import task3
    task3.run()

elif page == "Сохранение модели":
    import task4
    task4.run()
    
elif page == "ученик":
    import task6
    task6.run()

elif page == "экспорт проба":
    import task8
    task8.run()
    
elif page == "runtask":
    import run_task
    run_task.run()
    
