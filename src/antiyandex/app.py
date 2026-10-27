import threading
import tkinter as tk
from tkinter import messagebox

from . import browser, processes, registry
from .i18n import Translator


class AntiYandexApp:
    def __init__(self):
        self.translator = Translator()
        self.found_path = None

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

    def update_texts(self):
        self.root.title(self.t("title"))
        self.main_label.config(text=self.t("title"))
        self.btn_check.config(text=self.t("search_btn"))
        self.btn_registry.config(text=self.t("registry_check_btn"))
        self.btn_kill.config(text=self.t("kill_btn"))
        self.btn_delete.config(text=self.t("delete_btn"))
        self.set_status(self.t("status_wait"), "blue")

    def toggle_language(self):
        self.translator.toggle()
        self.update_texts()

    def search_browser(self):
        self.set_status(self.t("status_searching"), "blue")

        def task():
            path = browser.find_browser_path()
            self.found_path = path
            if path:
                self.set_status(self.t("status_found").format(path), "green")
            else:
                self.set_status(self.t("status_not_found"), "red")

        threading.Thread(target=task, daemon=True).start()

    def check_registry(self):
        if registry.has_yandex_entries():
            self.set_status(self.t("reg_found"), "green")
            messagebox.showinfo(self.t("title"), self.t("reg_found"))
        else:
            self.set_status(self.t("reg_not_found"), "red")
            messagebox.showwarning(self.t("title"), self.t("reg_not_found"))

    def kill_processes(self):
        if processes.kill_yandex_processes():
            self.set_status(self.t("status_killed"), "green")
            messagebox.showinfo(self.t("title"), self.t("success_kill"))
        else:
            self.set_status(self.t("status_no_proc"), "orange")
            messagebox.showwarning(self.t("title"), self.t("not_found_warning"))

    def delete_browser(self):
        if not self.found_path:
            messagebox.showwarning(self.t("title"), self.t("delete_first"))
            return

        def task():
            try:
                browser.remove_browser(self.found_path)
            except PermissionError:
                self.set_status(self.t("delete_fail"), "red")
                messagebox.showerror(self.t("title"), self.t("admin_hint"))
            except Exception as exc:
                self.set_status(self.t("delete_fail"), "red")
                messagebox.showerror(
                    self.t("title"), "{}\nError: {}".format(self.t("delete_fail"), exc)
                )
            else:
                registry.remove_yandex_entries()
                self.set_status(self.t("delete_success"), "green")
                messagebox.showinfo(self.t("title"), self.t("delete_success"))
                self.found_path = None

        threading.Thread(target=task, daemon=True).start()

    def run(self):
        self.root.mainloop()
