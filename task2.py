import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def run():

    st.title("Обучение модели")
    st.markdown("---")

    if st.button("Обучить модель"):
        st.info("Запуск обучения... ⏳")

        file_path = "blooms_dataset.csv"

        if not os.path.exists(file_path):
            st.error("Файл не найден")
        else:
            df = pd.read_csv(file_path, encoding="utf-8")

            if "text" not in df.columns or "bloom" not in df.columns:
                st.error("Нет нужных колонок (text, bloom)")
            else:
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

                accuracy = accuracy_score(y_test, y_pred)
                st.success(f"Модель обучена ✅ Точность: {accuracy:.2%}")

                st.subheader("Отчет классификации")
                st.text(classification_report(y_test, y_pred, zero_division=1))

                conf_matrix = confusion_matrix(y_test, y_pred)
                st.subheader("Матрица ошибок")

                plt.figure(figsize=(8,6))
                sns.heatmap(
                    conf_matrix,
                    annot=True,
                    fmt='d',
                    cmap='Blues',
                    xticklabels=model.classes_,
                    yticklabels=model.classes_
                )
                plt.xlabel("Предсказанный класс")
                plt.ylabel("Истинный класс")
                st.pyplot(plt.gcf())
                plt.clf()

                report = classification_report(y_test, y_pred, output_dict=True, zero_division=1)
                metrics_df = pd.DataFrame(report).transpose()
                metrics_df = metrics_df[['precision', 'recall', 'f1-score']]

                st.subheader("Сравнение метрик классификации")
                metrics_df.plot(kind='barh', figsize=(10,6), colormap='viridis')
                plt.xlabel('Значения')
                plt.ylabel('Классы')
                st.pyplot(plt.gcf())
                plt.clf()

                strong_classes = []
                weak_classes = []
                recommend_addition = []

                for idx, cls in enumerate(model.classes_):
                    correct = conf_matrix[idx, idx]
                    total = conf_matrix[idx, :].sum()

                    if total == 0:
                        continue

                    percent_correct = correct / total

                    if percent_correct >= 0.8:
                        strong_classes.append(cls)
                    elif percent_correct < 0.6:
                        weak_classes.append(cls)
                        recommend_addition.append(cls)

                st.subheader("Рекомендации")

                if strong_classes:
                    st.write(f"✅ Сильные классы: {', '.join(strong_classes)}")

                if weak_classes:
                    st.write(f"⚠️ Слабые классы: {', '.join(weak_classes)}")

                if recommend_addition:
                    st.write("💡 Рекомендуется добавить больше задач для этих классов")
                import pickle
                with open('model.pkl', 'wb') as f:
                    pickle.dump(model, f)

                if not strong_classes and not weak_classes:
                    st.write("Все классы распределены равномерно")

                import joblib

                joblib.dump(model, "model.pkl")
                joblib.dump(vectorizer, "vectorizer.pkl")
                st.success("Модель сохранена 💾")
