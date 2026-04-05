import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# -------------------------------------------------
# Task 3: Страница анализа и статистики модели
# Здесь отображаются: точность, отчет классификации,
# матрица ошибок, графики метрик и анализ сильных/слабых классов
# -------------------------------------------------
def run():
    st.title("📊 Статистика и анализ модели")
    st.markdown("---")

    file_path = "blooms_dataset.csv"

    if st.button("Запустить анализ"):

        if not os.path.exists(file_path):
            st.error("Файл не найден")
            return

        df = pd.read_csv(file_path)

        if "text" not in df.columns or "bloom" not in df.columns:
            st.error("Нет нужных колонок (text, bloom)")
            return

        X = df["text"]
        y = df["bloom"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_test_tfidf = vectorizer.transform(X_test)

        model = LogisticRegression(max_iter=1000, class_weight='balanced')
        model.fit(X_train_tfidf, y_train)

        y_pred = model.predict(X_test_tfidf)

        # -------------------
        # Точность
        # -------------------
        accuracy = accuracy_score(y_test, y_pred)
        st.success(f"Точность: {accuracy:.2%}")

        # -------------------
        # Отчет классификации
        # -------------------
        report = classification_report(y_test, y_pred, output_dict=True, zero_division=1)
        report_df = pd.DataFrame(report).transpose()

        st.subheader("Метрики")
        st.dataframe(report_df)

        # -------------------
        # Матрица ошибок
        # -------------------
        conf_matrix = confusion_matrix(y_test, y_pred)

        fig, ax = plt.subplots()
        sns.heatmap(
            conf_matrix,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=model.classes_,
            yticklabels=model.classes_,
            ax=ax
        )
        ax.set_title("Матрица ошибок")
        ax.set_xlabel("Предсказано")
        ax.set_ylabel("Истинно")

        st.pyplot(fig)

        # -------------------
        # График метрик
        # -------------------
        metrics_df = report_df[['precision', 'recall', 'f1-score']].drop("accuracy", errors="ignore")

        st.subheader("Сравнение метрик")
        st.bar_chart(metrics_df)

        # -------------------
        # Анализ классов
        # -------------------
        st.subheader("Анализ классов")

        strong = []
        weak = []

        for idx, cls in enumerate(model.classes_):
            correct = conf_matrix[idx, idx]
            total = conf_matrix[idx, :].sum()

            if total == 0:
                continue

            percent = correct / total

            st.write(f"**{cls}**: {percent:.0%} правильно")

            if percent >= 0.8:
                strong.append(cls)
            elif percent < 0.6:
                weak.append(cls)

        st.markdown("---")

        if strong:
            st.success(f"Сильные: {', '.join(strong)}")
        if weak:
            st.warning(f"Слабые: {', '.join(weak)}")

        if weak:
            st.info("Рекомендуется добавить больше задач в слабые классы")
