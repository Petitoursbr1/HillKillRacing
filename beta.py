import tkinter as tk
from pymem import Pymem
import psutil
import time

# Adresses des valeurs à modifier
GEMMES_ADDR = 0x61CAEC
PIECES_ADDR = 0x61CAD4

# Ouvrir le processus HillClimbRacing.exe
process_name = "HillClimbRacing.exe"

def find_process():
    """Trouvez le processus HillClimbRacing.exe."""
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None

# Fonction pour lire la valeur à partir d'une adresse
def read_value(pm, address):
    return pm.read_int(address)

# Fonction pour écrire une nouvelle valeur à une adresse
def write_value(pm, address, value):
    pm.write_int(address, value)

# Fonction pour mettre à jour l'affichage des valeurs
def update_values():
    try:
        pm = Pymem(find_process())
        gemmes_value = read_value(pm, GEMMES_ADDR)
        pieces_value = read_value(pm, PIECES_ADDR)
        gemmes_var.set(gemmes_value)
        pieces_var.set(pieces_value)
    except Exception as e:
        print(f"Erreur lors de la lecture des valeurs: {e}")

# Fonction pour modifier les valeurs
def modify_values():
    try:
        pm = Pymem(find_process())
        new_gemmes = gemmes_var.get()
        new_pieces = pieces_var.get()
        write_value(pm, GEMMES_ADDR, new_gemmes)
        write_value(pm, PIECES_ADDR, new_pieces)
        update_values()
    except Exception as e:
        print(f"Erreur lors de l'écriture des valeurs: {e}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Modifier les valeurs de Hill Climb Racing")

# Variables pour les valeurs
gemmes_var = tk.IntVar()
pieces_var = tk.IntVar()

# Création des éléments de l'interface
tk.Label(root, text="Gemmes:").grid(row=0, column=0)
tk.Entry(root, textvariable=gemmes_var).grid(row=0, column=1)

tk.Label(root, text="Pièces:").grid(row=1, column=0)
tk.Entry(root, textvariable=pieces_var).grid(row=1, column=1)

tk.Button(root, text="Modifier", command=modify_values).grid(row=2, column=0, columnspan=2)
tk.Button(root, text="Mettre à jour", command=update_values).grid(row=3, column=0, columnspan=2)

# Mettre à jour les valeurs initiales
update_values()

# Lancer la boucle principale de l'interface
root.mainloop()

