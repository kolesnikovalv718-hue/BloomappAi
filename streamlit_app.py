import streamlit as st

st.set_page_config(page_title="Меню", layout="wide")

page = st.sidebar.selectbox(
    "Выбор",
    ["Главная", "Редактор задач", "Обучение модели",
     "Статистика модели", "Сохранение модели",
     "ученик","экспорт проба","runtask"]
)

if page == "Главная":
    st.markdown("""
    <style>
    body {
        background: #1e1e1e;
        font-family: 'Arial', sans-serif;
        color: white;
    }
    .hero {
        text-align: center;
        padding: 50px 20px;
    }
    .hero h1 {
        font-size: 50px;
        background: linear-gradient(90deg, #ff6a00, #ee0979, #00f260);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .hero p {
        font-size: 20px;
        color: #ccc;
        margin-top: 10px;
    }
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 30px;
        margin: 50px 20px;
    }
    .card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.1));
        border: 2px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 40px 20px;
        text-align: center;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .card:hover {
        transform: translateY(-10px) rotate(-2deg);
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }
    .card h2 {
        font-size: 22px;
        margin-bottom: 10px;
        color: #fff;
    }
    .card p {
        color: #aaa;
        font-size: 16px;
    }
    </style>

    <div class="hero">
        <h1>🎓 AI-педагогика и тестирование</h1>
        <p>Блум, MML обучение и тестирование в одной панели</p>
    </div>

    <div class="grid">
        <div class="card">
            <h2>Знание</h2>
            <p>Тестирование базовых знаний и фактов</p>
        </div>
        <div class="card">
            <h2>Понимание</h2>
            <p>Проверка понимания концепций</p>
        </div>
        <div class="card">
            <h2>Применение</h2>
            <p>Практические задания и кейсы</p>
        </div>
        <div class="card">
            <h2>Анализ</h2>
            <p>Разбор данных и выводы</p>
        </div>
        <div class="card">
            <h2>Синтез</h2>
            <p>Создание новых решений</p>
        </div>
        <div class="card">
            <h2>Оценка</h2>
            <p>Критическая оценка и самоанализ</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Остальные страницы остаются без изменений
elif page == "Редактор задач":
    import task1; task1.run()
elif page == "Обучение модели":
    import task2; task2.run()
elif page == "Статистика модели":
    import task3; task3.run()
elif page == "Сохранение модели":
    import task4; task4.run()
elif page == "ученик":
    import task6; task6.run()
elif page == "экспорт проба":
    import task8; task8.run()
elif page == "runtask":
    import run_task; run_task.run()
