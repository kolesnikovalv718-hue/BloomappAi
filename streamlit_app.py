import streamlit as st
import pandas as pd
import os

# ---------------------------
# Стили кнопок
# ---------------------------
st.markdown("""
<style>
button {
    background-color: #4CAF50 !important;
    color: white !important;
    border-radius: 8px !important;
    margin: 2px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# CSV
# ---------------------------
file_path = "blooms_dataset.csv"

uploaded_file = st.file_uploader("Загрузите CSV с задачами", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.success(f"Загружено {len(df)} задач из CSV.")
elif os.path.exists(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    st.success(f"Файл найден. Загружено {len(df)} задач.")
else:
    df = pd.DataFrame({
        "text": ["Пример:\n$$ P(6)=\\frac{1}{6} $$"],
        "answer": [""],
        "level": ["Знание"],
        "bloom": ["Remembering"],
        "topic": ["Probability"],
        "interdisciplinary": [""]
    })
    df.to_csv(file_path, index=False, encoding='utf-8')

df = df.fillna("")

bloom_colors = {
    "Remembering": "gray",
    "Understanding": "blue",
    "Applying": "green",
    "Analyzing": "orange",
    "Evaluating": "red",
    "Creating": "purple"
}

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# ---------------------------
# Функции
# ---------------------------
def save_csv():
    global df
    idx = st.session_state.current_index
    if len(df) > 0:
        # Обновляем df из текущих значений редактирования
        df.loc[idx, "text"] = st.session_state.get(f"text_{idx}", df.loc[idx, "text"])
        df.loc[idx, "answer"] = st.session_state.get(f"answer_{idx}", df.loc[idx, "answer"])
        df.loc[idx, "topic"] = st.session_state.get(f"topic_{idx}", df.loc[idx, "topic"])
        df.loc[idx, "interdisciplinary"] = st.session_state.get(f"inter_{idx}", df.loc[idx, "interdisciplinary"])
        df.loc[idx, "bloom"] = st.session_state.get(f"bloom_{idx}", df.loc[idx, "bloom"])

    try:
        df.to_csv(file_path, index=False, encoding="utf-8")
        st.success(f"Сохранено! Файл: {file_path}")
    except Exception as e:
        st.error(f"Ошибка при сохранении: {e}")
def render_task(idx):
    task = df.loc[idx]
    task["text"] = st.text_area("Задача:", value=task["text"], key=f"text_{idx}")
    task["answer"] = st.text_area("Ответ:", value=task["answer"], key=f"answer_{idx}")
    task["topic"] = st.text_input("Тема:", value=task["topic"], key=f"topic_{idx}")
    task["interdisciplinary"] = st.text_input("Междисциплинарная:", value=task["interdisciplinary"], key=f"inter_{idx}")
    task["bloom"] = st.selectbox("Bloom:", options=list(bloom_colors.keys()),
                                 index=list(bloom_colors.keys()).index(task["bloom"]), key=f"bloom_{idx}")
    df.loc[idx] = task
    st.markdown(f"**Bloom:** <span style='color:{bloom_colors[task['bloom']]}'>{task['bloom']}</span>",
                unsafe_allow_html=True)

def prev_task():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1

def next_task():
    if st.session_state.current_index < len(df) - 1:
        st.session_state.current_index += 1

def add_task(
    
):
    global df
    new_row = {"text": "", "answer": "", "level": "", "bloom": "Remembering", "topic": "", "interdisciplinary": ""}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    st.session_state.current_index = len(df) - 1
    st.rerun()

# ---------------------------
# Заголовок и кнопки сверху
# ---------------------------
st.title("Редактор задач с Bloom")
cols = st.columns([1,1,1,1])
with cols[0]:
    if st.button("Предыдущая"):
        prev_task()
with cols[1]:
    if st.button("Следующая"):
        next_task()
with cols[2]:
    if st.button("Добавить задачу"):
        add_task()
with cols[3]:
    if st.button("Сохранить"):
        save_csv()
# ---------------------------
# Кнопка скачивания CSV
# ---------------------------
st.download_button(
    label="Скачать CSV",
    data=open(file_path, "rb").read(),  # читаем файл в байтах
    file_name="blooms_dataset.csv",
    mime="text/csv"
)

# ---------------------------
# Редактор текущей задачи сверху
# ---------------------------
if len(df) > 0:
    render_task(st.session_state.current_index)
else:
    st.warning("Нет задач")

# ---------------------------
# Фильтры и список задач внизу
# ---------------------------
st.sidebar.header("Фильтры")
filter_topic = st.sidebar.text_input("Фильтр по теме:")
filter_bloom = st.sidebar.selectbox("Фильтр Bloom:", options=["Все"] + list(bloom_colors.keys()))

filtered_df = df.copy()
if filter_topic:
    filtered_df = filtered_df[filtered_df["topic"].str.lower().str.contains(filter_topic.lower())]
if filter_bloom != "Все":
    filtered_df = filtered_df[filtered_df["bloom"] == filter_bloom]

st.header("Список задач (с фильтром)")
if len(filtered_df) == 0:
    st.warning("По фильтру нет задач")
else:
    for i, row in filtered_df.iterrows():
        color = bloom_colors.get(row["bloom"], "black")
        st.markdown(f"**№ {i+1}**: {row['text']}")
        st.markdown(f"Bloom: <span style='color:{color}'>{row['bloom']}</span>", unsafe_allow_html=True)
        st.markdown(f"Тема: {row['topic']}")
        st.markdown("---")
