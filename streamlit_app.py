
import os

# Создать папку pages, если её нет
if not os.path.exists("pages"):
    os.makedirs("pages")

# Создать пустой __init__.py, если его нет
init_file = os.path.join("pages", "__init__.py")
if not os.path.exists(init_file):
    with open(init_file, "w", encoding="utf-8") as f:
        f.write("# Пакет pages")
