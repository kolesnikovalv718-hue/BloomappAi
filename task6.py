# ---------------------------
# Task6 для ученика с кодом, проверкой и ИИ-пояснением
# ---------------------------

import streamlit as st
import pandas as pd
import os
import requests
import re
import io
import sys

# ---------------------------
# Hugging Face API для пояснений
# ---------------------------
HF_MODEL_URL = "https://api-inference.huggingface.co/models/NousResearch/Nous-Hermes-Llama2-13b"
HF_TOKEN = "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" 

def gpt_explain(task_text):
    """Генерирует краткое объяснение задачи для ученика без раскрытия ответа"""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": f"Объясни кратко и понятно задачу ученику, без ответа:\n{task_text}",
        "parameters": {"max_new_tokens": 200}
    }
    try:
        response = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=60)
        data = response.json()
        return data[0]["generated_text"] if isinstance(data, list) and "generated_text" in data[0] else "💡 Пояснение не удалось получить"
    except Exception as e:
        return f"Ошибка при вызове ИИ: {e}"

# ---------------------------
# Главная функция Streamlit
# ---------------------------
def run():
    # ---------------------------
    # Загрузка CSV с задачами или создание примера
    # ---------------------------
    file_path = "blooms_dataset.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='utf-8')
    else:
        df = pd.DataFrame({
            "text": ["Пример:\n$$ P(6)=\\frac{1}{6} $$"],
            "answer": ["1/6"],  # правильный ответ для проверки
            "level": ["Знание"],
            "bloom": ["Remembering"],
            "topic": ["Probability"],
            "interdisciplinary": [""]
        })
    df = df.fillna("")

    # ---------------------------
    # Streamlit state
    # ---------------------------
    if "df" not in st.session_state:
        st.session_state.df = df.copy()
    if "selected_task" not in st.session_state:
        st.session_state.selected_task = None
    if "checked" not in st.session_state:
        st.session_state.checked = False
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False
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
            st.session_state.checked = False
            st.session_state.show_answer = False
            st.session_state.student_result = None

    # ---------------------------
    # Показ выбранной задачи
    # ---------------------------
    if st.session_state.selected_task is not None:
        idx = st.session_state.selected_task
        task = st.session_state.df.loc[idx]

        st.markdown(f"**№{idx+1} Задача:**")

        # Разделяем текст задачи на обычный текст и LaTeX
        parts = re.split(r"(\$\$.*?\$\$)", task["text"], flags=re.DOTALL)
        for part in parts:
            if part.startswith("$$") and part.endswith("$$"):
                st.latex(part.strip("$$"))
            else:
                st.markdown(part)

        st.markdown(f"**Bloom:** <span style='color:{bloom_colors.get(task['bloom'], 'black')}'>{task['bloom']}</span>", unsafe_allow_html=True)
        st.markdown(f"**Тема:** {task['topic']}")

        # ---------------------------
        # Поле для текстового ответа
        # ---------------------------
        student_answer = st.text_area("Ваш ответ:")

        # Кнопка проверки текстового ответа
        if st.button("Проверить ответ"):
            if str(student_answer).strip() == str(task["answer"]).strip():
                st.success("✅ Верно!")
            else:
                st.error("❌ Неверно!")
            st.session_state.checked = True

        # Кнопка показать правильный ответ
        if st.button("Показать правильный ответ"):
            st.info(f"Правильный ответ: {task['answer']}")
            st.session_state.show_answer = True

        # ---------------------------
        # Поле для кода ученика
        # ---------------------------
        student_code = st.text_area("Введите код для решения задачи (если нужно):", height=150)

        # Кнопка выполнения кода с перехватом print и eval последней строки
        if st.button("Выполнить код"):
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()  # перехват print
            result = None
            try:
                local_vars = {}
                code_lines = student_code.strip().split("\n")

                if len(code_lines) > 1:
                    exec("\n".join(code_lines[:-1]), {}, local_vars)

                last_line = code_lines[-1]

                if "=" in last_line:
                    exec(last_line, {}, local_vars)
                    var_name = last_line.split("=")[0].strip()
                    result = local_vars.get(var_name)
                else:
                    try:
                        result = eval(last_line, {}, local_vars)
                    except:
                        exec(last_line, {}, local_vars)

                printed = redirected_output.getvalue()
                if printed:
                    result = printed.strip()

                st.session_state.student_result = result
                st.success(f"Код выполнен, результат: {st.session_state.student_result}")
                st.session_state.checked = True

            except Exception as e:
                st.error(f"Ошибка выполнения кода: {e}")
            finally:
                sys.stdout = old_stdout  # восстановление stdout

        # ---------------------------
        # Пояснение от ИИ
        # ---------------------------
        if st.session_state.checked or st.session_state.show_answer:
            st.markdown("---")
            st.markdown("💡 Пояснение от ИИ:")
            explanation = gpt_explain(task["text"])
            st.info(explanation)


# ---------------------------
# Запуск приложения
# ---------------------------
if __name__ == "__main__":
    run()
