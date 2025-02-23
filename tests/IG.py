import tkinter as tk
from tkinter import messagebox
from test_progression import greet, add

def show_greeting():
    name = entry_name.get()
    message = greet(name)
    messagebox.showinfo("Greeting", message)

def show_addition():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        result = add(a, b)
        messagebox.showinfo("Addition Result", f"The result is: {result}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers")

# Create the main window
root = tk.Tk()
root.title("Simple GUI")

# Greeting section
label_name = tk.Label(root, text="Enter your name:")
label_name.pack()

entry_name = tk.Entry(root)
entry_name.pack()

button_greet = tk.Button(root, text="Greet", command=show_greeting)
button_greet.pack()

# Addition section
label_a = tk.Label(root, text="Enter first number:")
label_a.pack()
 
entry_a = tk.Entry(root)
entry_a.pack()

label_b = tk.Label(root, text="Enter second number:")
label_b.pack()

entry_b = tk.Entry(root)
entry_b.pack()

button_add = tk.Button(root, text="Add", command=show_addition)
button_add.pack()

# Run the application
root.mainloop()
