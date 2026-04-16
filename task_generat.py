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
# МОДЕЛИ
# ===========================
MODELS = {
    "🟢 Бесплатная (работает всегда)": {
        "type": "inference",
        "url": "https://api-inference.huggingface.co/models/google/flan-t5-large"
    },
    "🟡 Mistral (может не работать)": {
        "type": "router",
        "model": "mistralai/Mistral-7B-Instruct-v0.2"
    },
    "🟡 Zephyr (может не работать)": {
        "type": "router",
        "model": "HuggingFaceH4/zephyr-7b-beta"
    }
}

# ===========================
# INFERENCE API (ТОЛЬКО ЭТОТ URL)
# ===========================
def ask_inference(prompt: str) -> str:
    url = "https://api-inference.huggingface.co/models/google/flan-t5-large"

    response = requests.post(
        url,
        headers=HEADERS,
        json={"inputs": prompt}
    )

    try:
        data = response.json()
    except Exception:
        return f"❌ RAW ответ: {response.text}"

    if response.status_code != 200:
        return f"❌ API {response.status_code}: {data}"

    return data[0].get("generated_text", str(data))


# ===========================
# ROUTER API
# ===========================
def ask_router(model: str, prompt: str) -> str:
    url = "https://router.huggingface.co/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        result = response.json()
    except Exception:
        return f"❌ RAW ответ: {response.text}"

    if response.status_code != 200:
        return f"❌ API {response.status_code}: {result}"

    try:
        return result["choices"][0]["message"]["content"]
    except Exception:
        return f"❌ Формат ответа: {result}"


# ===========================
# ГЕНЕРАЦИЯ
# ===========================
def generate_questions(topic: str, model_choice: str) -> str:
    prompt = f"""
Сгенерируй 5 вопросов по теме: "{topic}"
Для школьников.
Нумерованный список.
"""

    config = MODELS[model_choice]

    # 🟢 бесплатная модель
    if config["type"] == "inference":
        return ask_inference(prompt)

    # 🟡 router модели
    if config["type"] == "router":
        result = ask_router(config["model"], prompt)

        # fallback если не работает
        if result.startswith("❌"):
            return ask_inference(prompt)

        return result


# ===========================
# UI
# ===========================
def run():
    st.set_page_config(
        page_title="Генератор вопросов",
        page_icon="📝",
        layout="centered"
    )

    st.title("📝 Генератор вопросов")

    if not HF_TOKEN:
        st.error("❌ HF_TOKEN не найден в Secrets")
        st.stop()

    topic = st.text_input("Введите тему")

    model_choice = st.selectbox(
        "Выбери модель",
        list(MODELS.keys())
    )

    if st.button("Сгенерировать"):
        if not topic.strip():
            st.warning("Введите тему!")
            return

        with st.spinner("Генерируем..."):
            result = generate_questions(topic, model_choice)

        st.subheader("Результат:")
        st.write(result)


# запуск
if __name__ == "__main__":
    run()
