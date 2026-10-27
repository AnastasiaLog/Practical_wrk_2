from pathlib import Path

class ConfigError(ValueError):
    pass

def validate_string(value, param_name):
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"Параметр '{param_name}' "
                          f"должен быть непустой строкой.")
    return value.strip()

def validate_package_name(value):
    return validate_string(value, "package_name")

def validate_package_version(value):
    return validate_string(value, "package_version")

def validate_tree_mode(value):
    if value not in ("full", "direct"):
        raise ConfigError(f"Параметр 'tree_mode' должен быть"
                          f" 'full' или 'direct'. "
                          f"Получено: {value}")
    return value

def validate_repo_mode(value):
    if value not in ("remote", "local"):
        raise ConfigError(f"Параметр 'repo_mode' "
                          f"должен быть 'remote' или 'local'. "
                          f"Получено: {value}")
    return value

def validate_repo_url(value, mode):
    value = validate_string(value, "repo_url")
    if mode == "remote":
        if not value.startswith(("http://", "https://")):
            raise ConfigError(f"Для режима 'remote' URL "
                              f"должен начинаться с http:// "
                              f"или https://. Получено: {value}")
        return value
    elif mode == "local":
        if not Path(value).exists():
            raise ConfigError(f"Локальный путь не существует: {value}")
        return value