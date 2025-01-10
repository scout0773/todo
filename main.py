import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os
import time

class todoApp:
    priorities = {
        "high": "#e83f3f",
        "medium": "#edbe51",
        "low": "#5bd475"
    }
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("To-Do App")
        self.root.resizable(False, False)
        self.tasks =[]
        
        self._setup_ui()
        self.update_listbox()
        
    def _setup_ui(self):
        self.task_entry = tk.Entry(self.root, width=50)
        self.task_entry.pack(pady=10)
        
        self.priority_var = tk.StringVar(self.root)
        self.priority_var.set("medium")
        self.priority_dropdown = tk.OptionMenu(self.root, self.priority_var, "high", "medium", "low")
        self.priority_dropdown.pack()
        
        add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        add_button.pack()

        self.tasks_listbox = tk.Listbox(self.root, width=50)
        self.tasks_listbox.pack(pady=10)

        edit_button = tk.Button(self.root, text="Edit Task", command=self.edit_task)
        edit_button.pack()

        delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        delete_button.pack()

        save_button = tk.Button(self.root, text="Save Tasks", command=self.save_tasks)
        save_button.pack(side=tk.LEFT, padx=5)

        load_button = tk.Button(self.root, text="Load Tasks", command=lambda:self.load_tasks())
        load_button.pack(side=tk.RIGHT, padx=5)

    def add_task(self):
        task = self.task_entry.get().strip()
        priority = self.priority_var.get()
        if task and any(char.isalnum() for char in task):
            self.tasks.append((task, priority))
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")
            
    def delete_task(self):
        try:
            task_index = self.tasks_listbox.curselection()[0]
            self.tasks.pop(task_index)
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")
            
    def edit_task(self):
        try:
            task_index = self.tasks_listbox.curselection()[0]
            new_task = simpledialog.askstring("Edit Task", "Enter new task:")
            if new_task is not None:
                new_task = new_task.strip()
                if new_task and any(char.isalnum() for char in new_task):
                    priority = self.tasks[task_index][1]
                    self.tasks[task_index] = (new_task, priority)
                    self.update_listbox()
                    self.task_entry.delete(0, tk.END)
                else:
                    messagebox.showwarning("Warning", "Task cannot be empty.")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to edit.")
            
    def save_tasks(self):
        if self.tasks:
            try:
                if not os.path.exists("lists"):
                    os.makedirs("lists")
                    
                timestamp = int(time.time())
                filename = f"lists/todo_{timestamp}.txt"
                
                with open(filename, "w") as file:
                    for task, priority in self.tasks:
                        file.write(f"{task},{priority}\n")
                messagebox.showinfo("Success", "Tasks saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving tasks: {str(e)}")
    
    def load_tasks(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
            if file_path:
                if not file_path.endswith('.txt'):
                    messagebox.showerror("Error", "Only .txt files are allowed.")
                    return
                with open(file_path, "r") as file:
                    self.tasks.clear()
                    lines = file.readlines()
                    for line in lines:
                        task, priority = line.strip().split(',')
                        self.tasks.append((task, priority))
                    self.update_listbox()
                    messagebox.showinfo("Success", "Tasks loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading tasks: {str(e)}")
    
    def update_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        sorted_tasks = sorted(self.tasks, key=lambda x: ("high", "medium", "low").index(x[1]))
        for task, priority in sorted_tasks:
            self.tasks_listbox.insert(tk.END, task)
            self.tasks_listbox.itemconfig(tk.END, bg=self.priorities[priority])

    def run(self):
        self.root.mainloop()
            
if __name__ == "__main__":
    app = todoApp()
    app.run()