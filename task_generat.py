import requests
import streamlit as st

# ===========================
# TOKEN
# ===========================
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

# ===========================
# MODEL
# ===========================
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}


# ===========================
# DEBUG PRINTS
# ===========================
def debug_info():
    st.write("========== DEBUG INFO ==========")
    st.write("HF_TOKEN exists:", bool(HF_TOKEN))
    st.write("API_URL:", API_URL)
    st.write("HEADERS:", {"Authorization": "Bearer ***" if HF_TOKEN else "MISSING"})
    st.write("================================")


# ===========================
# REQUEST FUNCTION (MAX LOGGING)
# ===========================
def generate_questions(topic: str):

    st.write("========== REQUEST START ==========")
    st.write("Input topic:", topic)

    prompt = f"Сгенерируй 5 вопросов по теме: {topic}"

    payload = {"inputs": prompt}

    st.write("Payload:", payload)
    st.write("Sending POST request...")

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            timeout=30
        )
    except Exception as e:
        return f"❌ REQUEST EXCEPTION: {e}"

    # ===========================
    # RAW RESPONSE
    # ===========================
    st.write("========== RESPONSE RECEIVED ==========")
    st.write("Status code:", response.status_code)
    st.write("Response headers:", dict(response.headers))
    st.write("Raw text (first 500 chars):")
    st.code(response.text[:500])

    # ===========================
    # PARSE JSON
    # ===========================
    try:
        data = response.json()
    except Exception as e:
        return f"❌ JSON PARSE ERROR: {e}\nRAW: {response.text}"

    st.write("Parsed JSON:", data)

    # ===========================
    # ERROR HANDLING
    # ===========================
    if response.status_code != 200:
        return f"❌ API ERROR {response.status_code}\n{data}"

    # ===========================
    # OUTPUT
    # ===========================
    if isinstance(data, list):
        return data[0].get("generated_text", str(data))

    return str(data)


# ===========================
# STREAMLIT UI
# ===========================
def run():

    st.set_page_config(
        page_title="HF DEBUG APP",
        page_icon="🧪",
        layout="centered"
    )

    st.title("🧪 HF DEBUG MODE (полная диагностика)")

    debug_info()

    if not HF_TOKEN:
        st.error("❌ HF_TOKEN отсутствует в secrets")
        st.stop()

    topic = st.text_input("Введите тему")

    if st.button("ТЕСТ ЗАПРОСА"):

        if not topic.strip():
            st.warning("Введите тему")
            return

        result = generate_questions(topic)

        st.subheader("FINAL RESULT")
        st.write(result)


# ===========================
# RUN
# ===========================
if __name__ == "__main__":
    run()
