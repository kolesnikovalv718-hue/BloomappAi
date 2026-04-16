
import requests
import streamlit as st

# ===========================
# PUBLIC STABLE ENDPOINT (NO /models)
# ===========================
API_URL = "https://api-inference.huggingface.co/v1/chat/completions"

# токен можно оставить, но даже без него иногда работает
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}


# ===========================
# GENERATE
# ===========================
def generate_questions(topic: str):

    payload = {
        "model": "HuggingFaceH4/zephyr-7b-beta",
        "messages": [
            {
                "role": "user",
                "content": f"Сгенерируй 5 школьных вопросов по теме: {topic}. Нумерованный список."
            }
        ],
        "temperature": 0.7
    }

    st.write("DEBUG URL:", API_URL)
    st.write("DEBUG PAYLOAD:", payload)

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            timeout=60
        )
    except Exception as e:
        return f"❌ REQUEST ERROR: {e}"

    st.write("STATUS:", response.status_code)
    st.write("RAW:", response.text[:500])

    try:
        data = response.json()
    except Exception:
        return f"❌ NOT JSON: {response.text}"

    if response.status_code != 200:
        return f"❌ API ERROR {response.status_code}: {data}"

    return data["choices"][0]["message"]["content"]


# ===========================
# STREAMLIT
# ===========================
def run():
    st.title("🧪 Stable AI Generator (FIXED)")

    topic = st.text_input("Тема")

    if st.button("Сгенерировать"):
        if not topic.strip():
            st.warning("Введите тему")
            return

        result = generate_questions(topic)
        st.write(result)


if __name__ == "__main__":
    run()
