import streamlit as st
import pandas as pd
import os
import requests
import re

# ===========================
# ИИ (СТАБИЛЬНЫЙ HUGGINGFACE API)
# ===========================
HF_MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

HF_TOKEN = st.secrets["HF_TOKEN"]  # или вставь напрямую для теста

def gpt_explain(task_text):

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    payload = {
        "inputs": task_text,
        "parameters": {
            "max_new_tokens": 200
        }
    }

    try:
        r = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=60)
        data = r.json()

        # ошибка API
        if isinstance(data, dict) and "error" in data:
            return f"💡 ИИ недоступен: {data['error']}"

        # нормальный ответ
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]

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
            "text": ["Пример задачи $$P(A)=1/6$$"],
            "answer": ["1/6"],
            "topic": ["probability"],
            "bloom": ["remembering"]
        })

    df["topic"] = df["topic"].fillna("").str.strip().str.lower()
    df["text"] = df["text"].fillna("")
    df["answer"] = df["answer"].fillna("")

    # ===========================
    # SESSION
    # ===========================
    if "selected_task" not in st.session_state:
        st.session_state.selected_task = None

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "total" not in st.session_state:
        st.session_state.total = 0

    # ===========================
    # UI
    # ===========================
    st.title("📚 LMS PRO (STABLE VERSION)")

    st.progress(st.session_state.score / max(st.session_state.total, 1))
    st.write(f"⭐ {st.session_state.score} / {st.session_state.total}")

    tab1, tab2, tab3 = st.tabs(["📚 Задачи", "💻 Решение", "💡 ИИ"])

    # ===========================
    # TAB 1
    # ===========================
    with tab1:

        topic = st.text_input("Фильтр по теме")

        filtered = df.copy()

        if topic.strip():
            filtered = filtered[filtered["topic"].str.contains(topic.lower(), na=False)]

        task_list = filtered.reset_index()

        choice = st.selectbox(
            "Выбери задачу",
            task_list.index,
            format_func=lambda i: task_list.loc[i, "text"][:80]
        )

        st.session_state.selected_task = task_list.loc[choice, "index"]

    # ===========================
    # TAB 2
    # ===========================
    with tab2:

        if st.session_state.selected_task is None:
            st.info("Выбери задачу")
            return

        task = df.loc[st.session_state.selected_task]

        st.markdown("## 📌 Задача")

        parts = re.split(r"(\$\$.*?\$\$)", task["text"], flags=re.DOTALL)
        for part in parts:
            if part.startswith("$$") and part.endswith("$$"):
                st.latex(part.strip("$$"))
            else:
                st.markdown(part)

        # --------------------
        # ОТВЕТ
        # --------------------
        st.markdown("### ✍️ Ответ")
        ans = st.text_input("Введите ответ")

        if st.button("Проверить ответ"):
            st.session_state.total += 1

            if ans.strip() == task["answer"].strip():
                st.success("Верно ✅")
                st.session_state.score += 1
            else:
                st.error("Неверно ❌")
                st.info(f"Ожидаемый ответ: {task['answer']}")

        # --------------------
        # КОД
        # --------------------
        st.markdown("### 💻 Код")
        code = st.text_area("Python код")

        if st.button("Выполнить код"):

            try:
                local = {}
                exec(code, {}, local)

                result = list(local.values())[-1] if local else None

                st.write("Результат:", result)

                st.session_state.total += 1

                if str(result).strip() == task["answer"].strip():
                    st.success("Код верный ✅")
                    st.session_state.score += 1
                else:
                    st.error("Код неверный ❌")
                    st.info(f"Ожидаемый: {task['answer']}")

            except Exception as e:
                st.error(f"Ошибка: {e}")

    # ===========================
    # TAB 3
    # ===========================
    with tab3:

        if st.session_state.selected_task is None:
            st.info("Выбери задачу")
            return

        task = df.loc[st.session_state.selected_task]

        if st.button("💡 Объяснить"):
            st.info(gpt_explain(task["text"]))


if __name__ == "__main__":
    run()
