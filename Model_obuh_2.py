import streamlit as st
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

st.title("Обучение модели")

st.markdown("---")

if st.button("Обучить модель"):
    st.write("Запуск...")

    file_path = "blooms_dataset.csv"

    if not os.path.exists(file_path):
        st.error("Файл не найден")
    else:
        df = pd.read_csv(file_path, encoding="utf-8")

        # Проверка колонок
        if "text" not in df.columns or "bloom" not in df.columns:
            st.error("Нет нужных колонок (text, bloom)")
        else:
            X = df["text"]
            y = df["bloom"]

            # Разделение данных
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # Векторизация текста
            vectorizer = TfidfVectorizer()
            X_train_vec = vectorizer.fit_transform(X_train)

            # Обучение модели
            model = LogisticRegression()
            model.fit(X_train_vec, y_train)

            st.success("Модель обучена 🎉")
            st.write(f"Обучение: {len(X_train)}")
            st.write(f"Тест: {len(X_test)}")
