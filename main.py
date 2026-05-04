
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Имя файла, куда сохраняются книги
FILENAME = "books.json"


# ==================== ФУНКЦИИ ДЛЯ РАБОТЫ С ДАННЫМИ ====================

def load_books():
    """Загружает список книг из JSON-файла. Если файла нет — возвращает пустой список."""
    if not os.path.exists(FILENAME):
        return []
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_books(books):
    """Сохраняет список книг в JSON-файл."""
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)


def validate_book(title, author, year):
    """
    Проверяет, что данные книги введены правильно.
    Возвращает None если всё хорошо, или текст ошибки если есть проблема.
    """
    if not title.strip():
        return "Название не может быть пустым!"
    if not author.strip():
        return "Автор не может быть пустым!"
    if not year.strip():
        return "Год не может быть пустым!"
    try:
        year_num = int(year)
        if year_num < 1000 or year_num > 2026:
            return "Год должен быть от 1000 до 2026!"
    except ValueError:
        return "Год должен быть целым числом!"
    return None


# ==================== ГЛАВНОЕ ОКНО ПРИЛОЖЕНИЯ ====================

class LibraryApp:
    """Графическое приложение для управления библиотекой."""

    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер личной библиотеки")
        self.root.geometry("700x550")
        self.root.resizable(True, True)

        # Загружаем сохранённые книги
        self.books = load_books()

        # Создаём все элементы интерфейса
        self.create_widgets()

        # Показываем все книги при запуске
        self.refresh_table()

    # ---------- СОЗДАНИЕ ИНТЕРФЕЙСА ----------

    def create_widgets(self):
        """Рисует все кнопки, поля ввода и таблицу на экране."""

        # --- Рамка для добавления книги ---
        frame_add = ttk.LabelFrame(self.root, text="Добавить книгу", padding=10)
        frame_add.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_add, text="Название:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_title = ttk.Entry(frame_add, width=25)
        self.entry_title.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame_add, text="Автор:").grid(row=0, column=2, sticky="w", pady=2)
        self.entry_author = ttk.Entry(frame_add, width=25)
        self.entry_author.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(frame_add, text="Год:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_year = ttk.Entry(frame_add, width=10)
        self.entry_year.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        btn_add = ttk.Button(frame_add, text="Добавить книгу", command=self.add_book)
        btn_add.grid(row=1, column=3, pady=5, sticky="e")

        # --- Рамка для фильтрации ---
        frame_filter = ttk.LabelFrame(self.root, text="Фильтр по автору", padding=10)
        frame_filter.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_filter, text="Введите автора:").pack(side="left", padx=5)
        self.entry_filter = ttk.Entry(frame_filter, width=30)
        self.entry_filter.pack(side="left", padx=5)

        btn_filter = ttk.Button(frame_filter, text="Найти", command=self.filter_books)
        btn_filter.pack(side="left", padx=5)

        btn_show_all = ttk.Button(frame_filter, text="Показать все", command=self.refresh_table)
        btn_show_all.pack(side="left", padx=5)

        # --- Таблица для отображения книг ---
        frame_table = ttk.Frame(self.root)
        frame_table.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("title", "author", "year")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)

        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("year", text="Год")

        self.tree.column("title", width=250)
        self.tree.column("author", width=200)
        self.tree.column("year", width=80)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Кнопки управления ---
        frame_buttons = ttk.Frame(self.root)
        frame_buttons.pack(fill="x", padx=10, pady=5)

        btn_delete = ttk.Button(frame_buttons, text="Удалить выбранную книгу", command=self.delete_book)
        btn_delete.pack(side="left", padx=5)

        btn_save = ttk.Button(frame_buttons, text="Сохранить в файл", command=self.save_to_file)
        btn_save.pack(side="right", padx=5)

    # ---------- ДЕЙСТВИЯ ----------

    def add_book(self):
        """Добавляет новую книгу в список и обновляет таблицу."""
        title = self.entry_title.get()
        author = self.entry_author.get()
        year = self.entry_year.get()

        # Проверяем данные
        error = validate_book(title, author, year)
        if error:
            messagebox.showerror("Ошибка", error)
            return

        # Добавляем книгу
        new_book = {
            "title": title.strip(),
            "author": author.strip(),
            "year": int(year.strip())
        }
        self.books.append(new_book)

        # Очищаем поля ввода
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)

        # Обновляем таблицу
        self.refresh_table()
        messagebox.showinfo("Готово", f"Книга '{title.strip()}' добавлена!")

    def delete_book(self):
        """Удаляет выбранную в таблице книгу."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите книгу для удаления!")
            return

        # Получаем данные выбранной строки
        item = self.tree.item(selected[0])
        values = item["values"]

        # Удаляем книгу из списка
        title, author, year = values[0], values[1], values[2]
        self.books = [
            book for book in self.books
            if not (book["title"] == title and book["author"] == author and book["year"] == int(year))
        ]

        self.refresh_table()
        messagebox.showinfo("Готово", f"Книга '{title}' удалена!")

    def filter_books(self):
        """Показывает только книги указанного автора."""
        author_filter = self.entry_filter.get().strip().lower()
        if not author_filter:
            messagebox.showwarning("Внимание", "Введите имя автора для поиска!")
            return

        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Заполняем только подходящими книгами
        found = False
        for book in self.books:
            if author_filter in book["author"].lower():
                self.tree.insert("", tk.END, values=(book["title"], book["author"], book["year"]))
                found = True

        if not found:
            messagebox.showinfo("Результат", f"Книг автора '{self.entry_filter.get().strip()}' не найдено.")

    def refresh_table(self):
        """Обновляет таблицу — показывает все книги из списка self.books."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for book in self.books:
            self.tree.insert("", tk.END, values=(book["title"], book["author"], book["year"]))

    def save_to_file(self):
        """Сохраняет текущий список книг в JSON-файл."""
        save_books(self.books)
        messagebox.showinfo("Готово", f"Книги сохранены в файл '{FILENAME}'!")


# ==================== ЗАПУСК ПРИЛОЖЕНИЯ ====================

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
