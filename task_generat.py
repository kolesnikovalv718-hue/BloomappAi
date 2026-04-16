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
    "🟢 Бесплатная (стабильная)": {
        "type": "inference",
        "url": "https://api-inference.huggingface.co/models/google/flan-t5-large"
    },
    "🟡 Mistral (иногда работает)": {
        "type": "router",
        "model": "mistralai/Mistral-7B-Instruct-v0.2"
    },
    "🟡 Zephyr (иногда работает)": {
        "type": "router",
        "model": "HuggingFaceH4/zephyr-7b-beta"
    }
}


# ===========================
# INFERENCE API
# ===========================
def ask_inference(url, prompt):
    response = requests.post(url, headers=HEADERS, json={"inputs": prompt})

    try:
        data = response.json()
    except Exception:
        return f"❌ Ошибка: {response.text}"

    if response.status_code != 200:
        return f"❌ API {response.status_code}: {data}"

    return data[0].get("generated_text", str(data))


# ===========================
# ROUTER API
# ===========================
def ask_router(model, prompt):
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
        return f"❌ Ошибка: {response.text}"

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

    if config["type"] == "inference":
        return ask_inference(config["url"], prompt)

    elif config["type"] == "router":
        result = ask_router(config["model"], prompt)

        # fallback если упало
        if result.startswith("❌"):
            fallback = MODELS["🟢 Бесплатная (стабильная)"]
            return ask_inference(fallback["url"], prompt)

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
        st.error("❌ HF_TOKEN не найден")
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
