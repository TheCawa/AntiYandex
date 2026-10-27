import psutil

YANDEX_PROCESS_NAMES = {"browser.exe", "yandex.exe"}
YANDEX_EXE_MARKERS = ("yandexbrowser", "\\yandex\\")


def _is_yandex_process(name, exe):
    lowered_exe = (exe or "").lower()
    lowered_name = (name or "").lower()

    if "yandexbrowser" in lowered_exe:
        return True
    if lowered_name in YANDEX_PROCESS_NAMES and "\\yandex\\" in lowered_exe:
        return True
    if not lowered_exe:
        return lowered_name in YANDEX_PROCESS_NAMES
    return False


def kill_yandex_processes():
    killed = False
    for proc in psutil.process_iter(["name", "exe"]):
        try:
            if _is_yandex_process(proc.info.get("name"), proc.info.get("exe")):
                proc.kill()
                killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return killed
