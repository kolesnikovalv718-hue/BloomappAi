import streamlit as st
import pandas as pd
import os
import requests
import re

# ===========================
# ИИ (HuggingFace)
# ===========================
HF_MODEL_URL = "https://router.huggingface.co/v1/models/mistralai/Mistral-7B-Instruct-v0.2"

HF_TOKEN = st.secrets.get("HF_TOKEN", None)

def gpt_explain(task_text):
    if not HF_TOKEN:
        return "💡 Нет HF_TOKEN в secrets"

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": f"Объясни задачу шаг за шагом:\n{task_text}",
        "parameters": {"max_new_tokens": 200}
    }

    try:
        r = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=60)

        if r.status_code != 200:
            st.write("STATUS:", r.status_code)
            st.write("RESPONSE:", r.text)
            return "💡 ИИ временно недоступен"

        data = r.json()

        # разные форматы ответа HF
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]

        if isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"]

        return str(data)

    except Exception as e:
        return f"💡 Ошибка подключения: {e}"


# ===========================
# APP
# ===========================
def run():

    file_path = "blooms_dataset.csv"

    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding="utf-8")
    else:
        df = pd.DataFrame({
            "text": ["Пример $$P(A)=1/6$$"],
            "answer": ["1/6"],
            "topic": ["probability"],
            "bloom": ["remembering"]
        })

    df["topic"] = df["topic"].fillna("").str.strip().str.lower()
    df["text"] = df["text"].fillna("")
    df["answer"] = df["answer"].fillna("")

    if "df" not in st.session_state:
        st.session_state.df = df.copy()

    if "selected_task" not in st.session_state:
        st.session_state.selected_task = None

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "total" not in st.session_state:
        st.session_state.total = 0

    st.title("📚 LMS PRO CHECKER")

    st.progress(st.session_state.score / max(st.session_state.total, 1))
    st.write(f"⭐ Баллы: {st.session_state.score} / {st.session_state.total}")

    tab1, tab2, tab3 = st.tabs(["📚 Задачи", "💻 Решение", "💡 ИИ"])

    # ===========================
    # TAB 1
    # ===========================
    with tab1:

        topic = st.text_input("Фильтр по теме")

        filtered_df = st.session_state.df.copy()

        if topic.strip():
            filtered_df = filtered_df[
                filtered_df["topic"].str.contains(topic.lower().strip(), na=False)
            ]

        task_options = filtered_df.reset_index()

        selected = st.selectbox(
            "Выберите задачу",
            task_options.index,
            format_func=lambda i: task_options.loc[i, "text"][:80]
        )

        st.session_state.selected_task = task_options.loc[selected, "index"]

    # ===========================
    # TAB 2
    # ===========================
    with tab2:

        if st.session_state.selected_task is None:
            st.info("Выбери задачу")
            return

        task = st.session_state.df.loc[st.session_state.selected_task]

        st.markdown("## 📌 Задача")

        parts = re.split(r"(\$\$.*?\$\$)", task["text"], flags=re.DOTALL)
        for part in parts:
            if part.startswith("$$") and part.endswith("$$"):
                st.latex(part.strip("$$"))
            else:
                st.markdown(part)

        mode = st.radio("Режим проверки", ["Ответ", "Код", "Оба"])

        # ===========================
        # ANSWER
        # ===========================
        if mode in ["Ответ", "Оба"]:

            student_answer = st.text_input("Введите ответ")

            if st.button("Проверить ответ"):

                st.session_state.total += 1

                if student_answer.strip() == str(task["answer"]).strip():
                    st.success("Верно ✅")
                    st.session_state.score += 1
                else:
                    st.error("Неверно ❌")
                    st.info(f"📌 Ожидаемый ответ: {task['answer']}")

        # ===========================
        # CODE
        # ===========================
        if mode in ["Код", "Оба"]:

            student_code = st.text_area("Введите код")

            if st.button("Выполнить код"):

                try:
                    safe_globals = {"__builtins__": {}}
                    safe_locals = {}

                    exec(student_code, safe_globals, safe_locals)

                    result = None
                    if safe_locals:
                        result = list(safe_locals.values())[-1]

                    st.write("📤 Результат:")
                    st.code(result)

                    st.session_state.total += 1

                    if str(result).strip() == str(task["answer"]).strip():
                        st.success("Код верный ✅")
                        st.session_state.score += 1
                    else:
                        st.error("Код неверный ❌")
                        st.info(f"📌 Ожидаемый ответ: {task['answer']}")

                except Exception as e:
                    st.error(f"Ошибка выполнения кода: {e}")

    # ===========================
    # TAB 3
    # ===========================
    with tab3:

        if st.session_state.selected_task is None:
            st.info("Выбери задачу")
            return

        task = st.session_state.df.loc[st.session_state.selected_task]

        if st.button("💡 Объяснить задачу ИИ"):
            st.info(gpt_explain(task["text"]))


if __name__ == "__main__":
    run()
