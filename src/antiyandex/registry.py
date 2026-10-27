import winreg

YANDEX_NAME_MARKERS = ("Yandex", "Яндекс")

UNINSTALL_KEYS = (
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
)


def _is_yandex_display_name(name):
    return any(marker in name for marker in YANDEX_NAME_MARKERS)


def _uninstall_subkeys(hkey, path):
    subkeys = []
    try:
        with winreg.OpenKey(hkey, path) as key:
            index = 0
            while True:
                try:
                    subkeys.append(winreg.EnumKey(key, index))
                except OSError:
                    break
                index += 1
    except OSError:
        pass
    return subkeys


def _display_name(hkey, path, subkey_name):
    try:
        with winreg.OpenKey(hkey, path + "\\" + subkey_name, 0, winreg.KEY_READ) as subkey:
            return winreg.QueryValueEx(subkey, "DisplayName")[0]
    except OSError:
        return None


def _yandex_subkeys(hkey, path):
    for subkey_name in _uninstall_subkeys(hkey, path):
        name = _display_name(hkey, path, subkey_name)
        if isinstance(name, str) and _is_yandex_display_name(name):
            yield subkey_name


def has_yandex_entries():
    """True, если в реестре есть записи об установленном Яндекс Браузере."""
    return any(True for hkey, path in UNINSTALL_KEYS for _ in _yandex_subkeys(hkey, path))


def remove_yandex_entries():
    removed = False
    for hkey, path in UNINSTALL_KEYS:
        subkeys = list(_yandex_subkeys(hkey, path))
        if not subkeys:
            continue
        try:
            with winreg.OpenKey(hkey, path, 0, winreg.KEY_WRITE) as key:
                for subkey_name in subkeys:
                    try:
                        winreg.DeleteKey(key, subkey_name)
                        removed = True
                    except OSError:
                        pass
        except OSError:
            continue
    return removed
