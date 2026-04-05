import streamlit as st
import pandas as pd
import os

def run():
    # ---------------------------
    # Путь к CSV
    # ---------------------------
    file_path = "blooms_dataset.csv"

    # ---------------------------
    # Загрузка или создание CSV
    # ---------------------------
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

    # ---------------------------
    # Session state
    # ---------------------------
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

    # ---------------------------
    # Фильтры сверху
    # ---------------------------
    st.header("Фильтр задач")
    filter_topic = st.text_input("Фильтр по теме:", "")
    filter_bloom = st.selectbox("Фильтр Bloom:", options=["Все"] + list(bloom_colors.keys()))

    filtered_df = st.session_state.df.copy()
    if filter_topic:
        filtered_df = filtered_df[filtered_df["topic"].str.lower().str.contains(filter_topic.lower())]
    if filter_bloom != "Все":
        filtered_df = filtered_df[filtered_df["bloom"] == filter_bloom]

    if len(filtered_df) == 0:
        st.warning("По фильтру нет задач")
    else:
        st.info(f"Задач после фильтра: {len(filtered_df)}")

    # ---------------------------
    # Функции для работы с задачей
    # ---------------------------
    def save_current_task():
        idx = st.session_state.current_index
        st.session_state.df.loc[idx, "text"] = st.session_state.get(f"text_{idx}", "")
        st.session_state.df.loc[idx, "answer"] = st.session_state.get(f"answer_{idx}", "")
        st.session_state.df.loc[idx, "topic"] = st.session_state.get(f"topic_{idx
