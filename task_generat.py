import requests
import streamlit as st

# ===========================
# ТОКЕН
# ===========================
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# ===========================
# БЕСПЛАТНАЯ МОДЕЛЬ (СТАБИЛЬНАЯ)
# ===========================
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"


# ===========================
# ЗАПРОС К МОДЕЛИ
# ===========================
def generate_questions(topic: str) -> str:
    prompt = f"""
Сгенерируй 5 вопросов по теме: {topic}.
Уровень: школьники.
Формат: нумерованный список.
Коротко и понятно.
"""

    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={"inputs": prompt}
    )

    # если модель "просыпается"
    try:
        data = response.json()
    except Exception:
        return f"❌ Ошибка ответа API: {response.text}"

    # обработка ошибок HF
    if response.status_code != 200:
        return f"❌ API ошибка {response.status_code}: {data}"

    # иногда HF возвращает список
    if isinstance(data, list):
        return data[0].get("generated_text", str(data))

    return str(data)


# ===========================
# STREAMLIT UI
# ===========================
def run():
    st.set_page_config(
        page_title="Генератор вопросов",
        page_icon="📝",
        layout="centered"
    )

    st.title("📝 Генератор вопросов (бесплатный AI)")

    # проверка токена
    if not HF_TOKEN:
        st.error("❌ Добавь HF_TOKEN в Streamlit Secrets")
        st.stop()

    topic = st.text_input(
        "Введите тему",
        placeholder="например: Python циклы, ООП, физика закон Ома"
    )

    if st.button("Сгенерировать"):
        if not topic.strip():
            st.warning("Введите тему!")
            return

        with st.spinner("Генерирую вопросы..."):
            result = generate_questions(topic)

        st.subheader("Результат:")
        st.write(result)


# ===========================
# ЗАПУСК
# ===========================
if __name__ == "__main__":
    run()
