# ---------------------------
# Task6 для ученика с объяснением ИИ
# ------------------------
# ---------------------------
# Импорт для локальной модели
# ---------------------------
from pathlib import Path
from gpt4all import GPT4All  # pip install gpt4all

# ---------------------------
# Инициализация модели (один раз)
# ---------------------------
model_path = "ggml-gpt4all-j-v1.3-groovy.bin"  # загрузи модель заранее
gpt_model = GPT4All(model_path)

def gpt_explain(task_text):
    """
    Генерирует пояснение к задаче от локальной модели ИИ без ключа
    """
    prompt = (
        f"Объясни кратко и понятно задачу ученику, без раскрытия ответа:\n{task_text}\nПояснение:"
    )
    # Генерация текста
    response = gpt_model.generate(prompt, max_tokens=200)
    return response

# ---------------------------
# В твоём блоке пояснения
# ---------------------------
st.markdown("---")
st.markdown("💡 Пояснение от ИИ:")
if st.session_state.selected_task is not None:
    task = st.session_state.df.loc[st.session_state.selected_task]
    explanation = gpt_explain(task["text"])
    st.info(explanation)
