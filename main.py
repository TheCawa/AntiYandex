import tkinter as tk
from tkinter import messagebox
import os
import shutil
import psutil
import threading
import winreg
import locale


def get_system_lang():
    try:
        lang = locale.getlocale()[0] or "en"
    except:
        lang = "en"
    return "ru" if lang.startswith("ru") else "en"

language = get_system_lang()

YANDEX_PATHS = (
    r"C:\Program Files (x86)\Yandex\YandexBrowser",
    r"C:\Program Files\Yandex\YandexBrowser",
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Yandex", "YandexBrowser"),
    os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local", "Yandex", "YandexBrowser")
)

found_path = None

def t(key):
    translations = {
        "ru": {
            "title": "Удаление Яндекс Браузера",
            "search_btn": "Поиск Яндекса",
            "delete_btn": "Удалить Яндекс",
            "kill_btn": "Завершить процессы",
            "status_wait": "Статус: Ожидание",
            "status_searching": "Идёт поиск...",
            "status_found": "Найден в:\n{}",
            "status_not_found": "Яндекс не найден",
            "status_killed": "Процессы завершены",
            "status_no_proc": "Процессов не найдено",
            "success_kill": "Процессы Яндекса завершены.",
            "not_found_warning": "Процессы не найдены.",
            "delete_success": "Яндекс успешно удалён.",
            "delete_fail": "Ошибка при удалении.",
            "delete_first": "Сначала запустите поиск.",
            "registry_check_btn": "Реестр",
            "reg_found": "Найден в реестре",
            "reg_not_found": "В реестре не найден"
        },
        "en": {
            "title": "Yandex Remover",
            "search_btn": "Search Yandex",
            "delete_btn": "Delete Yandex",
            "kill_btn": "Kill Processes",
            "status_wait": "Status: Waiting",
            "status_searching": "Searching...",
            "status_found": "Found in:\n{}",
            "status_not_found": "Not found",
            "status_killed": "Processes killed",
            "status_no_proc": "No processes",
            "success_kill": "Processes killed successfully.",
            "not_found_warning": "No processes found.",
            "delete_success": "Deleted successfully.",
            "delete_fail": "Deletion failed.",
            "delete_first": "Run search first.",
            "registry_check_btn": "Registry",
            "reg_found": "Found in registry",
            "reg_not_found": "Not found in registry"
        }
    }
    return translations[language].get(key, key)

def update_status(status, color="black"):
    status_label.config(text=status, fg=color)

def check_registry_for_yandex():
    found_in_reg = False
    try:
        path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        if "Yandex" in name or "Яндекс" in name:
                            found_in_reg = True
                            break
                except: continue
    except: pass

    if found_in_reg:
        update_status(t("reg_found"), "green")
        messagebox.showinfo(t("title"), t("reg_found"))
    else:
        update_status(t("reg_not_found"), "red")
        messagebox.showwarning(t("title"), t("reg_not_found"))

def kill_yandex_processes():
    killed = False
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() in ["browser.exe", "yandex.exe"]:
                proc.kill()
                killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied): continue

    if killed:
        update_status(t("status_killed"), "green")
        messagebox.showinfo(t("title"), t("success_kill"))
    else:
        update_status(t("status_no_proc"), "orange")
        messagebox.showwarning(t("title"), t("not_found_warning"))

def check_yandex_browser():
    def task():
        global found_path
        update_status(t("status_searching"), "blue")
        for path in YANDEX_PATHS:
            if os.path.exists(path):
                found_path = path
                update_status(t("status_found").format(path), "green")
                return
        found_path = None
        update_status(t("status_not_found"), "red")
    threading.Thread(target=task, daemon=True).start()

def uninstall_yandex_browser():
    if not found_path:
        messagebox.showwarning(t("title"), t("delete_first"))
        return

    def task():
        global found_path
        try:
            if os.path.exists(found_path):
                shutil.rmtree(found_path, ignore_errors=True)
                if not os.path.exists(found_path):
                    update_status(t("delete_success"), "green")
                    messagebox.showinfo(t("title"), t("delete_success"))
                    found_path = None
                else:
                    raise Exception("Files locked")
        except Exception as e:
            update_status(t("delete_fail"), "red")
            messagebox.showerror(t("title"), f"{t('delete_fail')}\nError: {e}")

    threading.Thread(target=task, daemon=True).start()

# --- GUI ---
root = tk.Tk()
root.geometry("500x350")
root.resizable(False, False)

main_label = tk.Label(root, font=("Arial", 14, "bold"))
main_label.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

btn_check = tk.Button(btn_frame, width=20, command=check_yandex_browser)
btn_check.pack(pady=2)

btn_registry = tk.Button(btn_frame, width=20, command=check_registry_for_yandex)
btn_registry.pack(pady=2)

btn_kill = tk.Button(btn_frame, width=20, command=kill_yandex_processes)
btn_kill.pack(pady=2)

btn_delete = tk.Button(btn_frame, width=20, bg="red", fg="white", command=uninstall_yandex_browser)
btn_delete.pack(pady=10)

status_label = tk.Label(root, font=("Arial", 10), wraplength=450)
status_label.pack(pady=10)

def update_ui():
    """Функция обновления всех текстов в интерфейсе"""
    root.title(t("title"))
    main_label.config(text=t("title"))
    btn_check.config(text=t("search_btn"))
    btn_registry.config(text=t("registry_check_btn"))
    btn_kill.config(text=t("kill_btn"))
    btn_delete.config(text=t("delete_btn"))
    update_status(t("status_wait"), "blue")

def toggle_language():
    global language
    language = "en" if language == "ru" else "ru"
    update_ui()

tk.Button(root, text="RU/EN", command=toggle_language).place(x=430, y=10)

update_ui()

root.mainloop()