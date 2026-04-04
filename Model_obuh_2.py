import streamlit as st
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

st.title("Обучение модели")
st.markdown("---")

if st.button("Обучить модель"):
    st.write("Запуск...")

    file_path = "blooms_dataset.csv"

    # Проверка наличия файла
    if not os.path.exists(file_path):
        st.error("Файл не найден")
    else:
        df = pd.read_csv(file_path, encoding="utf-8")

        # Проверка нужных колонок
        if "text" not in df.columns or "bloom" not in df.columns:
            st.error("Нет нужных колонок (text, bloom)")
        else:
            # Разделяем признаки и целевую переменную
            X = df["text"]
            y = df["bloom"]

            # Разделение на обучающую и тестовую выборки
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # TF-IDF векторизация текста
            vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
            X_train_tfidf = vectorizer.fit_transform(X_train)
            X_test_tfidf = vectorizer.transform(X_test)

            # Обучение модели
            model = LogisticRegression(max_iter=1000, class_weight='balanced')
            model.fit(X_train_tfidf, y_train)

            # Предсказание и оценка
            y_pred = model.predict(X_test_tfidf)
            accuracy = accuracy_score(y_test, y_pred)

            st.success(f"Готово ✅ Точность модели: {accuracy:.2%}")
            st.write("Отчет классификации:")
            st.text(classification_report(y_test, y_pred, zero_division=1))

            # Дополнительно: вывод размеров выборок
            st.write(f"Размер обучающей выборки: {len(X_train)}")
            st.write(f"Размер тестовой выборки: {len(X_test)}")
