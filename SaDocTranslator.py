import tkinter as tk
from tkinter import ttk
import pickle
import SaDocsListWordcount as func

project_path = '/home/simon/Superalgos/Projects'
storage_file = 'dateiliste'  # Binäre Speicherung der File-Liste zur Weiterverwendung
csv_filename = 'Superalgos_Docs_list.csv'  # Filename for the output csv file. Date/Time (%y%m%d-%h%m) will be added before.

def create_doc_list(project_path = project_path, storage_file = storage_file):
    data = func.filelist(project_path)
    pickle.dump(data, open(storage_file, "wb" ))


# root window
root = tk.Tk()
root.geometry("600x600+0+0")
root.title('SuperalgosDocTranslator')
root.resizable(True, True)

create_list = ttk.Button(root, text="Docs-Liste erstellen", command=create_doc_list)
create_list.bind('<Return>', create_doc_list(project_path, storage_file))
create_list.pack(padx=10, pady=10)

label = ttk.Label(root, text='Seitentitel, resp. Suchbegriff eingeben:')
label.pack(padx=10, pady=10)

suchwort = tk.StringVar()
suchfeld = ttk.Entry(root, textvariable=suchwort)
suchfeld.pack(padx=10, pady=10)
# suchfeld.bind('<Return>', return_pressed)

root.mainloop()
