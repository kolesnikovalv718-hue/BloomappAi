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
    body { background:#0c0f1e; color:white; font-family:'Segoe UI', sans-serif; }

    /* Герой-заголовок */
    .hero { text-align:center; padding:60px 20px; position:relative; }
    .hero h1 {
        font-size:60px; 
        background: linear-gradient(90deg, #ff6a00, #ee0979, #00f260);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight:bold; margin-bottom:10px;
    }
    .hero p { font-size:20px; color:#ccc; margin-bottom:50px; }

    /* Динамический фон с частицами */
    .bg-particles { position:absolute; width:100%; height:400px; top:0; left:0; overflow:hidden; z-index:-1; }
    .particle {
        position:absolute; border-radius:50%; opacity:0.3;
        animation: move 20s infinite linear;
    }
    .p1 { width:50px; height:50px; background:#ff6a00; top:10%; left:20%; }
    .p2 { width:30px; height:30px; background:#ee0979; top:30%; left:70%; }
    .p3 { width:40px; height:40px; background:#00f260; top:60%; left:40%; }
    .p4 { width:60px; height:60px; background:#2196F3; top:80%; left:10%; }
    @keyframes move {
        0% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
        100% { transform: translateY(0) rotate(360deg); }
    }

    /* Карточки Bloom */
    .grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap:30px; margin:0 20px 50px 20px; }
    .card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.1));
        border:2px solid rgba(255,255,255,0.1); border-radius:20px; padding:40px 20px;
        text-align:center; transition: transform 0.3s, box-shadow 0.3s; cursor:pointer;
        position:relative;
    }
    .card:hover { transform: translateY(-10px) rotate(-3deg); box-shadow:0 10px 50px rgba(0,0,0,0.7); }
    .card h2 { font-size:22px; margin-bottom:10px; color:white; }
    .card p { font-size:16px; color:#aaa; }

    /* Индикаторы прогресса */
    .progress-bar {
        position:absolute; bottom:10px; left:20px; width:80%; height:8px;
        background: rgba(255,255,255,0.1); border-radius:4px; overflow:hidden;
    }
    .progress-bar-inner {
        height:100%; width:0%; background: linear-gradient(90deg,#ff6a00,#00f260);
        border-radius:4px; animation: load 3s forwards;
    }
    @keyframes load { 0% { width:0%; } 100% { width:70%; } }
    </style>

    <div class="hero">
        <div class="bg-particles">
            <div class="particle p1"></div>
            <div class="particle p2"></div>
            <div class="particle p3"></div>
            <div class="particle p4"></div>
        </div>
        <h1>🎓 AI-педагогика & MML обучение</h1>
        <p>Bloom, тестирование и прогресс учеников в интерактивной панели</p>
    </div>

    <div class="grid">
        <div class="card">
            <h2>Знание</h2><p>Факты и определения</p>
            <div class="progress-bar"><div class="progress-bar-inner"></div></div>
        </div>
        <div class="card">
            <h2>Понимание</h2><p>Смысл и концепции</p>
            <div class="progress-bar"><div class="progress-bar-inner" style="animation-delay:0.3s"></div></div>
        </div>
        <div class="card">
            <h2>Применение</h2><p>Практические задачи</p>
            <div class="progress-bar"><div class="progress-bar-inner" style="animation-delay:0.6s"></div></div>
        </div>
        <div class="card">
            <h2>Анализ</h2><p>Разбор информации</p>
            <div class="progress-bar"><div class="progress-bar-inner" style="animation-delay:0.9s"></div></div>
        </div>
        <div class="card">
            <h2>Синтез</h2><p>Создание нового</p>
            <div class="progress-bar"><div class="progress-bar-inner" style="animation-delay:1.2s"></div></div>
        </div>
        <div class="card">
            <h2>Оценка</h2><p>Критическая оценка</p>
            <div class="progress-bar"><div class="progress-bar-inner" style="animation-delay:1.5s"></div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Остальные страницы без изменений
elif page == "Редактор задач": import task1; task1.run()
elif page == "Обучение модели": import task2; task2.run()
elif page == "Статистика модели": import task3; task3.run()
elif page == "Сохранение модели": import task4; task4.run()
elif page == "ученик": import task6; task6.run()
elif page == "экспорт проба": import task8; task8.run()
elif page == "runtask": import run_task; run_task.run()
