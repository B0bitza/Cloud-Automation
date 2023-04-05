import tkinter as tk
from tkinter import ttk
import openpyxl
import paramiko

USERNAME = "user" # credidentiale temporare
PASSWORD = "parola"

workbook = openpyxl.load_workbook('task3.xlsx')
worksheet = workbook['Sheet1']

window = tk.Tk()
window.title("Task3")
window.geometry("700x400")


# Search bar and search button
search_frame = tk.Frame(window)
search_frame.pack(side=tk.TOP, fill=tk.X)

search_label = tk.Label(search_frame, text="Cauta VM:")
search_label.grid(row=0, column=0, padx=5, pady=5, sticky='n')

search_bar = tk.Entry(search_frame, width=50)
search_bar.grid(row=0, column=1, padx=5, pady=5, sticky='n')

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def ssh_connect(vm):
    # SSH client object
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=vm, username=USERNAME, password=PASSWORD)
        ssh_status_label.config(text=f"Conexiune SSH reusita pentru {vm}", fg="green")
        ssh.close()

    except paramiko.AuthenticationException:
        # Displays an authentication error:
        print("Eroare de autentificare. Verifica username-ul si parola.")
        ssh_status_label.config(text=f"Conexiune esuata pentru {vm}. Verifica username-ul si parola.", fg="red")
    except paramiko.SSHException:
        # Displays any other SSH-related error:
        print("Eroare SSH. Verifica conexiunea la retea.")
        ssh_status_label.config(text=f"Conexiune esuata pentru {vm}. Verifica conexiunea la retea.", fg="red")
    except Exception as e:
        # Displays any other error:
        print("Unexpected error:", e)
        ssh_status_label.config(text=f"Conexiune esuata pentru {vm}. Unexpected error {e}.", fg="red")

search_button = tk.Button(search_frame, text="Cauta", command="") #caici va veni functia search, command=search
search_button.grid(row=0, column=2, padx=5, pady=5, sticky='n')

ssh_status_label = tk.Label(search_frame, text="")
ssh_status_label.grid(row=1, columnspan=3, padx=5, pady=5, sticky='n')

search_frame.columnconfigure(1, weight=1)

# Canvas widget with scrollbar
canvas = tk.Canvas(window)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

# Frame to hold the data
data_frame = tk.Frame(canvas)

# Add the frame to the Canvas widget
canvas.create_window((0, 0), window=data_frame, anchor='nw')

# Run the Tkinter event loop
window.mainloop()