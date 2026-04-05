# ---------------------------
# Task6 для ученика с пояснением ИИ и поддержкой кода ученика
# ---------------------------

import streamlit as st
import pandas as pd
import os
from gpt4all import GPT4All
import re

def run():
    # ---------------------------
    # Инициализация локальной модели ИИ (GPT4All)
    # ---------------------------
    model_path = "ggml-gpt4all-j-v1.3-groovy.bin"  # загрузи модель заранее
    gpt_model = GPT4All(model_path)

    # ---------------------------
    # Функция генерации пояснения от ИИ
    # ---------------------------
    def gpt_explain(task_text):
        """
        Генерирует краткое объяснение задачи для ученика
        без раскрытия правильного ответа
        """
        prompt = f"Объясни кратко и понятно задачу ученику, без раскрытия ответа:\n{task_text}\nПояснение:"
        response = gpt_model.generate(prompt, max_tokens=200)
        return response

    # ---------------------------
    # Загрузка CSV с задачами или создание примера
    # ---------------------------
    file_path = "blooms_dataset.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='utf-8')
    else:
        # Пример задачи с LaTeX
        df = pd.DataFrame({
            "text": ["Пример:\n$$ P(6)=\\frac{1}{6} $$"],
            "answer": [""],  # сюда может быть ожидаемый результат выполнения
            "level": ["Знание"],
            "bloom": ["Remembering"],
            "topic": ["Probability"],
            "interdisciplinary": [""]
        })
    df = df.fillna("")

    # ---------------------------
    # Streamlit state для сохранения между перезагрузками
    # ---------------------------
    if "df" not in st.session_state:
        st.session_state.df = df.copy()
    if "selected_task" not in st.session_state:
        st.session_state.selected_task = None
    if "show_explanation" not in st.session_state:
        st.session_state.show_explanation = False
    if "student_result" not in st.session_state:
        st.session_state.student_result = None

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
    # Кнопки выбора задачи
    # ---------------------------
    st.subheader("Выберите задачу")
    for i, (_, row) in enumerate(filtered_df.iterrows()):
        if st.button(f"Задача {_+1}"):
            st.session_state.selected_task = _
            st.session_state.show_explanation = False  # сброс пояснения при смене задачи
            st.session_state.student_result = None     # сброс результата выполнения

    # ---------------------------
    # Показ выбранной задачи с LaTeX
    # ---------------------------
    if st.session_state.selected_task is not None:
        idx = st.session_state.selected_task
        task = st.session_state.df.loc[idx]

        st.markdown(f"**№{idx+1} Задача:**")

        # Разделяем текст задачи на обычный текст и формулы $$...$$
        parts = re.split(r"(\$\$.*?\$\$)", task["text"], flags=re.DOTALL)
        for part in parts:
            if part.startswith("$$") and part.endswith("$$"):
                st.latex(part.strip("$$"))
            else:
                st.markdown(part)

        st.markdown(f"**Bloom:** <span style='color:{bloom_colors.get(task['bloom'], 'black')}'>{task['bloom']}</span>", unsafe_allow_html=True)
        st.markdown(f"**Тема:** {task['topic']}")

        # ---------------------------
        # Поле для кода ученика
        # ---------------------------
        student_code = st.text_area("Введите код для решения задачи:")

        # ---------------------------
        # Кнопка выполнения кода ученика
        # ---------------------------
        if st.button("Выполнить код"):
            try:
                local_vars = {}
                exec(student_code, {}, local_vars)  # выполнение кода ученика безопасно в отдельном словаре
                # Ожидаем, что результат выполнения помещается в переменную `result`
                st.session_state.student_result = local_vars.get("result", None)
                st.success(f"Код выполнен, результат: {st.session_state.student_result}")
                st.session_state.show_explanation = True  # показать пояснение после выполнения
            except Exception as e:
                st.error(f"Ошибка выполнения кода: {e}")

        # ---------------------------
        # Пояснение от ИИ (только после выполнения кода)
        # ---------------------------
        if st.session_state.show_explanation:
            st.markdown("---")
            st.markdown("💡 Пояснение от ИИ:")
            explanation = gpt_explain(task["text"])
            st.info(explanation)
