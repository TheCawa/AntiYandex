import os
import shutil

YANDEX_PATHS = (
    r"C:\Program Files (x86)\Yandex\YandexBrowser",
    r"C:\Program Files\Yandex\YandexBrowser",
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Yandex", "YandexBrowser"),
    os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local", "Yandex", "YandexBrowser"),
)


def find_browser_paths():
    found = []
    seen = set()
    for path in YANDEX_PATHS:
        if not path or not os.path.exists(path):
            continue
        key = os.path.normcase(os.path.abspath(path))
        if key in seen:
            continue
        seen.add(key)
        found.append(path)
    return found


def find_browser_path():
    paths = find_browser_paths()
    return paths[0] if paths else None


def remove_browser(path):
    shutil.rmtree(path, ignore_errors=True)
    if not os.path.exists(path):
        return []

    leftovers = []
    for root, _dirs, files in os.walk(path):
        leftovers.extend(os.path.join(root, name) for name in files)
    if not leftovers:
        leftovers.append(path)
    return leftovers
