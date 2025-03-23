import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import json

# Define colors for light and dark mode
LIGHT_BG = "#f0f0f0"
DARK_BG = "#2e2e2e"
LIGHT_TEXT = "#000000"
DARK_TEXT = "#ffffff"


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Task Manager")
        self.root.geometry("600x500")
        self.dark_mode = False

        self.tasks = []
        self.load_tasks()

        # Theme switch
        self.theme_button = ttk.Button(root, text="Toggle Dark Mode", command=self.toggle_theme)
        self.theme_button.pack(pady=5)

        # Task input
        self.task_entry = ttk.Entry(root, width=50)
        self.task_entry.pack(pady=5)

        self.priority_var = tk.StringVar(value="Medium")
        ttk.Label(root, text="Priority:").pack()
        self.priority_menu = ttk.Combobox(root, textvariable=self.priority_var, values=["High", "Medium", "Low"])
        self.priority_menu.pack()

        self.due_date = tk.StringVar()
        ttk.Label(root, text="Due Date (YYYY-MM-DD):").pack()
        self.date_entry = ttk.Entry(root, textvariable=self.due_date, width=15)
        self.date_entry.pack()

        # Add task button
        self.add_button = ttk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        # Task Listbox
        self.task_listbox = tk.Listbox(root, width=60, height=10)
        self.task_listbox.pack(pady=10)
        self.refresh_task_list()

        # Remove Task Button
        self.remove_button = ttk.Button(root, text="Remove Selected Task", command=self.remove_task)
        self.remove_button.pack()

        self.apply_theme()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        bg_color = DARK_BG if self.dark_mode else LIGHT_BG
        text_color = DARK_TEXT if self.dark_mode else LIGHT_TEXT
        self.root.configure(bg=bg_color)

        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Label, tk.Listbox)):
                widget.configure(bg=bg_color, fg=text_color)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        priority = self.priority_var.get()
        due_date = self.due_date.get()

        if task_text == "":
            messagebox.showerror("Error", "Task cannot be empty!")
            return

        try:
            datetime.datetime.strptime(due_date, "%Y-%m-%d")  # Validate date
        except ValueError:
            messagebox.showerror("Error", "Invalid date format!")
            return

        self.tasks.append({"task": task_text, "priority": priority, "due_date": due_date})
        self.save_tasks()
        self.refresh_task_list()
        self.task_entry.delete(0, tk.END)

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            return

        del self.tasks[selected_index[0]]
        self.save_tasks()
        self.refresh_task_list()

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, f"{task['task']} (Priority: {task['priority']}, Due: {task['due_date']})")

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
