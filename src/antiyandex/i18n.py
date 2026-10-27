import locale

TRANSLATIONS = {
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
        "reg_not_found": "В реестре не найден",
        "reg_removed": "Записи реестра очищены",
        "reg_remove_fail": "Не удалось очистить реестр",
        "admin_hint": "Запустите программу от имени администратора для удаления записей реестра",
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
        "reg_not_found": "Not found in registry",
        "reg_removed": "Registry entries cleaned",
        "reg_remove_fail": "Failed to clean registry",
        "admin_hint": "Run the program as administrator to delete registry entries",
    },
}


def get_system_language():
    try:
        lang = locale.getlocale()[0] or "en"
    except Exception:
        lang = "en"
    return "ru" if lang.startswith("ru") else "en"


class Translator:
    def __init__(self, language=None):
        self.language = language or get_system_language()

    def __call__(self, key):
        return TRANSLATIONS[self.language].get(key, key)

    def toggle(self):
        self.language = "en" if self.language == "ru" else "ru"
        return self.language
