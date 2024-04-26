import tkinter as tk
from tkinter import messagebox, simpledialog

def add_task():
    task = task_entry.get().strip()
    if task and any(char.isalnum() for char in task):
        tasks.append(task)
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
        new_task = tk.simpledialog.askstring("Edit Task", "Enter new task:")
        if new_task:
            tasks[task_index] = new_task
            update_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to edit.")

def update_listbox():
    tasks_listbox.delete(0, tk.END)
    for task in tasks:
        tasks_listbox.insert(tk.END, task)

root = tk.Tk()
root.title("To-Do App")

tasks = []

task_entry = tk.Entry(root, width=50)
task_entry.pack(pady=10)

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack()

tasks_listbox = tk.Listbox(root, width=50)
tasks_listbox.pack(pady=10)

edit_button = tk.Button(root, text="Edit Task", command=edit_task)
edit_button.pack()

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack()

update_listbox()

root.mainloop()