import re

def load_local_graph(path):
    packages = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ":" not in line:
                raise ValueError(f"Неверная строка: {line}")
            name, deps = line.split(":", 1)
            name = name.strip().upper()
            if not re.fullmatch(r"[A-Z]+", name):
                raise ValueError(f"Имя пакета должно быть "
                                 f"заглавными латинскими: {name}")
            packages[name] = {d.strip().upper() for d
                              in deps.split() if d.strip()}
    return packages