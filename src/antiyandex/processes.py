import psutil

YANDEX_PROCESS_NAMES = {"browser.exe", "yandex.exe"}


def kill_yandex_processes():
    killed = False
    for proc in psutil.process_iter(["name"]):
        try:
            name = proc.info["name"]
            if name and name.lower() in YANDEX_PROCESS_NAMES:
                proc.kill()
                killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return killed
