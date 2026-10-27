from pathlib import Path

class ConfigError(ValueError):
    pass

def validate_string(value, param_name):
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"Параметр '{param_name}' должен быть непустой строкой.")
    return value.strip()

def validate_package_name(value):
    return validate_string(value, "package_name")

def validate_package_version(value):
    return validate_string(value, "package_version")

def validate_tree_mode(value):
    if value not in ("full", "direct"):
        raise ConfigError(f"Параметр 'tree_mode' должен быть 'full' или 'direct'. Получено: {value}")
    return value

def validate_repo_mode(value):
    if value not in ("remote", "local"):
        raise ConfigError(f"Параметр 'repo_mode' должен быть 'remote' или 'local'. Получено: {value}")
    return value

def validate_repo_url(value, mode):
    value = validate_string(value, "repo_url")
    if mode == "remote":
        if not value.startswith(("http://", "https://")):
            raise ConfigError(f"Для режима 'remote' URL должен начинаться с http:// или https://. Получено: {value}")
        return value
    elif mode == "local":
        if not Path(value).exists():
            raise ConfigError(f"Локальный путь не существует: {value}")
        return value