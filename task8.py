# task8.py экспорт из ворд доработать 
import streamlit as st
import docx
import pandas as pd
import os
import tempfile
import zipfile

def run():
    st.title("📄 Конвертер Word → CSV (с картинками и формулами)")

    uploaded_file = st.file_uploader("Загрузи Word файл (.docx)", type=["docx"])

    # Функция для определения новой задачи
    def is_new_task(text):
        return text and text[0].isdigit() and "." in text[:3]

    if uploaded_file:
        if st.button("Обработать файл"):
            with tempfile.TemporaryDirectory() as tmpdir:
                # Сохраняем загруженный Word во временной папке
                doc_path = os.path.join(tmpdir, "input.docx")
                with open(doc_path, "wb") as f:
                    f.write(uploaded_file.read())

                doc = docx.Document(doc_path)

                tasks = []
                current_task = None
                task_id = 0
                processed_rIds = set()  # чтобы картинки не дублировались

                # ===== Обработка параграфов и картинок =====
                for para in doc.paragraphs:
                    text = para.text.strip()

                    # --- новая задача ---
                    if is_new_task(text):
                        if current_task:
                            tasks.append(current_task)
                        task_id += 1
                        current_task = {
                            "id": task_id,
                            "задание": text or "",
                            "формула": "",
                            "картинки": [],
                            "решение": ""
                        }

                    elif current_task:
                        if text.startswith("Формула"):
                            current_task["формула"] = (current_task.get("формула") or "") + "\n" + text.replace("Формула:", "").strip()
                        elif text.startswith("Решение"):
                            current_task["решение"] = (current_task.get("решение") or "") + "\n" + text.replace("Решение:", "").strip()
                        elif text:
                            current_task["задание"] = (current_task.get("задание") or "") + "\n" + text

                    # --- ищем картинки ---
                    for rel in doc.part.rels.values():
                        if "image" in rel.target_ref and rel.rId not in processed_rIds:
                            if current_task:  # проверка, чтобы не было TypeError
                                img_data = rel.target_part.blob
                                img_name = f"img_{task_id}_{len(current_task['картинки'])}.png"
                                img_path = os.path.join(tmpdir, img_name)
                                with open(img_path, "wb") as f:
                                    f.write(img_data)
                                current_task["картинки"].append(img_name)
                                processed_rIds.add(rel.rId)

                # добавляем последнюю задачу
                if current_task:
                    tasks.append(current_task)

                # ===== Подготовка CSV =====
                for t in tasks:
                    t["картинки"] = ";".join(t["картинки"])
                df = pd.DataFrame(tasks)
                csv_path = os.path.join(tmpdir, "dataset.csv")
                df.to_csv(csv_path, index=False, encoding='utf-8-sig')

                # ===== Создание ZIP =====
                zip_path = os.path.join(tmpdir, "dataset.zip")
                with zipfile.ZipFile(zip_path, "w") as zipf:
                    zipf.write(csv_path, "dataset.csv")
                    for file in os.listdir(tmpdir):
                        if file.endswith(".png"):
                            zipf.write(os.path.join(tmpdir, file), f"images/{file}")

                st.success("✅ Файл обработан!")
                st.subheader("Таблица с заданиями:")
                st.dataframe(df)

                # ===== Кнопка скачивания ZIP =====
                with open(zip_path, "rb") as f:
                    st.download_button(
                        label="📦 Скачать CSV + картинки",
                        data=f,
                        file_name="dataset.zip",
                        mime="application/zip"
                    )

                # ===== Показ формул через st.latex() =====
                st.subheader("Формулы (LaTeX)")
                for t in tasks:
                    if t.get("формула"):
                        st.write(f"Задача {t['id']}:")
                        st.latex(t["формула"])
