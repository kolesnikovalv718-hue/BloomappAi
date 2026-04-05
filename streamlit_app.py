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
    body { background:#0a1f3d; color:white; font-family:'Segoe UI', sans-serif; }

    /* Герой-заголовок */
    .hero { text-align:center; padding:60px 20px; position:relative; overflow:hidden; }
    .hero h1 {
        font-size:56px;
        background: linear-gradient(90deg, #00d4ff, #0077ff, #00aaff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight:bold; margin-bottom:10px;
    }
    .hero p { font-size:20px; color:#a0c4ff; margin-bottom:50px; }

    /* Синусоида на фоне */
    .sinewave {
        position:absolute; width:200%; height:400px; top:0; left:-50%;
        background: repeating-linear-gradient(
            0deg,
            rgba(0,255,255,0.1) 0px,
            rgba(0,255,255,0.1) 2px,
            transparent 2px,
            transparent 10px
        );
        animation: wave 8s linear infinite;
        transform: rotate(45deg);
        z-index:-2;
    }
    @keyframes wave {
        0% { transform: translateX(0) rotate(45deg); }
        100% { transform: translateX(-50%) rotate(45deg); }
    }

    /* Светящаяся карта (точки + линии) */
    .network { position:absolute; width:100%; height:100%; top:0; left:0; z-index:-1; }
    .node {
        position:absolute;
        width:8px; height:8px;
        background:#00f0ff;
        border-radius:50%;
        box-shadow: 0 0 15px #00f0ff, 0 0 25px #00d4ff;
        animation: flicker 3s infinite alternate;
    }
    @keyframes flicker { 0% { opacity:0.4; } 50% { opacity:1; } 100% { opacity:0.4; } }

    /* Карточки Bloom */
    .grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap:30px; margin:0 20px 50px 20px; }
    .card {
        background: linear-gradient(135deg, rgba(0,119,255,0.2), rgba(0,180,255,0.1));
        border-radius:20px; padding:40px 20px; text-align:center; transition: transform 0.3s, box-shadow 0.3s;
        cursor:pointer; border:1px solid rgba(0,180,255,0.3); position:relative;
    }
    .card:hover { transform: translateY(-10px) rotate(-3deg); box-shadow:0 10px 50px rgba(0,0,0,0.7); }
    .card h2 { font-size:22px; margin-bottom:10px; color:#00f0ff; }
    .card p { font-size:16px; color:#a0d4ff; }

    /* Прогресс-бары */
    .progress-bar { position:absolute; bottom:10px; left:20px; width:80%; height:8px; background: rgba(255,255,255,0.1); border-radius:4px; overflow:hidden; }
    .progress-bar-inner { height:100%; width:0%; background: linear-gradient(90deg,#00d4ff,#0077ff); border-radius:4px; animation: load 3s forwards; }
    @keyframes load { 0% { width:0%; } 100% { width:70%; } }
    </style>

    <div class="hero">
        <div class="sinewave"></div>
        <div class="network">
            <div class="node" style="top:10%; left:20%;"></div>
            <div class="node" style="top:30%; left:70%;"></div>
            <div class="node" style="top:60%; left:40%;"></div>
            <div class="node" style="top:80%; left:10%;"></div>
        </div>
        <h1>🎓 AI-педагогика & MML обучение</h1>
        <p>Интерактивная карта знаний Bloom с прогрессом учеников</p>
    </div>

    <div class="grid">
        <div class="card"><h2>Знание</h2><p>Факты и определения</p><div class="progress-bar"><div class="progress-bar-inner"></div></div></div>
        <div class="card"><h2>Понимание</h2><p>Смысл и концепции</p><div class="progress-bar"><div class="progress-bar-inner" style="animation-delay:0.3s"></div></div></div>
        <div class="card"><h2>Применение</h2><p>Практические задачи</p><div class="progress-bar"><div class="progress-bar-inner" style="animation-delay:0.6s"></div></div></div>
        <div class="card"><h2>Анализ</h2><p>Разбор информации</p><div class="progress-bar"><div class="progress-bar-inner" style="animation-delay:0.9s"></div></div></div>
        <div class="card"><h2>Синтез</h2><p>Создание нового</p><div class="progress-bar"><div class="progress-bar-inner" style="animation-delay:1.2s"></div></div></div>
        <div class="card"><h2>Оценка</h2><p>Критическая оценка</p><div class="progress-bar"><div class="progress-bar-inner" style="animation-delay:1.5s"></div></div></div>
    </div>
    """, unsafe_allow_html=True)

# Остальные страницы
elif page == "Редактор задач": import task1; task1.run()
elif page == "Обучение модели": import task2; task2.run()
elif page == "Статистика модели": import task3; task3.run()
elif page == "Сохранение модели": import task4; task4.run()
elif page == "ученик": import task6; task6.run()
elif page == "экспорт проба": import task8; task8.run()
elif page == "runtask": import run_task; run_task.run()
