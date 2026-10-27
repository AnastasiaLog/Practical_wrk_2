import urllib.request
import gzip
import re


def get_dependencies(repo_url, package_name, package_version):
    releases = ["jammy", "focal", "noble", "bionic"]
    components = ["main", "universe"]

    content = None
    for rel in releases:
        for comp in components:
            url = f"{repo_url}/dists/{rel}/{comp}/binary-amd64/Packages.gz"
            try:
                print(f"Скачивание данных из {rel}/{comp}...")
                response = urllib.request.urlopen(url, timeout=10)
                compressed_data = response.read()
                content = gzip.decompress(compressed_data).decode('utf-8')
                break
            except Exception:
                continue
        if content:
            break

    if not content:
        return None, "Не удалось найти файл Packages.gz в репозитории."

    blocks = content.split('\n\n')

    for block in blocks:
        if not block.strip():
            continue

        lines = block.split('\n')
        pkg_name = ""
        pkg_version = ""
        depends = ""

        for line in lines:
            if line.startswith("Package: "):
                pkg_name = line.split(": ")[1].strip()
            elif line.startswith("Version: "):
                pkg_version = line.split(": ")[1].strip()
            elif line.startswith("Depends: "):
                depends = line.split(": ")[1].strip()

        if pkg_name == package_name and pkg_version == package_version:
            if not depends:
                return [], "У пакета нет прямых зависимостей."

            depends = re.sub(r'\(.*?\)', '', depends)
            depends = depends.replace('|', ',')
            depends = depends.replace(':any', '')

            deps_list = [d.strip() for d in depends.split(',') if d.strip()]
            return deps_list, None

    return None, f"Пакет '{package_name}' " \
                 f"версии '{package_version}' не найден."