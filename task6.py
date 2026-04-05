# task6_student.py
import streamlit as st
import pandas as pd
import os

def run():
    # ---------------------------
    # Заголовок и описание
    # ---------------------------
    st.title("📚 Учебные задачи")
    st.markdown("Выбирай задачу и решай! Сверху можно фильтровать по теме.")

    # ---------------------------
    # Путь к CSV с задачами
    # ---------------------------
    file_path = "blooms_dataset.csv"

    if not os.path.exists(file_path):
        st.error("Файл с задачами не найден")
        return

    # ---------------------------
    # Загрузка CSV
    # ---------------------------
    df = pd.read_csv(file_path, encoding='utf-8').fillna("")

    # ---------------------------
    # Цвета для Bloom
    # ---------------------------
    bloom_colors = {
        "Remembering": "gray",
        "Understanding": "blue",
        "Applying": "green",
        "Analyzing": "orange",
        "Evaluating": "red",
        "Creating": "purple"
    }

    # ---------------------------
    # Фильтр по теме
    # ---------------------------
    all_topics = ["Все"] + sorted(df["topic"].dropna().unique().tolist())
    selected_topic = st.selectbox("Фильтр по теме:", all_topics)

    if selected_topic != "Все":
        filtered_df = df[df["topic"] == selected_topic].reset_index()
    else:
        filtered_df = df.reset_index()

    # ---------------------------
    # Состояние выбранной задачи
    # ---------------------------
    if "current_task" not in st.session_state:
        st.session_state.current_task = 0

    # ---------------------------
    # Выбор задачи кнопками
    # ---------------------------
    st.markdown("**Выберите задачу:**")
    cols = st.columns(min(10, len(filtered_df)))
    for i, row in filtered_df.iterrows():
        col = cols[i % len(cols)]
        if col.button(str(i + 1)):
            st.session_state.current_task = i

    # ---------------------------
    # Показ выбранной задачи
    # ---------------------------
    task_idx = st.session_state.current_task
    if task_idx >= len(filtered_df):
        task_idx = 0
    st.session_state.current_task = task_idx

    task = filtered_df.loc[task_idx]

    st.markdown("---")
    st.markdown(f"**Задача {task_idx + 1} из {len(filtered_df)}**")
    st.markdown(f"**Тема:** {task['topic']}")
    st.markdown(f"**Bloom:** <span style='color:{bloom_colors.get(task['bloom'], 'black')}'>{task['bloom']}</span>", unsafe_allow_html=True)

    # Текст задачи и ответ
    st.subheader("Задача:")
    st.markdown(task["text"], unsafe_allow_html=True)

    # ---------------------------
    # Ввод ответа и проверка
    # ---------------------------
    answer_input = st.text_area("Ваш ответ:")

    if st.button("Проверить ответ"):
        correct = str(task["answer"]).strip()
        if answer_input.strip() == correct:
            st.success("✅ Правильно!")
        else:
            st.error(f"❌ Неправильно. Правильный ответ:\n{correct}")

    # ---------------------------
    # Выполнение Python-кода
    # ---------------------------
    st.subheader("🖥 Выполнить Python-код")
    code_input = st.text_area("Введите код для выполнения:", height=120)

    if st.button("Выполнить код"):
        with st.expander("Результат выполнения", expanded=True):
            try:
                local_vars = {}
                exec(code_input, {}, local_vars)
                if "result" in local_vars:
                    st.write("Результат:", local_vars["result"])
                else:
                    st.write("Код выполнен")
            except Exception as e:
                st.error(f"Ошибка выполнения: {e}")
