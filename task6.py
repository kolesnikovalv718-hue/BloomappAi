# ---------------------------
# Task6 для ученика с объяснением ИИ
# ---------------------------

import streamlit as st
import pandas as pd
import os

# Комментарий: интерфейс для ученика, задачи с Bloom, LaTeX, фильтр по теме, пояснение от ИИ
def run():

    file_path = "blooms_dataset.csv"

    # Загрузка CSV
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='utf-8')
    else:
        df = pd.DataFrame({
            "text": ["Пример:\n$$ P(6)=\\frac{1}{6} $$"],
            "answer": [""],
            "level": ["Знание"],
            "bloom": ["Remembering"],
            "topic": ["Probability"],
            "interdisciplinary": [""]
        })
    df = df.fillna("")

    if "df" not in st.session_state:
        st.session_state.df = df.copy()
    if "selected_task" not in st.session_state:
        st.session_state.selected_task = None

    bloom_colors = {
        "Remembering": "gray",
        "Understanding": "blue",
        "Applying": "green",
        "Analyzing": "orange",
        "Evaluating": "red",
        "Creating": "purple"
    }

    st.title("📚 Задачи для ученика")

    # ---------------------------
    # Фильтр по теме
    # ---------------------------
    st.subheader("Фильтр по теме")
    filter_topic = st.text_input("Введите тему:")

    filtered_df = st.session_state.df.copy()
    if filter_topic:
        filtered_df = filtered_df[filtered_df["topic"].str.lower().str.contains(filter_topic.lower())]

    if len(filtered_df) == 0:
        st.warning("Нет задач по этой теме")
        return

    # ---------------------------
    # Кнопки с номерами задач
    # ---------------------------
    st.subheader("Выберите задачу")
    cols = st.columns(len(filtered_df))
    for i, (_, row) in enumerate(filtered_df.iterrows()):
        if cols[i % len(cols)].button(f"{_+1}"):
            st.session_state.selected_task = _
    
    # ---------------------------
    # Показ выбранной задачи
    # ---------------------------
    if st.session_state.selected_task is not None:
        idx = st.session_state.selected_task
        task = st.session_state.df.loc[idx]

        st.markdown(f"**№{idx+1} Задача:**")
        st.markdown(task["text"], unsafe_allow_html=True)
        st.markdown(f"**Bloom:** <span style='color:{bloom_colors.get(task['bloom'], 'black')}'>{task['bloom']}</span>", unsafe_allow_html=True)
        st.markdown(f"**Тема:** {task['topic']}")

        # ---------------------------
        # Ввод ответа ученика
        # ---------------------------
        student_answer = st.text_area("Ваш ответ:")

        if st.button("Проверить ответ"):
            correct_answer = task["answer"]
            if student_answer.strip() == str(correct_answer).strip():
                st.success("✅ Верно!")
            else:
                st.error("❌ Неверно!")

        # ---------------------------
        # Пояснение от ИИ
        # ---------------------------
        st.markdown("---")
        st.markdown("💡 Пояснение от ИИ:")
        # Здесь можно подключить локальную модель GPT4All/llama.cpp
        # Пример: st.text(gpt_explain(task['text']))
        st.info("Здесь будет пояснение от ИИ (без раскрытия правильного ответа)")
