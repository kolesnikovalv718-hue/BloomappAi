# ---------------------------
# Task62для ученика с кодом, проверкой и ИИ-пояснением
# ---------------------------
import streamlit as st
import pandas as pd
import os
import requests
import re

# ---------------------------
# ИИ (HuggingFace)
# ---------------------------
HF_MODEL_URL = "https://api-inference.huggingface.co/models/NousResearch/Nous-Hermes-Llama2-13b"
HF_TOKEN = "hdd"

def gpt_explain(task_text):
    st.write("APP VERSION 2 LOADED")
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": f"Объясни задачу кратко и понятно без ответа:\n{task_text}",
        "parameters": {"max_new_tokens": 200}
    }
    try:
        r = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=60)
        data = r.json()
        return data[0]["generated_text"] if isinstance(data, list) else "Ошибка ИИ"
    except Exception as e:
        return f"Ошибка: {e}"


@st.cache_data
def get_explanation(text):
    return gpt_explain(text)


# ---------------------------
# APP
# ---------------------------
def run():

    file_path = "blooms_dataset.csv"

    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding="utf-8")
    else:
        df = pd.DataFrame({
            "text": ["Пример задачи $$P(A)=1/6$$"],
            "answer": ["1/6"],
            "topic": ["Probability"],
            "bloom": ["Remembering"]
        })

    df = df.fillna("")

    if "df" not in st.session_state:
        st.session_state.df = df.copy()

    if "selected_task" not in st.session_state:
        st.session_state.selected_task = None

    # ---------------------------
    # UI
    # ---------------------------
    st.title("📚 Smart LMS")

    tab1, tab2, tab3 = st.tabs(["📚 Задачи", "💻 Решение", "💡 Объяснение"])

    # ===========================
    # TAB 1 — ЗАДАЧИ
    # ===========================
    with tab1:

        st.subheader("Выбор задачи")

        topic = st.text_input("Фильтр по теме")

        filtered_df = st.session_state.df.copy()

        if topic:
            filtered_df = filtered_df[
                filtered_df["topic"].str.lower().str.contains(topic.lower())
            ]

        if len(filtered_df) == 0:
            st.warning("Нет задач")
            return

        task_options = filtered_df.reset_index()

        selected = st.selectbox(
            "Выберите задачу",
            task_options.index,
            format_func=lambda i: task_options.loc[i, "text"][:80] + "..."
        )

        st.session_state.selected_task = task_options.loc[selected, "index"]

    # ===========================
    # TAB 2 — РЕШЕНИЕ
    # ===========================
    with tab2:

        if st.session_state.selected_task is None:
            st.info("Выбери задачу")
            return

        task = st.session_state.df.loc[st.session_state.selected_task]

        st.markdown("### 📌 Задача")
        st.write(task["text"])

        # ---------------------------
        # ✍️ ТЕКСТОВЫЙ ОТВЕТ
        # ---------------------------
        st.markdown("### ✍️ Ответ")
        student_answer = st.text_input("Введите ответ")

        if st.button("Проверить ответ"):
            if student_answer.strip() == str(task["answer"]).strip():
                st.success("Верно ✅")
            else:
                st.error("Неверно ❌")

        # ---------------------------
        # 💻 КОД
        # ---------------------------
        st.markdown("### 💻 Код")
        student_code = st.text_area("Введите код")

        if st.button("Выполнить код"):

            try:
                safe_globals = {"__builtins__": {}}
                safe_locals = {}

                exec(student_code, safe_globals, safe_locals)

                result = list(safe_locals.values())[-1] if safe_locals else None

                st.write("📤 Результат:")
                st.write(result)

                # ✔ ЕДИНСТВЕННОЕ СРАВНЕНИЕ
                if str(result).strip() == str(task["answer"]).strip():
                    st.success("Код решён правильно ✅")
                else:
                    st.error("Неверный результат ❌")

            except Exception as e:
                st.error(f"Ошибка: {e}")

    # ===========================
    # TAB 3 — ИИ
    # ===========================
    with tab3:

        if st.session_state.selected_task is None:
            st.info("Выбери задачу")
            return

        task = st.session_state.df.loc[st.session_state.selected_task]

        st.subheader("💡 Объяснение")

        if st.button("Сгенерировать объяснение"):
            st.info(get_explanation(task["text"]))


# ---------------------------
# RUN
# ---------------------------
if __name__ == "__main__":
    run()
  
