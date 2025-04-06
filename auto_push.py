import os
import tkinter as tk

def auto_push():
    os.system("git add .")
    os.system('git commit -m "Auto commit by button"')
    os.system("git push origin main")

root = tk.Tk()
root.title("Git Auto Push")

button = tk.Button(root, text="Push to Git", command=auto_push)
button.pack(padx=20, pady=20)

root.mainloop()
