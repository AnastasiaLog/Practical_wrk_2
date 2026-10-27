import json
from pathlib import Path
from validators import (
    ConfigError, validate_package_name, validate_package_version,
    validate_repo_mode, validate_repo_url, validate_tree_mode
)

def load_config(path_str):
    path = Path(path_str)
    if not path.exists() or not path.is_file():
        raise ConfigError(f"Файл конфигурации не найден: {path_str}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        raise ConfigError("Ошибка синтаксиса JSON.")

    if not isinstance(data, dict):
        raise ConfigError("Корневой элемент JSON "
                          "должен быть объектом.")

    required = ["package_name", "repo_url", "repo_mode",
                "package_version", "tree_mode"]
    for key in required:
        if key not in data:
            raise ConfigError(f"Отсутствует обязательный ключ: {key}")

    mode = validate_repo_mode(data["repo_mode"])

    return {
        "package_name": validate_package_name(data["package_name"]),
        "repo_url": validate_repo_url(data["repo_url"], mode),
        "repo_mode": mode,
        "package_version": validate_package_version(
            data["package_version"]),
        "tree_mode": validate_tree_mode(data["tree_mode"]),
    }