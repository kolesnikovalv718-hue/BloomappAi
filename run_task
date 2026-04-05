# generate_tasks.py
from transformers import pipeline
import pandas as pd

def run():
    # ----------------------------
    # Модель на Hugging Face
    # ----------------------------
    model_name = "TheBloke/GPT4All-Mini-1.3-GGUF"
    print("Загрузка модели… (скачивается один раз, затем в кэше)")
    generator = pipeline(
        "text-generation",
        model=model_name
    )

    # ----------------------------
    # Шаблон задания
    # ----------------------------
    prompt = """
    Сгенерируй задание по тригонометрии для 10 класса с формулой y = A + B*cos(k*t),
    укажи конкретные числа, время для расчета и подробное решение.
    """

    # ----------------------------
    # Генерация 10 заданий
    # ----------------------------
    print("Генерация заданий…")
    tasks = []
    for i in range(10):
        result = generator(prompt, max_length=500)[0]['generated_text']
        tasks.append(result)

    # ----------------------------
    # Сохраняем в CSV
    # ----------------------------
    df = pd.DataFrame({"Задание": tasks})
    df.to_csv("tasks_generated.csv", index=False, encoding="utf-8")
    print("Готово! 10 заданий сгенерированы и сохранены в tasks_generated.csv")

# ----------------------------
# Если запустить напрямую
# ----------------------------
if __name__ == "__main__":
    run()
