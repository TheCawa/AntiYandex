import os
import shutil

YANDEX_PATHS = (
    r"C:\Program Files (x86)\Yandex\YandexBrowser",
    r"C:\Program Files\Yandex\YandexBrowser",
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Yandex", "YandexBrowser"),
    os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local", "Yandex", "YandexBrowser"),
)


def find_browser_path():
    for path in YANDEX_PATHS:
        if path and os.path.exists(path):
            return path
    return None


def remove_browser(path):
    shutil.rmtree(path, ignore_errors=True)
    if os.path.exists(path):
        raise RuntimeError("Files locked")
