
import streamlit as st
import pandas as pd
import os

# ---------------------------
# Цветные кнопки
# ---------------------------
st.markdown("""
<style>
div.stButton > button:first-child {
    height: 3em;
    border-radius: 8px;
    color: white;
}
div.stButton > button:nth-child(1) {background-color: gray;}
div.stButton > button:nth-child(2) {background-color: blue;}
div.stButton > button:nth-child(3) {background-color: green;}
div.stButton > button:nth-child(4) {background-color: red;}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Путь к CSV
# ---------------------------
file_path = "blooms_dataset.csv"

# ---------------------------
# Инициализация df в сессии
# ---------------------------
if "df" not in st.session_state:
    if os.path.exists(file_path):
        st.session_state.df = pd.read_csv(file_path, encoding='utf-8').fillna("")
    else:
        st.session_state.df = pd.DataFrame({
            "text": ["Пример:\n$$ P(6)=\\frac{1}{6} $$"],
            "answer": [""],
            "level": ["Знание"],
            "bloom": ["Remembering"],
            "topic": ["Probability"],
            "interdisciplinary": [""]
        })
    st.session_state.current_index = 0

df = st.session_state.df

# ---------------------------
# Цвета Bloom
# ---------------------------
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
    st.session_state.df.to_csv(file_path, index=False, encoding="utf-8")
    st.success(f"Сохранено! Всего задач: {len(st.session_state.df)}")

def render_task(idx):
    task = df.loc[idx]
    task["text"] = st.text_area("Задача:", value=task.get("text",""), key=f"text_{idx}")
    task["answer"] = st.text_area("Ответ:", value=task.get("answer",""), key=f"answer_{idx}")
    task["topic"] = st.text_input("Тема:", value=task.get("topic",""), key=f"topic_{idx}")
    task["interdisciplinary"] = st.text_input("Междисциплинарная:", value=task.get("interdisciplinary",""), key=f"inter_{idx}")
    task["bloom"] = st.selectbox(
        "Bloom:", 
        options=list(bloom_colors.keys()), 
        index=list(bloom_colors.keys()).index(task.get("bloom","Remembering")), 
        key=f"bloom_{idx}"
    )
    st.session_state.df.loc[idx] = task
    st.markdown(
        f"**Bloom:** <span style='color:{bloom_colors[task['bloom']]}'>{task['bloom']}</span>", 
        unsafe_allow_html=True
    )

def prev_task():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1

def next_task():
    if st.session_state.current_index < len(df) - 1:
        st.session_state.current_index += 1

def add_task():
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
    st.experimental_rerun()

# ---------------------------
# Заголовок
# ---------------------------
st.title("Редактор задач с Bloom")

# ---------------------------
# Фильтры
# ---------------------------
st.sidebar.header("Фильтры")
filter_topic = st.sidebar.text_input("Фильтр по теме:")
filter_bloom = st.sidebar.selectbox("Фильтр Bloom:", options=["Все"] + list(bloom_colors.keys()))

# ---------------------------
# Применение фильтров
# ---------------------------
filtered_df = df.copy()
if filter_topic:
    filtered_df = filtered_df[filtered_df["topic"].str.lower().str.contains(filter_topic.lower())]
if filter_bloom != "Все":
    filtered_df = filtered_df[filtered_df["bloom"] == filter_bloom]

# ---------------------------
# Отображение текущей задачи
# ---------------------------
if st.session_state.current_index >= len(df):
    st.session_state.current_index = len(df) - 1

if len(df) > 0:
    render_task(st.session_state.current_index)
else:
    st.warning("Нет задач")

# ---------------------------
# Кнопки управления
# ---------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Предыдущая"):
        prev_task()
with col2:
    if st.button("Следующая"):
        next_task()
with col3:
    if st.button("Добавить задачу"):
        add_task()
with col4:
    if st.button("Сохранить"):
        save_csv()

# ---------------------------
# Список задач
# ---------------------------
st.header("Список задач (с фильтром)")
for i, row in filtered_df.iterrows():
    color = bloom_colors.get(row["bloom"], "black")
    st.markdown(f"**№ {i+1}**: {row['text']}")
    st.markdown(f"Bloom: <span style='color:{color}'>{row['bloom']}</span>", unsafe_allow_html=True)
    st.markdown(f"Тема: {row['topic']}")
    st.markdown("---")
