import streamlit as st
import pandas as pd
import os

def run():
    """
    Ученический режим для задач Bloom.
    Только просмотр задач, ввод ответа и проверка.
    Статистика по уровням Bloom остаётся.
    """

    # ---------------------------
    # Путь к CSV
    # ---------------------------
    file_path = "blooms_dataset.csv"

    # ---------------------------
    # Загрузка CSV
    # ---------------------------
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='utf-8')
    else:
        st.error("Файл с задачами не найден")
        return

    df = df.fillna("")

    # ---------------------------
    # Session state
    # ---------------------------
    if "df" not in st.session_state:
        st.session_state.df = df.copy()
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = [""] * len(st.session_state.df)

    bloom_colors = {
        "Remembering": "gray",
        "Understanding": "blue",
        "Applying": "green",
        "Analyzing": "orange",
        "Evaluating": "red",
        "Creating": "purple"
    }

    # ---------------------------
    # Навигация
    # ---------------------------
    def next_task():
        if st.session_state.current_index < len(st.session_state.df) - 1:
            st.session_state.current_index += 1

    def prev_task():
        if st.session_state.current_index > 0:
            st.session_state.current_index -= 1

    # ---------------------------
    # Отображение текущей задачи
    # ---------------------------
    idx = st.session_state.current_index
    task = st.session_state.df.loc[idx]

    st.markdown(f"### Задача {idx+1}/{len(st.session_state.df)}")
    st.markdown(task["text"], unsafe_allow_html=True)
    st.markdown(f"**Bloom:** <span style='color:{bloom_colors.get(task['bloom'],'black')}'>{task['bloom']}</span>", unsafe_allow_html=True)
    st.markdown(f"**Тема:** {task['topic']}", unsafe_allow_html=True)

    st.text_area("Твой ответ:", key=f"user_answer_{idx}", height=80)
    
    # ---------------------------
    # Проверка ответа
    # ---------------------------
    if st.button("Проверить ответ"):
        user_answer = st.session_state.get(f"user_answer_{idx}", "").strip()
        correct_answer = task["answer"].strip()
        if user_answer == correct_answer:
            st.success("✅ Правильно!")
        else:
            st.error(f"❌ Неправильно. Правильный ответ:\n{correct_answer}")

    # ---------------------------
    # Кнопки навигации
    # ---------------------------
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("← Предыдущая задача"):
            prev_task()
    with nav2:
        if st.button("Следующая задача →"):
            next_task()

    # ---------------------------
    # Статистика Bloom
    # ---------------------------
    st.markdown("---")
    st.header("📊 Статистика по уровням Bloom")
    counts = st.session_state.df['bloom'].value_counts()
    for bloom, color in bloom_colors.items():
        count = counts.get(bloom, 0)
        st.markdown(f"<span style='color:{color}; font-weight:bold'>{bloom}: {count}</span>", unsafe_allow_html=True)
