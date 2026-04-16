import requests
import streamlit as st

# ===========================
# НАСТРОЙКИ API
# ===========================
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# модели (основная + запасная)
MODELS = [
    "mistralai/Mistral-7B-Instruct-v0.2",
    "HuggingFaceH4/zephyr-7b-beta"
]


# ===========================
# ЗАПРОС К API
# ===========================
def ask_model(model: str, prompt: str) -> str:
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=HEADERS, json=data)

    try:
        result = response.json()
    except Exception:
        return f"❌ Ошибка разбора ответа: {response.text}"

    if response.status_code != 200:
        return f"❌ API {response.status_code}: {result}"

    try:
        return result["choices"][0]["message"]["content"]
    except Exception:
        return f"❌ Непонятный формат ответа: {result}"


# ===========================
# ГЕНЕРАЦИЯ С FALLBACK
# ===========================
def generate_questions(topic: str) -> str:
    prompt = f"""
Сгенерируй 5 чётких вопросов по теме: "{topic}"
Для школьников. Без лишнего текста.
Нумерованный список.
"""

    for model in MODELS:
        result = ask_model(model, prompt)

        # если модель сработала — выходим
        if not result.startswith("❌"):
            return result

    return "❌ Все модели недоступны. Попробуй позже."


# ===========================
# STREAMLIT UI
# ===========================
def run():
    st.set_page_config(
        page_title="Генератор вопросов",
        page_icon="📝",
        layout="centered"
    )

    st.title("📝 Генератор вопросов для школьников")

    # проверка токена сразу
    if not HF_TOKEN:
        st.error("❌ HF_TOKEN не найден в Secrets")
        st.stop()

    topic = st.text_input(
        "Введите тему",
        placeholder="например: циклы Python, закон Ома, базы данных"
    )

    if st.button("Сгенерировать"):
        if not topic.strip():
            st.warning("Введите тему!")
            return

        with st.spinner("Генерируем вопросы..."):
            result = generate_questions(topic)

        st.subheader("Результат:")
        st.write(result)
