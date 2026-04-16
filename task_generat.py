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
# STABLE MODEL (free inference)
# ===========================
API_URL = "https://api-inference.huggingface.co/models/microsoft/phi-2"


# ===========================
# FULL DEBUG INFO
# ===========================
def debug_info():
    st.write("========== DEBUG INFO ==========")
    st.write("HF_TOKEN exists:", bool(HF_TOKEN))
    st.write("API_URL:", API_URL)
    st.write("MODEL TYPE: inference API (NO /models/google)")
    st.write("================================")


# ===========================
# REQUEST WITH FULL LOGGING
# ===========================
def generate_questions(topic: str):

    st.write("========== REQUEST START ==========")
    st.write("Input topic:", topic)

    prompt = f"Сгенерируй 5 школьных вопросов по теме: {topic}"

    payload = {
        "inputs": prompt
    }

    st.write("Payload:", payload)
    st.write("Sending request to HF...")

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            timeout=60
        )
    except Exception as e:
        return f"❌ REQUEST ERROR: {e}"

    # ===========================
    # RESPONSE DEBUG
    # ===========================
    st.write("========== RESPONSE RECEIVED ==========")
    st.write("Status code:", response.status_code)
    st.write("Headers:", dict(response.headers))
    st.write("Raw text (first 800 chars):")
    st.code(response.text[:800])

    # ===========================
    # JSON PARSE
    # ===========================
    try:
        data = response.json()
    except Exception as e:
        return f"❌ JSON ERROR: {e}\nRAW:\n{response.text}"

    st.write("Parsed JSON:", data)

    # ===========================
    # ERROR CHECK
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
        page_title="HF DEBUG FIXED",
        page_icon="🧪",
        layout="centered"
    )

    st.title("🧪 HF DEBUG FIX (working version)")

    debug_info()

    if not HF_TOKEN:
        st.error("❌ HF_TOKEN missing in Streamlit secrets")
        st.stop()

    topic = st.text_input("Введите тему")

    if st.button("ТЕСТ"):

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
