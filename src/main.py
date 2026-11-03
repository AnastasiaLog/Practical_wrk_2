import argparse
import sys
import os
from config_loader import load_config
from validators import ConfigError
from fetcher import get_dependencies
from local_repo import load_local_graph
from graph import make_graph


def print_graph(graph):
    print("\nГраф зависимостей (DFS):")
    for name in sorted(graph):
        deps = ", ".join(sorted(graph[name])) if graph[name] else "—"
        print(f"  {name}: {deps}")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_config = os.path.join(base_dir, "config.json")

    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей (Этап 3)")
    parser.add_argument("-c", "--config", default=default_config,
                        help="Путь к JSON-конфигу")
    args = parser.parse_args()

    try:
        cfg = load_config(args.config)

        print("Параметры конфигурации:")
        for key, val in cfg.items():
            print(f"  {key.ljust(15)}: {val}")

        if cfg["repo_mode"] == "local":
            packages = load_local_graph(cfg["repo_url"])
            root = cfg["package_name"].upper()
            if root not in packages:
                raise ConfigError(
                    f"Пакет '{root}' отсутствует в тестовом репозитории.")
            print(f"\nЛокальный режим: граф загружен из "
                  f"'{cfg['repo_url']}'.")

        elif cfg["repo_mode"] == "remote":
            print("\nПоиск прямых зависимостей...")
            deps, error = get_dependencies(
                cfg["repo_url"], cfg["package_name"],
                cfg["package_version"])

            if error:
                print(f"Ошибка: {error}")
                return 1

            root = cfg["package_name"]
            packages = {root: set(deps or [])}
            print(f"Прямые зависимости '{root}' "
                  f"({cfg['package_version']}): "
                  f"{', '.join(sorted(packages[root])) or '—'}")

        else:
            raise ConfigError(f"Неизвестный режим: "
                              f"{cfg['repo_mode']}")

        graph = make_graph(root, packages)
        print_graph(graph)

        return 0

    except ConfigError as e:
        print(f"Ошибка конфигурации: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())