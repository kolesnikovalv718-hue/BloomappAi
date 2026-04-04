import streamlit as st
import pandas as pd
import os

# ---------------------------
# Настройки CSV
# ---------------------------
file_path = "blooms_dataset.csv"

# ---------------------------
# Загрузка или создание
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

# Заполняем пустые
df = df.fillna("")

# ---------------------------
# Инициализация session_state
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
# Функции
# ---------------------------
def save_csv():
    global df
    idx = st.session_state.current_index
    if len(df) > 0:
        # Берём актуальные значения из редактора
        df.loc[idx, "text"] = st.session_state.get(f"text_{idx}", df.loc[idx, "text"])
        df.loc[idx, "answer"] = st.session_state.get(f"answer_{idx}", df.loc[idx, "answer"])
        df.loc[idx, "topic"] = st.session_state.get(f"topic_{idx}", df.loc[idx, "topic"])
        df.loc[idx, "interdisciplinary"] = st.session_state.get(f"inter_{idx}", df.loc[idx, "interdisciplinary"])
        df.loc[idx, "bloom"] = st.session_state.get(f"bloom_{idx}", df.loc[idx, "bloom"])

    # Теперь точно сохраняем в файл
    df.to_csv(file_path, index=False, encoding="utf-8")
    st.success(f"Сохранено! Файл: {file_path}")

def render_task(idx):
    task = st.session_state.df.loc[idx]
    st.text_area("Задача:", value=task["text"], key=f"text_{idx}", height=80)
    st.text_area("Ответ:", value=task["answer"], key=f"answer_{idx}", height=80)
    st.text_input("Тема:", value=task["topic"], key=f"topic_{idx}")
    st.text_input("Междисциплинарная:", value=task["interdisciplinary"], key=f"inter_{idx}")
    st.selectbox("Bloom:", options=list(bloom_colors.keys()), index=list(bloom_colors.keys()).index(task["bloom"]), key=f"bloom_{idx}")
    st.markdown(f"**Bloom:** <span style='color:{bloom_colors[task['bloom']]}'>{task['bloom']}</span>", unsafe_allow_html=True)

def prev_task():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1

def next_task():
    if st.session_state.current_index < len(st.session_state.df) - 1:
        st.session_state.current_index += 1

def add_task():
    new_row = {"text": "", "answer": "", "level": "", "bloom": "Remembering", "topic": "", "interdisciplinary": ""}
    st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
    st.session_state.current_index = len(st.session_state.df) - 1

def delete_task():
    idx = st.session_state.current_index
    if len(st.session_state.df) > 0:
        st.session_state.df.drop(idx, inplace=True)
        st.session_state.df.reset_index(drop=True, inplace=True)
        st.session_state.current_index = max(0, idx-1)

# ---------------------------
# Заголовок и информация
# ---------------------------
st.title("Редактор задач с Bloom")
st.info(f"Всего задач: {len(st.session_state.df)}")

# ---------------------------
# Кнопки управления в одной линии
# ---------------------------
cols = st.columns(6)
with cols[0]:
    if st.button("Предыдущая"):
        prev_task()
with cols[1]:
    if st.button("Следующая"):
        next_task()
with cols[2]:
    if st.button("Добавить"):
        add_task()
with cols[3]:
    if st.button("Сохранить"):
        save_csv()
with cols[4]:
    st.download_button(
        label="Скачать CSV",
        data=st.session_state.df.to_csv(index=False).encode("utf-8"),
        file_name="blooms_dataset.csv",
        mime="text/csv"
    )
with cols[5]:
    if st.button("Удалить"):
        delete_task()

st.markdown("---")

# ---------------------------
# Редактор текущей задачи
# ---------------------------
if len(st.session_state.df) > 0:
    render_task(st.session_state.current_index)
else:
    st.warning("Нет задач")

st.markdown("---")

# ---------------------------
# Фильтры и список задач
# ---------------------------
st.header("Список задач")
filter_topic = st.text_input("Фильтр по теме:")
filter_bloom = st.selectbox("Фильтр Bloom:", options=["Все"] + list(bloom_colors.keys()))

filtered_df = st.session_state.df.copy()
if filter_topic:
    filtered_df = filtered_df[filtered_df["topic"].str.lower().str.contains(filter_topic.lower())]
if filter_bloom != "Все":
    filtered_df = filtered_df[filtered_df["bloom"] == filter_bloom]

if len(filtered_df) == 0:
    st.warning("По фильтру нет задач")
else:
    for i, row in filtered_df.iterrows():
        color = bloom_colors.get(row["bloom"], "black")
        st.markdown(f"---\n**№ {i+1}**: {row['text']}\n**Bloom:** <span style='color:{color}'>{row['bloom']}</span>\n**Тема:** {row['topic']}", unsafe_allow_html=True)
