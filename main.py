import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
from datetime import datetime
import os

class TaskManager:
    def __init__(self):
        self.tasks_file = "tasks.json"
        self.history_file = "history.json"
        self.tasks = {
            "учеба": ["Прочитать статью", "Решить задачи", "Написать конспект", 
                      "Повторить лекцию", "Сделать домашнее задание"],
            "спорт": ["Сделать зарядку", "Пробежка 30 мин", "Отжимания", 
                     "Растяжка", "Йога"],
            "работа": ["Проверить почту", "Написать отчет", "Созвониться с клиентом", 
                      "Запланировать встречу", "Обновить документацию"]
        }
        self.history = []
        self.load_tasks()
        self.load_history()
    
    def load_tasks(self):
        """Загрузка задач из JSON файла"""
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r', encoding='utf-8') as file:
                    loaded_tasks = json.load(file)
                    if loaded_tasks:  # Проверяем, что файл не пустой
                        self.tasks = loaded_tasks
            except (json.JSONDecodeError, FileNotFoundError):
                print("Ошибка загрузки файла задач. Используются предустановленные задачи.")
    
    def load_history(self):
        """Загрузка истории из JSON файла"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as file:
                    self.history = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                print("Ошибка загрузки истории. История пуста.")
    
    def save_tasks(self):
        """Сохранение задач в JSON файл"""
        with open(self.tasks_file, 'w', encoding='utf-8') as file:
            json.dump(self.tasks, file, ensure_ascii=False, indent=4)
    
    def save_history(self):
        """Сохранение истории в JSON файл"""
        with open(self.history_file, 'w', encoding='utf-8') as file:
            json.dump(self.history, file, ensure_ascii=False, indent=4)
    
    def generate_random_task(self, task_type=None):
        """Генерация случайной задачи с возможной фильтрацией по типу"""
        if task_type and task_type != "все":
            available_tasks = self.tasks.get(task_type, [])
        else:
            available_tasks = []
            for tasks_list in self.tasks.values():
                available_tasks.extend(tasks_list)
        
        if not available_tasks:
            return None
        
        task = random.choice(available_tasks)
        
        # Определяем тип выбранной задачи
        task_type_result = task_type if task_type != "все" else "общая"
        if task_type == "все" or not task_type:
            for type_name, tasks_list in self.tasks.items():
                if task in tasks_list:
                    task_type_result = type_name
                    break
        
        # Добавляем в историю
        history_entry = {
            "task": task,
            "type": task_type_result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(history_entry)
        self.save_history()
        
        return history_entry
    
    def add_task(self, task_text, task_type):
        """Добавление новой задачи с проверкой на пустую строку"""
        if not task_text or not task_text.strip():
            raise ValueError("Задача не может быть пустой")
        
        task_text = task_text.strip()
        
        if task_type not in self.tasks:
            self.tasks[task_type] = []
        
        if task_text in self.tasks[task_type]:
            return False  # Задача уже существует
        
        self.tasks[task_type].append(task_text)
        self.save_tasks()
        return True
    
    def delete_task(self, task_text, task_type):
        """Удаление задачи"""
        if task_type in self.tasks and task_text in self.tasks[task_type]:
            self.tasks[task_type].remove(task_text)
            self.save_tasks()
            return True
        return False
    
    def get_task_types(self):
        """Получение списка типов задач"""
        return list(self.tasks.keys())
    
    def get_tasks_by_type(self, task_type):
        """Получение задач определенного типа"""
        return self.tasks.get(task_type, [])


class RandomTaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("700x600")
        
        self.task_manager = TaskManager()
        
        self.setup_ui()
        self.update_tasks_list()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Заголовок
        title_label = tk.Label(
            self.root, 
            text="Генератор случайных задач", 
            font=("Arial", 16, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Фрейм для генерации задач
        generate_frame = tk.Frame(self.root)
        generate_frame.pack(pady=10)
        
        tk.Label(generate_frame, text="Тип задачи:").pack(side=tk.LEFT, padx=5)
        
        # Выпадающий список для фильтрации
        self.task_type_var = tk.StringVar(value="все")
        self.type_combobox = ttk.Combobox(
            generate_frame, 
            textvariable=self.task_type_var,
            values=["все"] + self.task_manager.get_task_types(),
            state="readonly",
            width=15
        )
        self.type_combobox.pack(side=tk.LEFT, padx=5)
        
        # Кнопка генерации
        generate_btn = tk.Button(
            generate_frame,
            text="Сгенерировать задачу",
            command=self.generate_task,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        )
        generate_btn.pack(side=tk.LEFT, padx=10)
        
        # Результат генерации
        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12),
            fg="#2196F3",
            pady=5
        )
        self.result_label.pack()
        
        # Фрейм для добавления новых задач
        add_frame = tk.LabelFrame(self.root, text="Добавить новую задачу", padx=10, pady=10)
        add_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(add_frame, text="Текст задачи:").grid(row=0, column=0, padx=5)
        self.new_task_entry = tk.Entry(add_frame, width=30)
        self.new_task_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(add_frame, text="Тип задачи:").grid(row=0, column=2, padx=5)
        self.new_task_type_var = tk.StringVar(value="учеба")
        new_type_combobox = ttk.Combobox(
            add_frame,
            textvariable=self.new_task_type_var,
            values=self.task_manager.get_task_types(),
            width=12
        )
        new_type_combobox.grid(row=0, column=3, padx=5)
        
        add_btn = tk.Button(
            add_frame,
            text="Добавить",
            command=self.add_task,
            bg="#2196F3",
            fg="white"
        )
        add_btn.grid(row=0, column=4, padx=10)
        
        # Фрейм для отображения задач
        tasks_frame = tk.LabelFrame(self.root, text="Список задач", padx=10, pady=10)
        tasks_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.tasks_listbox = tk.Listbox(tasks_frame, height=10)
        self.tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tasks_scrollbar = tk.Scrollbar(tasks_frame, command=self.tasks_listbox.yview)
        tasks_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tasks_listbox.config(yscrollcommand=tasks_scrollbar.set)
        
        # Кнопка удаления задачи
        tasks_control_frame = tk.Frame(tasks_frame)
        tasks_control_frame.pack(pady=5)
        
        delete_btn = tk.Button(
            tasks_control_frame,
            text="Удалить выбранную задачу",
            command=self.delete_task,
            bg="#f44336",
            fg="white"
        )
        delete_btn.pack()
        
        # Фрейм для истории
        history_frame = tk.LabelFrame(self.root, text="История сгенерированных задач", padx=10, pady=10)
        history_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.history_text = tk.Text(history_frame, height=8, wrap=tk.WORD)
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        history_scrollbar = tk.Scrollbar(history_frame, command=self.history_text.yview)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.config(yscrollcommand=history_scrollbar.set)
        
        # Кнопка очистки истории
        clear_btn = tk.Button(
            history_frame,
            text="Очистить историю",
            command=self.clear_history,
            bg="#FF9800",
            fg="white"
        )
        clear_btn.pack(pady=5)
        
        self.update_history_display()
    
    def generate_task(self):
        """Обработчик кнопки генерации задачи"""
        task_type = self.task_type_var.get()
        
        result = self.task_manager.generate_random_task(task_type)
        
        if result:
            self.result_label.config(
                text=f"Ваша задача: {result['task']}",
                fg="#4CAF50"
            )
            self.update_history_display()
            self.update_tasks_list()
        else:
            messagebox.showwarning("Предупреждение", "Нет доступных задач для выбранного типа")
    
    def add_task(self):
        """Обработчик кнопки добавления задачи"""
        task_text = self.new_task_entry.get()
        task_type = self.new_task_type_var.get()
        
        if not task_text.strip():
            messagebox.showerror("Ошибка", "Задача не может быть пустой")
            return
        
        try:
            result = self.task_manager.add_task(task_text, task_type)
            if result:
                messagebox.showinfo("Успех", f"Задача '{task_text}' добавлена")
                self.new_task_entry.delete(0, tk.END)
                self.update_tasks_list()
                # Обновляем выпадающий список типов
                self.type_combobox.config(values=["все"] + self.task_manager.get_task_types())
                self.new_task_type_var.set(task_type)
            else:
                messagebox.showwarning("Предупреждение", "Такая задача уже существует")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    
    def delete_task(self):
        """Обработчик кнопки удаления задачи"""
        selection = self.tasks_listbox.curselection()
        if selection:
            selected_text = self.tasks_listbox.get(selection[0])
            # Парсим строку формата "[тип] задача"
            try:
                task_type = selected_text[1:selected_text.index("]")]
                task_text = selected_text[selected_text.index("]")+2:]
                
                if self.task_manager.delete_task(task_text, task_type):
                    messagebox.showinfo("Успех", f"Задача удалена: {task_text}")
                    self.update_tasks_list()
                    self.type_combobox.config(values=["все"] + self.task_manager.get_task_types())
                else:
                    messagebox.showwarning("Ошибка", "Не удалось удалить задачу")
            except (ValueError, IndexError):
                messagebox.showwarning("Ошибка", "Ошибка формата задачи")
        else:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления")
    
    def update_tasks_list(self):
        """Обновление списка задач в интерфейсе"""
        self.tasks_listbox.delete(0, tk.END)
        
        for task_type, tasks in self.task_manager.tasks.items():
            for task in tasks:
                self.tasks_listbox.insert(tk.END, f"[{task_type}] {task}")
    
    def update_history_display(self):
        """Обновление отображения истории"""
        self.history_text.delete(1.0, tk.END)
        
        for entry in reversed(self.task_manager.history):
            history_line = f"[{entry['timestamp']}] [{entry['type']}] {entry['task']}\n"
            self.history_text.insert(tk.END, history_line)
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.task_manager.history = []
            self.task_manager.save_history()
            self.update_history_display()
            messagebox.showinfo("Успех", "История очищена")


def main():
    root = tk.Tk()
    app = RandomTaskGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
