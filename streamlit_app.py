import streamlit as st

st.set_page_config(page_title="Меню", layout="wide")

page = st.sidebar.selectbox(
    "Выбор:",
    ["Главная", "Редактор задач", "Обучение модели",
     "Статистика модели", "Сохранение модели",
     "ученик","экспорт проба","runtask"]
)

if page == "Главная":
    st.markdown(
        """
        <style>
        body {
            background: #0f2027;  /* тёмный фон */
            background: linear-gradient(to right, #2c5364, #203a43, #0f2027);
            color: white;
        }
        .hero {
            text-align: center;
            padding: 80px 20px;
            font-family: 'Arial', sans-serif;
        }
        .hero h1 {
            font-size: 60px;
            background: linear-gradient(90deg, #ff6a00, #ee0979, #00f260);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glow 2s ease-in-out infinite alternate;
        }
        @keyframes glow {
            0% { text-shadow: 0 0 10px #ff6a00, 0 0 20px #ee0979; }
            50% { text-shadow: 0 0 20px #00f260, 0 0 40px #ee0979; }
            100% { text-shadow: 0 0 30px #ff6a00, 0 0 60px #00f260; }
        }
        .cards {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 50px;
        }
        .card {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            width: 200px;
            text-align: center;
            transition: transform 0.3s, background 0.3s;
        }
        .card:hover {
            transform: translateY(-10px);
            background: rgba(255,255,255,0.2);
        }
        .card h2 { font-size: 22px; }
        </style>

        <div class="hero">
            <h1>🚀 AI Панель управления</h1>
            <p>Выбери задание или следи за статусом модели</p>
        </div>

        <div class="cards">
            <div class="card"><h2>Редактор задач</h2></div>
            <div class="card"><h2>Обучение модели</h2></div>
            <div class="card"><h2>Статистика</h2></div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Остальные страницы — без изменений
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
