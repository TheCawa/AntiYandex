import ctypes
import threading
import tkinter as tk
from tkinter import messagebox

from . import browser, processes, registry
from .i18n import Translator


def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except (AttributeError, OSError):
        return False


class AntiYandexApp:
    def __init__(self):
        self.translator = Translator()
        self.found_paths = []

        self.root = tk.Tk()
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        self._build_ui()
        self.update_texts()

    def _build_ui(self):
        self.main_label = tk.Label(self.root, font=("Arial", 14, "bold"))
        self.main_label.pack(pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        self.btn_check = tk.Button(btn_frame, width=20, command=self.search_browser)
        self.btn_check.pack(pady=2)

        self.btn_registry = tk.Button(btn_frame, width=20, command=self.check_registry)
        self.btn_registry.pack(pady=2)

        self.btn_kill = tk.Button(btn_frame, width=20, command=self.kill_processes)
        self.btn_kill.pack(pady=2)

        self.btn_delete = tk.Button(
            btn_frame, width=20, bg="red", fg="white", command=self.delete_browser
        )
        self.btn_delete.pack(pady=10)

        self.status_label = tk.Label(self.root, font=("Arial", 10), wraplength=450)
        self.status_label.pack(pady=10)

        self.lang_button = tk.Button(self.root, text="RU/EN", command=self.toggle_language)
        self.lang_button.place(x=430, y=10)

    def t(self, key):
        return self.translator(key)

    def set_status(self, text, color="black"):
        self.status_label.config(text=text, fg=color)

    def run_in_ui(self, callback):
        self.root.after(0, callback)

    def update_texts(self):
        self.root.title(self.t("title"))
        self.main_label.config(text=self.t("title"))
        self.btn_check.config(text=self.t("search_btn"))
        self.btn_registry.config(text=self.t("registry_check_btn"))
        self.btn_kill.config(text=self.t("kill_btn"))
        self.btn_delete.config(text=self.t("delete_btn"))
        if is_admin():
            self.set_status(self.t("status_wait"), "blue")
        else:
            self.set_status(self.t("warn_no_admin"), "orange")

    def toggle_language(self):
        self.translator.toggle()
        self.update_texts()

    def search_browser(self):
        self.set_status(self.t("status_searching"), "blue")

        def task():
            paths = browser.find_browser_paths()

            def done():
                self.found_paths = paths
                if paths:
                    self.set_status(
                        self.t("status_found").format("\n".join(paths)), "green"
                    )
                else:
                    self.set_status(self.t("status_not_found"), "red")

            self.run_in_ui(done)

        threading.Thread(target=task, daemon=True).start()

    def check_registry(self):
        if registry.has_yandex_entries():
            self.set_status(self.t("reg_found"), "green")
            messagebox.showinfo(self.t("title"), self.t("reg_found"))
        else:
            self.set_status(self.t("reg_not_found"), "red")
            messagebox.showwarning(self.t("title"), self.t("reg_not_found"))

    def kill_processes(self):
        self.set_status(self.t("status_searching"), "blue")

        def task():
            killed = processes.kill_yandex_processes()

            def done():
                if killed:
                    self.set_status(self.t("status_killed"), "green")
                    messagebox.showinfo(self.t("title"), self.t("success_kill"))
                else:
                    self.set_status(self.t("status_no_proc"), "orange")
                    messagebox.showwarning(self.t("title"), self.t("not_found_warning"))

            self.run_in_ui(done)

        threading.Thread(target=task, daemon=True).start()

    def delete_browser(self):
        if not self.found_paths:
            messagebox.showwarning(self.t("title"), self.t("delete_first"))
            return

        paths = list(self.found_paths)

        def task():
            locked = []
            for path in paths:
                try:
                    locked.extend(browser.remove_browser(path))
                except PermissionError:
                    locked.append(path)
                except OSError as exc:
                    locked.append("{}: {}".format(path, exc))

            if locked:
                def fail():
                    self.set_status(self.t("delete_fail"), "red")
                    messagebox.showerror(
                        self.t("title"),
                        "{}\n\n{}".format(
                            self.t("delete_locked").format(len(locked)),
                            self.t("admin_hint"),
                        ),
                    )

                self.run_in_ui(fail)
                return

            removed, failed = registry.remove_yandex_entries()

            def done():
                self.found_paths = []
                self.set_status(self.t("delete_success"), "green")
                message = self.t("delete_success")
                if removed:
                    message = "{}\n{}".format(message, self.t("reg_removed"))
                if failed:
                    message = "{}\n{}".format(message, self.t("reg_remove_fail"))
                    messagebox.showwarning(self.t("title"), message)
                else:
                    messagebox.showinfo(self.t("title"), message)

            self.run_in_ui(done)

        threading.Thread(target=task, daemon=True).start()

    def run(self):
        self.root.mainloop()
