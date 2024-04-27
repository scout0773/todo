import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog

priorities = {
    "high": "#e83f3f",
    "medium": "#edbe51",
    "low": "#5bd475"
}

def add_task():
    task = task_entry.get().strip()
    priority = priority_var.get()
    if task and any(char.isalnum() for char in task):
        tasks.append((task, priority))
        update_listbox()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task.")
        
def delete_task():
    try:
        task_index = tasks_listbox.curselection()[0]
        tasks.pop(task_index)
        update_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to delete.")
        
def edit_task():
    try:
        task_index = tasks_listbox.curselection()[0]
        new_task = simpledialog.askstring("Edit Task", "Enter new task:")
        if new_task is not None:
            new_task = new_task.strip()
            if new_task and any(char.isalnum() for char in new_task):
                priority = tasks[task_index][1]
                tasks[task_index] = (new_task, priority)
                update_listbox()
                task_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Warning", "Task cannot be empty.")
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to edit.")
        
def save_tasks():
    if tasks:
        try:
            with open("tasks.txt", "w") as file:
                for task, priority in tasks:
                    file.write(f"{task},{priority}\n")
            messagebox.showinfo("Success", "Tasks saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving tasks: {str(e)}")

def load_tasks():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                tasks.clear()
                lines = file.readlines()
                for line in lines:
                    task, priority = line.strip().split(',')
                    tasks.append((task, priority))
                update_listbox()
                messagebox.showinfo("Success", "Tasks loaded successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading tasks: {str(e)}")

def update_listbox():
    tasks_listbox.delete(0, tk.END)
    for task, priority in tasks:
        tasks_listbox.insert(tk.END, task)
        tasks_listbox.itemconfig(tk.END, bg=priorities[priority])

root = tk.Tk()
root.title("To-Do App")

tasks = []

task_entry = tk.Entry(root, width=50)
task_entry.pack(pady=10)

priority_var = tk.StringVar(root)
priority_var.set("medium")
priority_dropdown = tk.OptionMenu(root, priority_var, "high", "medium", "low")
priority_dropdown.pack()

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack()

tasks_listbox = tk.Listbox(root, width=50)
tasks_listbox.pack(pady=10)

edit_button = tk.Button(root, text="Edit Task", command=edit_task)
edit_button.pack()

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack()

save_button = tk.Button(root, text="Save Tasks", command=save_tasks)
save_button.pack(side=tk.LEFT, padx=5)

load_button = tk.Button(root, text="Load Tasks", command=lambda:load_tasks())
load_button.pack(side=tk.RIGHT, padx=5)

update_listbox()

root.mainloop()