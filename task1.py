import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components

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
    # Функции для работы с задачей
    # ---------------------------
    def save_current_task():
        idx = st.session_state.current_index
        st.session_state.df.loc[idx, "text"] = st.session_state.get(f"text_{idx}", "")
        st.session_state.df.loc[idx, "answer"] = st.session_state.get(f"answer_{idx}", "")
        st.session_state.df.loc[idx, "topic"] = st.session_state.get(f"topic_{idx}", "")
        st.session_state.df.loc[idx, "interdisciplinary"] = st.session_state.get(f"inter_{idx}", "")
        st.session_state.df.loc[idx, "bloom"] = st.session_state.get(f"bloom_{idx}", "Remembering")

    def save_csv():
        save_current_task()
        st.session_state.df.to_csv(file_path, index=False, encoding='utf-8')
        st.success(f"Сохранено! Файл: {file_path}")

    def render_task(idx):
        st.text_area("Задача:", value=st.session_state.df.loc[idx, "text"], key=f"text_{idx}", height=80)
        st.text_area("Ответ:", value=st.session_state.df.loc[idx, "answer"], key=f"answer_{idx}", height=80)
        st.text_input("Тема:", value=st.session_state.df.loc[idx, "topic"], key=f"topic_{idx}")
        st.text_input("Междисциплинарная:", value=st.session_state.df.loc[idx, "interdisciplinary"], key=f"inter_{idx}")
        bloom_val = st.selectbox("Bloom:", options=list(bloom_colors.keys()),
                                 index=list(bloom_colors.keys()).index(st.session_state.df.loc[idx, "bloom"]),
                                 key=f"bloom_{idx}")
        st.markdown(f"**Bloom:** <span style='color:{bloom_colors[bloom_val]}'>{bloom_val}</span>", unsafe_allow_html=True)

        # LaTeX preview
        st.markdown("---")
        st.subheader("Предпросмотр задачи")
        st.markdown(st.session_state.get(f"text_{idx}", ""), unsafe_allow_html=True)
        st.markdown("**Ответ:**")
        st.markdown(st.session_state.get(f"answer_{idx}", ""), unsafe_allow_html=True)

        # Python code editor
        st.markdown("---")
        st.subheader("🖥 Редактор Python-кода")
        code_val = st.text_area("Код:", key=f"code_{idx}", height=120)

        run_col, check_col, solution_col = st.columns([1,1,1])
        with run_col:
            if st.button("Выполнить код", key=f"run_{idx}"):
                with st.expander("Результат выполнения", expanded=True):
                    try:
                        local_vars = {}
                        exec(code_val, {}, local_vars)
                        if "result" in local_vars:
                            st.write("Результат:", local_vars["result"])
                        else:
                            st.write("Код выполнен")
                    except Exception as e:
                        st.error(f"Ошибка выполнения: {e}")

        with check_col:
            if st.button("Проверить", key=f"check_{idx}"):
                correct = st.session_state.df.loc[idx, "answer"]
                if code_val.strip() == str(correct).strip():
                    st.success("✅ Правильно!")
                else:
                    st.error(f"❌ Неправильно. Правильный ответ:\n{correct}")

        with solution_col:
            if st.button("Показать решение", key=f"sol_{idx}"):
                solution = st.session_state.df.loc[idx, "answer"]
                if solution.strip() == "":
                    st.info("💡 Решение пока недоступно")
                else:
                    st.info(f"💡 Решение:\n{solution}")

    # ---------------------------
    # Навигация без st.experimental_rerun
    # ---------------------------
    def next_task():
        save_current_task()
        if st.session_state.current_index < len(st.session_state.df) - 1:
            st.session_state.current_index += 1

    def prev_task():
        save_current_task()
        if st.session_state.current_index > 0:
            st.session_state.current_index -= 1

    def add_task():
        save_current_task()
        new_row = {"text": "", "answer": "", "level": "", "bloom": "Remembering", "topic": "", "interdisciplinary": ""}
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
        st.session_state.current_index = len(st.session_state.df) - 1

    def delete_task():
        save_current_task()
        idx = st.session_state.current_index
        if len(st.session_state.df) > 0:
            st.session_state.df.drop(idx, inplace=True)
            st.session_state.df.reset_index(drop=True, inplace=True)
            st.session_state.current_index = max(0, idx-1)

    # ---------------------------
    # Навигационные кнопки в одну строку с разными цветами
    # ---------------------------
    st.title("Редактор задач с Bloom + LaTeX + Python")
    st.info(f"Всего задач: {len(st.session_state.df)}")

    buttons_html = f"""
    <div style="display:flex; gap:10px; margin-bottom:20px;">
      <button onclick="window.parent.postMessage({{func:'prev_task'}}, '*')" style="flex:1; background:#6c757d; color:white; border:none; padding:10px 20px; border-radius:10px; cursor:pointer;">Предыдущая</button>
      <button onclick="window.parent.postMessage({{func:'next_task'}}, '*')" style="flex:1; background:#0d6efd; color:white; border:none; padding:10px 20px; border-radius:10px; cursor:pointer;">Следующая</button>
      <button onclick="window.parent.postMessage({{func:'add_task'}}, '*')" style="flex:1; background:#198754; color:white; border:none; padding:10px 20px; border-radius:10px; cursor:pointer;">Добавить</button>
      <button onclick="window.parent.postMessage({{func:'save_csv'}}, '*')" style="flex:1; background:#ffc107; color:white; border:none; padding:10px 20px; border-radius:10px; cursor:pointer;">Сохранить</button>
      <button onclick="window.parent.postMessage({{func:'download_csv'}}, '*')" style="flex:1; background:#0dcaf0; color:white; border:none; padding:10px 20px; border-radius:10px; cursor:pointer;">Скачать CSV</button>
      <button onclick="window.parent.postMessage({{func:'delete_task'}}, '*')" style="flex:1; background:#dc3545; color:white; border:none; padding:10px 20px; border-radius:10px; cursor:pointer;">Удалить</button>
    </div>
    <style>
    button:hover {{
        transform: scale(1.05);
        transition: all 0.2s ease;
    }}
    </style>
    """
    components.html(buttons_html, height=70)

    # ---------------------------
    # Рендер текущей задачи
    # ---------------------------
    if len(st.session_state.df) > 0:
        render_task(st.session_state.current_index)
    else:
        st.warning("Нет задач")

    # ---------------------------
    # Фильтры и список задач снизу
    # ---------------------------
    st.markdown("---")
    st.header("Список задач")
    filter_topic = st.text_input("Фильтр по теме (снизу):")
    filter_bloom = st.selectbox("Фильтр Bloom (снизу):", options=["Все"] + list(bloom_colors.keys()))

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
            st.markdown(
                f"---\n**№ {i+1}**: {row['text']}\n**Bloom:** <span style='color:{color}'>{row['bloom']}</span>\n**Тема:** {row['topic']}",
                unsafe_allow_html=True
            )

    # ---------------------------
    # Статистика Bloom
    # ---------------------------
    st.markdown("---")
    st.header("📊 Статистика по уровням Bloom")
    counts = st.session_state.df['bloom'].value_counts()
    for bloom, color in bloom_colors.items():
        count = counts.get(bloom, 0)
        st.markdown(f"<span style='color:{color}; font-weight:bold'>{bloom}: {count}</span>", unsafe_allow_html=True)
