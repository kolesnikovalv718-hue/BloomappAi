import csv

# ---------------------------
# Загрузка или создание CSV
# ---------------------------
if os.path.exists(file_path):
    try:
        df = pd.read_csv(
            file_path,
            encoding='utf-8',
            quotechar='"',       # учитываем кавычки
            quoting=csv.QUOTE_ALL,
            keep_default_na=False  # пустые ячейки не превращаем в NaN
        )
    except Exception as e:
        st.error(f"Ошибка при чтении CSV: {e}")
        df = pd.DataFrame({
            "text": ["Пример:\n$$ P(6)=\\frac{1}{6} $$"],
            "answer": [""],
            "level": ["Знание"],
            "bloom": ["Remembering"],
            "topic": ["Probability"],
            "interdisciplinary": [""]
        })
else:
    df = pd.DataFrame({
        "text": ["Пример:\n$$ P(6)=\\frac{1}{6} $$"],
        "answer": [""],
        "level": ["Знание"],
        "bloom": ["Remembering"],
        "topic": ["Probability"],
        "interdisciplinary": [""]
    })

# На всякий случай заменяем пустые на ""
df = df.fillna("")
