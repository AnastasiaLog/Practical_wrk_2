import argparse
import sys
import os
from config_loader import load_config
from validators import ConfigError
from fetcher import get_dependencies


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_config = os.path.join(base_dir, "config.json")

    parser = argparse.ArgumentParser(description="Инструмент визуализации графа зависимостей (Этап 2)")
    parser.add_argument("-c", "--config", default=default_config, help="Путь к JSON-конфигу")
    args = parser.parse_args()

    try:
        cfg = load_config(args.config)

        print("Параметры конфигурации:")
        for key, val in cfg.items():
            print(f"  {key.ljust(15)}: {val}")

        if cfg["repo_mode"] == "remote":
            print("\nПоиск прямых зависимостей...")

            deps, error = get_dependencies(cfg["repo_url"], cfg["package_name"], cfg["package_version"])

            if error:
                print(f"Ошибка: {error}")
            elif not deps:
                print("У пакета нет прямых зависимостей.")
            else:
                print(f"\nПрямые зависимости пакета '{cfg['package_name']}' ({cfg['package_version']}):")
                for d in deps:
                    print(f"  - {d}")
        else:
            print("\nРежим 'local' пока не поддерживается для сбора данных.")

        return 0
    except ConfigError as e:
        print(f"Ошибка конфигурации: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())