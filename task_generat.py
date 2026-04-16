import requests
import streamlit as st

# ===========================
# TOKEN
# ===========================
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# ===========================
# FREE MODEL (STABLE)
# ===========================
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"


# ===========================
# REQUEST FUNCTION
# ===========================
def generate_questions(topic: str) -> str:
    prompt = f"""
Сгенерируй 5 вопросов по теме: {topic}
Для школьников.
Формат: нумерованный список.
Коротко и понятно.
"""

    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={"inputs": prompt}
    )

    # ❗ если ошибка API — показываем сразу (очень важно для диагностики)
    if response.status_code != 200:
        return f"❌ API ERROR {response.status_code}\n{response.text}"

    try:
        data = response.json()
    except Exception:
        return f"❌ JSON ERROR:\n{response.text}"

    # HF иногда возвращает список
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

    st.title("📝 Генератор вопросов (Free AI)")

    # проверка токена
    if not HF_TOKEN:
        st.error("❌ HF_TOKEN не найден в Streamlit Secrets")
        st.stop()

    topic = st.text_input(
        "Введите тему",
        placeholder="например: Python циклы, ООП, физика"
    )

    if st.button("Сгенерировать"):
        if not topic.strip():
            st.warning("Введите тему")
            return

        with st.spinner("Генерация..."):
            result = generate_questions(topic)

        st.subheader("Результат:")
        st.write(result)


# ===========================
# START
# ===========================
if __name__ == "__main__":
    run()
