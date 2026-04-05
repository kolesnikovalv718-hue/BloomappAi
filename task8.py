# task8.py
import streamlit as st
import docx
import pandas as pd
import os
import tempfile
import zipfile

def run():
    st.title("📄 Конвертер Word → CSV (с картинками и формулами)")

    uploaded_file = st.file_uploader("Загрузи Word файл (.docx)", type=["docx"])

    def is_new_task(text):
        return text and text[0].isdigit() and "." in text[:3]

    if uploaded_file:
        if st.button("Обработать файл"):
            with tempfile.TemporaryDirectory() as tmpdir:
                doc_path = os.path.join(tmpdir, "input.docx")
                with open(doc_path, "wb") as f:
                    f.write(uploaded_file.read())

                doc = docx.Document(doc_path)

                tasks = []
                current_task = None
                task_id = 0
                processed_rIds = set()

                for para in doc.paragraphs:
                    text = para.text.strip()
                    if is_new_task(text):
                        if current_task:
                            tasks.append(current_task)
                        task_id += 1
                        current_task = {
                            "id": task_id,
                            "задание": text,
                            "формула": "",
                            "картинки": [],
                            "решение": ""
                        }
                    elif current_task:
                        if text.startswith("Формула"):
                            current_task["формула"] += text.replace("Формула:", "").strip()
                        elif text.startswith("Решение"):
                            current_task["решение"] += text.replace("Решение:", "").strip()
                        elif text:
                            current_task["задание"] += "\n" + text

                    # Картинки
                    for rel in doc.part.rels.values():
                        if "image" in rel.target_ref and rel.rId not in processed_rIds:
                            img_data = rel.target_part.blob
                            img_name = f"img_{task_id}_{len(current_task['картинки'])}.png"
                            img_path = os.path.join(tmpdir, img_name)
                            with open(img_path, "wb") as f:
                                f.write(img_data)
                            current_task["картинки"].append(img_name)
                            processed_rIds.add(rel.rId)

                if current_task:
                    tasks.append(current_task)

                # CSV
                for t in tasks:
                    t["картинки"] = ";".join(t["картинки"])
                df = pd.DataFrame(tasks)
                csv_path = os.path.join(tmpdir, "dataset.csv")
                df.to_csv(csv_path, index=False, encoding='utf-8-sig')

                # ZIP
                zip_path = os.path.join(tmpdir, "dataset.zip")
                with zipfile.ZipFile(zip_path, "w") as zipf:
                    zipf.write(csv_path, "dataset.csv")
                    for file in os.listdir(tmpdir):
                        if file.endswith(".png"):
                            zipf.write(os.path.join(tmpdir, file), f"images/{file}")

                st.success("✅ Файл обработан!")
                st.dataframe(df)

                with open(zip_path, "rb") as f:
                    st.download_button(
                        label="📦 Скачать CSV + картинки",
                        data=f,
                        file_name="dataset.zip",
                        mime="application/zip"
                    )

                st.subheader("Формулы (LaTeX)")
                for t in tasks:
                    if t["формула"]:
                        st.write(f"Задача {t['id']}:")
                        st.latex(t["формула"])
