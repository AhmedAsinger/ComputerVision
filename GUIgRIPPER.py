import subprocess
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Reconf. Six Finger Gripper Cont. Prog.")
root.geometry("1000x700")

canvas1 = tk.Canvas(root, width=300, height=300, bg='white', relief='raised')
canvas1.pack(side=tk.LEFT, padx=40, pady=30)

label1 = tk.Label(root, text='Six Finger Gripper Control')
label1.config(font=('helvetica', 24))
canvas1.create_window(150, 0, window=label1)


def get_python_file():
    global file_path
    file_path = filedialog.askopenfilename()


browseButton = tk.Button(text="Select Gripper Control File", command=get_python_file, bg='green', fg='white',
                         font=('helvetica', 18, 'bold'))
canvas1.create_window(150, 130, window=browseButton)


def run_python_file():
    global file_path, process
    print(file_path)
    process = subprocess.Popen([r"H:\PythonCodeGripper\venv\Scripts\python.exe", file_path])


runButton = tk.Button(text='Run The Gripper', command=run_python_file, bg='green', fg='white',
                      font=('helvetica', 18, 'bold'))
canvas1.create_window(150, 200, window=runButton)


def reset_python_file():
    global process
    process.kill()
    run_python_file()


resetButton = tk.Button(text='Detect Another Object', command=reset_python_file, bg='orange', fg='white',
                        font=('helvetica', 18, 'bold'))
canvas1.create_window(150, 270, window=resetButton)


def close_program():
    global process
    if process.poll() == None:
        process.kill()
    root.destroy()


closeButton = tk.Button(text='Close Program', command=close_program, bg='red', fg='white',
                        font=('helvetica', 18, 'bold'))
canvas1.create_window(150, 60, window=closeButton)

# Add image to the right side of the window
img = Image.open(r'H:\PythonCodeGripper\shape.png')
img = img.resize((600, 400), Image.ANTIALIAS)
photo_img = ImageTk.PhotoImage(img)
image_label = tk.Label(root, image=photo_img)
image_label.image = photo_img
image_label.pack(side=tk.RIGHT, padx=20, pady=20)

root.mainloop()
