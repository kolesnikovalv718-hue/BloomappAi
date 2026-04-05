# task6_student.py
import streamlit as st
import pandas as pd
import os

# ---------------------------
# Функция запуска для ученика
# ---------------------------
def run():
    """
    Задачи для ученика:
    - Фильтр по теме
    - Выбор задачи по кнопкам
    - Проверка ответа
    - Пояснение от GPT (только объяснение)
    - Прогресс
    """

    # ---------------------------
    # Загрузка данных
    # ---------------------------
    file_path = "blooms_dataset.csv"

    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='utf-8')
    else:
        st.warning("Файл задач не найден. Пример загружен.")
        df = pd.DataFrame({
            "text": ["Пример:\n$$ P(6)=\\frac{1}{6} $$"],
            "answer": [""],
            "level": ["Знание"],
            "bloom": ["Remembering"],
            "topic": ["Probability"]
        })
    df = df.fillna("")

    # ---------------------------
    # Bloom цвета
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
    # Session state
    # ---------------------------
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "filtered_indices" not in st.session_state:
        st.session_state.filtered_indices = list(range(len(df)))

    # ---------------------------
    # Фильтр по теме
    # ---------------------------
    st.header("Фильтр по теме")
    filter_topic = st.text_input("Введите тему:")
    filtered_df = df.copy()
    if filter_topic:
        filtered_df = df[filtered_df["topic"].str.lower().str.contains(filter_topic.lower())]
    st.session_state.filtered_indices = filtered_df.index.tolist()

    if len(st.session_state.filtered_indices) == 0:
        st.warning("Нет задач по выбранной теме")
        return

    # ---------------------------
    # Кнопки выбора задачи
    # ---------------------------
    st.subheader("Выберите задачу")
    cols = st.columns(10)
    for idx, task_idx in enumerate(st.session_state.filtered_indices):
        if cols[idx % 10].button(f"{task_idx+1}", key=f"btn_{task_idx}"):
            st.session_state.current_index = task_idx

    # ---------------------------
    # Текущая задача
    # ---------------------------
    idx = st.session_state.current_index
    task = df.loc[idx]

    st.markdown("---")
    st.markdown(f"**Задача {idx+1}/{len(df)}**")
    st.markdown(f"**Bloom:** <span style='color:{bloom_colors.get(task['bloom'], 'black')}'>{task['bloom']}</span>", unsafe_allow_html=True)
    st.markdown(f"**Тема:** {task['topic']}")
    st.markdown("---")
    st.markdown(task["text"], unsafe_allow_html=True)

    # ---------------------------
    # Поле для ответа
    # ---------------------------
    answer_input = st.text_area("Ваш ответ:", key=f"answer_{idx}", height=100)
    if st.button("Проверить ответ", key=f"check_{idx}"):
        correct_answer = str(task["answer"]).strip()
        if answer_input.strip() == correct_answer:
            st.success("✅ Верно!")
        else:
            st.error(f"❌ Неверно. Правильный ответ:\n{correct_answer}")

    # ---------------------------
    # Пояснение GPT (только объяснение)
    # ---------------------------
    st.markdown("---")
    if st.button("Объяснить с GPT", key=f"gpt_{idx}"):
        # Здесь можно вызвать GPT API с задачей и ответом
        st.info("💡 Пояснение (пример без API):\nОбъяснение шагов решения задачи, рассуждения и логики, без готового ответа.")

    # ---------------------------
    # Прогресс
    # ---------------------------
    st.markdown("---")
    st.info(f"Прогресс: задача {st.session_state.current_index+1} из {len(df)}")
