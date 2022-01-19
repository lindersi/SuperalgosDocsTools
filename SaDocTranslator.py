import tkinter as tk
from tkinter import ttk
import os
import SaDocsListWordcount as func

project_path = '/home/simon/Superalgos'
storage_file = 'dateiliste'


    pickle.dump(data, storage_file)
    print(f'Processed {i} Docs files in {project_path}.')
    print(f'List stored in {os.getcwd()}/{storage_file} (binary Python dictionary).')


# root window
root = tk.Tk()
root.geometry("600x800+0+0")
root.title('SuperalgosDocTranslator')
root.resizable(True, True)

label = ttk.Label(root, text='Seitentitel, resp. Suchbegriff eingeben:')
label.pack(ipadx=10, ipady=10)

suchwort = tk.StringVar()
suchfeld = ttk.Entry(root, textvariable=suchwort)
suchfeld.bind('<Return>', return_pressed)

root.mainloop()
