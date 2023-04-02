import tkinter as tk
import paramiko


# Creaza o fereastra
root = tk.Tk()
root.title("SSH Client")
root.geometry("700x400")

username = "root" # username si parola temporare
password = "parola"

# Creaza un dictionar cu adresele IP ale serverelor
vm_data = { "123" : {"username": username, "password": password},
            "124" : {"username": username, "password": password},
            "125" : {"username": username, "password": password},
}

# Creeaza o functie pentru cautarea unei adrese IP
def search():
    ip_address = search_bar.get()
    if ip_address in vm_data:
        # Datele de autentificare pentru VM
        username = vm_data[ip_address]["username"]
        password = vm_data[ip_address]["password"]
        
        # Creaza un obiect SSHClient
        ssh = paramiko.SSHClient()

        # Adauga cheia SSH a serverului la lista de chei cunoscute
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Conectare la server
            ssh.connect(ip_address, username=username, password=password)

            # Afiseaza mesaj de conectare reusita
            print("Conectare reusita la", ip_address)

            # Inchide conexiunea SSH
            ssh.close()
        except paramiko.AuthenticationException:
            # Se afiseaza daca autentificarea a esuat
            print("Eroare de autentificare. Verifica username-ul si parola.")
        except paramiko.SSHException:
            # Afiseaza orice alta exceptie SSH-related
            print("Eroare SSH. Verifica conexiunea la retea.")
        except Exception as e:
            # Afiseaza orice alta exceptie
            print("Unexpected error:", e)
    else:
        # Afiseaza mesaj daca adresa IP nu exista in dictionar
        print("Adresa IP nu exista in dictionar.")

# Creeaza un label pentru introducerea adresei IP
search_label = tk.Label(root, text="Cauta VM:")
search_bar = tk.Entry(root, width=50)

# Adauga un buton search pentru cautarea adresei IP
search_button = tk.Button(root, text="Cauta", padx=10, pady=5, command=search)

# Adauga elementele in interfata grafica
search_label.grid(row=0, column=0, padx=5, pady=5, sticky='n')
search_bar.grid(row=0, column=1, padx=5, pady=5, sticky='n', columnspan=1)
search_button.grid(row=0, column=2, padx=5, pady=5, sticky='n')

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)

# Ruleaza aplicatia
root.mainloop()