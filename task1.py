import streamlit as st
import pandas as pd
import os
import joblib

def run():

    st.markdown("""
<style>

.stButton > button {
    border-radius: 12px;
    padding: 10px;
    font-weight: bold;
    color: white;
    border: none;
    transition: 0.2s;
}

/* кнопки */
button[id*="prev"] {
    background: linear-gradient(45deg, #6c757d, #495057);
}

div[data-testid="column"]:nth-of-type(2) .stButton > button {
    background: linear-gradient(45deg, #0d6efd, #3a86ff);
}

div[data-testid="column"]:nth-of-type(3) .stButton > button {
    background: linear-gradient(45deg, #198754, #2ecc71);
}

div[data-testid="column"]:nth-of-type(4) .stButton > button {
    background: linear-gradient(45deg, #fd7e14, #ff9f43);
}

div[data-testid="column"]:nth-of-type(6) .stButton > button {
    background: linear-gradient(45deg, #dc3545, #ff4d6d);
}

.stButton:last-child > button {
    background: linear-gradient(45deg, #6f42c1, #9b5de5);
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 10px rgba(0,0,0,0.3);
}

</style>
""", unsafe_allow_html=True)

    # ===========================
    # MODEL
    # ===========================
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")

    def predict_bloom(text):
        vec = vectorizer.transform([text])
        return model.predict(vec)[0]

    file_path = "blooms_dataset.csv"

    # ===========================
    # DATA LOAD
    # ===========================
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='utf-8')
        df["text"] = df["text"].astype(str).str.replace("\\n", "\n")
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

    # ===========================
    # SESSION
    # ===========================
    if "df" not in st.session_state:
        st.session_state.df = df.copy()

    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    bloom_colors = {
        "Remembering": "gray",
        "Understanding": "blue",
        "Applying": "green",
        "Analyzing": "orange",
        "Evaluating": "red",
        "Creating": "purple"
    }

    # ===========================
    # SAVE
    # ===========================
    def save_current_task():
        idx = st.session_state.current_index
        st.session_state.df.loc[idx, "text"] = st.session_state.get(f"text_{idx}", "")
        st.session_state.df.loc[idx, "answer"] = st.session_state.get(f"answer_{idx}", "")
        st.session_state.df.loc[idx, "topic"] = st.session_state.get(f"topic_{idx}", "")
        st.session_state.df.loc[idx, "interdisciplinary"] = st.session_state.get(f"inter_{idx}", "")
        st.session_state.df.loc[idx, "bloom"] = st.session_state.get(f"bloom_{idx}", "Remembering")

    def save_csv():
        save_current_task()
        st.session_state.df.to_csv(
            file_path,
            index=False,
            encoding='utf-8',
            quoting=1
        )
        st.success("Сохранено!")

    # ===========================
    # NAVIGATION
    # ===========================
    def next_task():
        save_current_task()
        if st.session_state.current_index < len(st.session_state.df) - 1:
            st.session_state.current_index += 1

    def prev_task():
        save_current_task()
        if st.session_state.current_index > 0:
            st.session_state.current_index -= 1

    def add_task():
        save_current_task()
        new_row = {
            "text": "",
            "answer": "",
            "level": "",
            "bloom": "Remembering",
            "topic": "",
            "interdisciplinary": ""
        }
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
        st.session_state.current_index = len(st.session_state.df) - 1

    def delete_task():
        save_current_task()
        idx = st.session_state.current_index
        if len(st.session_state.df) > 0:
            st.session_state.df.drop(idx, inplace=True)
            st.session_state.df.reset_index(drop=True, inplace=True)
            st.session_state.current_index = max(0, idx - 1)

    # ===========================
    # UI
    # ===========================
    st.title("📚 Редактор задач (FULL LMS)")
    st.info(f"Всего задач: {len(st.session_state.df)}")

    # NAV BUTTONS
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅ Назад"):
            prev_task()

    with col2:
        if st.button("➡ Вперёд"):
            next_task()

    with col3:
        if st.button("➕ Добавить"):
            add_task()

    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button("💾 Сохранить"):
            save_csv()

    with col5:
        st.download_button(
            "⬇ Скачать CSV",
            st.session_state.df.to_csv(index=False).encode("utf-8"),
            "blooms_dataset.csv"
        )

    with col6:
        if st.button("🗑 Удалить"):
            delete_task()

    # ===========================
    # TASK EDITOR
    # ===========================
    idx = st.session_state.current_index

    st.subheader("📌 Задача")

    st.text_area("Текст:", value=st.session_state.df.loc[idx, "text"], key=f"text_{idx}", height=120)
    st.text_area("Ответ:", value=st.session_state.df.loc[idx, "answer"], key=f"answer_{idx}", height=80)
    st.text_input("Тема:", value=st.session_state.df.loc[idx, "topic"], key=f"topic_{idx}")
    st.text_input("Междисциплинарная:", value=st.session_state.df.loc[idx, "inter_{idx}")

    # BLOOM
    st.markdown("---")
    st.subheader("Bloom")

    text_val = st.session_state.get(f"text_{idx}", "")
    bloom_pred = predict_bloom(text_val) if text_val else "Remembering"

    st.selectbox(
        "Bloom:",
        list(bloom_colors.keys()),
        index=list(bloom_colors.keys()).index(bloom_pred),
        key=f"bloom_{idx}"
    )

    st.markdown("---")

    # ===========================
    # CODE EDITOR
    # ===========================
    st.subheader("🖥 Код")

    code_val = st.text_area("Python код:", key=f"code_{idx}", height=150)

    if st.button("🚀 Выполнить"):
        try:
            local = {}
            exec(code_val, {}, local)

            if "result" in local:
                st.success(f"Результат: {local['result']}")
            else:
                st.success("Код выполнен")

        except Exception as e:
            st.error(f"Ошибка: {e}")

    # ===========================
    # PREVIEW
    # ===========================
    st.markdown("---")
    st.subheader("👁 Предпросмотр")

    st.code(st.session_state.get(f"text_{idx}", ""), language="python")

    st.markdown("**Ответ:**")
    st.write(st.session_state.get(f"answer_{idx}", ""))

    # ===========================
    # STATISTICS
    # ===========================
    st.markdown("---")
    st.subheader("📊 Статистика Bloom")

    counts = st.session_state.df["bloom"].value_counts()

    for k, v in bloom_colors.items():
        st.write(f"{k}: {counts.get(k, 0)}")


if __name__ == "__main__":
    run()
