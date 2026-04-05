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
        background: #0f111a;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Герой-заголовок */
    .hero {
        text-align:center;
        padding:60px 20px;
        position: relative;
    }
    .hero h1 {
        font-size:60px;
        background: linear-gradient(90deg, #ff6a00, #ee0979, #00f260);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight:bold;
        margin-bottom:10px;
    }
    .hero p {
        font-size:20px;
        color:#ccc;
        margin-bottom:50px;
    }

    /* Геометрический фон */
    .bg-shapes {
        position: absolute;
        width:100%; height:400px; top:0; left:0;
        overflow:hidden; z-index:-1;
    }
    .shape {
        position:absolute;
        border-radius:20%;
        opacity:0.2;
        animation: move 15s infinite linear;
    }
    .shape1 { width:150px; height:150px; background:#ff6a00; top:10%; left:5%; }
    .shape2 { width:200px; height:200px; background:#ee0979; top:40%; left:70%; }
    .shape3 { width:100px; height:100px; background:#00f260; top:70%; left:30%; }
    @keyframes move {
        0% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
        100% { transform: translateY(0) rotate(360deg); }
    }

    /* Карточки Bloom */
    .grid {
        display:grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap:30px;
        margin:0 20px 50px 20px;
    }
    .card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.1));
        border: 2px solid rgba(255,255,255,0.1);
        border-radius:20px;
        padding:40px 20px;
        text-align:center;
        transition: transform 0.3s, box-shadow 0.3s;
        cursor:pointer;
    }
    .card:hover {
        transform: translateY(-10px) rotate(-3deg);
        box-shadow: 0 10px 50px rgba(0,0,0,0.7);
    }
    .card h2 { font-size:22px; margin-bottom:10px; color:white; }
    .card p { font-size:16px; color:#aaa; }
    </style>

    <div class="hero">
        <div class="bg-shapes">
            <div class="shape shape1"></div>
            <div class="shape shape2"></div>
            <div class="shape shape3"></div>
        </div>
        <h1>🎓 AI-педагогика & MML обучение</h1>
        <p>Блум, тестирование и прогресс учеников в одной панели</p>
    </div>

    <div class="grid">
        <div class="card"><h2>Знание</h2><p>Факты и определения</p></div>
        <div class="card"><h2>Понимание</h2><p>Смысл и концепции</p></div>
        <div class="card"><h2>Применение</h2><p>Практические задачи</p></div>
        <div class="card"><h2>Анализ</h2><p>Разбор информации</p></div>
        <div class="card"><h2>Синтез</h2><p>Создание нового</p></div>
        <div class="card"><h2>Оценка</h2><p>Критическая оценка</p></div>
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
