import tkinter as tk
from pymem import Pymem
import psutil

# Variables globales pour les adresses
GEMMES_ADDR = None
PIECES_ADDR = None

# Nom du processus
process_name = "HillClimbRacing.exe"

def find_process():
    """Trouve le processus HillClimbRacing.exe et retourne son PID."""
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None

def scan_memory_for_value_in_range(pm, value, start_address, end_address):
    """Scanne la mémoire dans une plage spécifique pour trouver l'adresse contenant une valeur."""
    value_hex = int(value)
    step_size = 0x1  # Taille des étapes du scan
    total_steps = (end_address - start_address) // step_size  # Nombre total d'étapes

    for i, address in enumerate(range(start_address, end_address, step_size)):
        try:
            if pm.read_int(address) == value_hex:
                print(f"Adresse trouvée : {hex(address)}")
                return address
        except:
            continue

        # Affichage de la progression dans le terminal
        if i % 1000 == 0:  # Afficher la progression toutes les 1000 étapes
            progress_percentage = (i / total_steps) * 100
            print(f"Progression : {progress_percentage:.2f}%")

    return None

def locate_addresses():
    """Localise les adresses de pièces et gemmes en fonction de leurs valeurs actuelles."""
    global GEMMES_ADDR, PIECES_ADDR
    try:
        pid = find_process()
        if not pid:
            raise Exception("Processus non trouvé.")
        
        pm = Pymem(pid)

        # Récupération des valeurs saisies par l'utilisateur
        current_gemmes = int(gemmes_current_var.get())
        current_pieces = int(pieces_current_var.get())

        # Plages d'adresses spécifiques pour les pièces et les gemmes
        pieces_start_address = 0x00CAD4
        pieces_end_address = 0xFFCAD4
        gemmes_start_address = 0x00CACE
        gemmes_end_address = 0xFFCACE

        print("Scan des pièces...")
        PIECES_ADDR = scan_memory_for_value_in_range(pm, current_pieces, pieces_start_address, pieces_end_address)
        if PIECES_ADDR is None:
            raise Exception("Adresse des pièces non localisée.")
        
        print("Scan des gemmes...")
        GEMMES_ADDR = scan_memory_for_value_in_range(pm, current_gemmes, gemmes_start_address, gemmes_end_address)
        if GEMMES_ADDR is None:
            raise Exception("Adresse des gemmes non localisée.")

        print(f"Adresse des pièces trouvée : {hex(PIECES_ADDR)}")
        print(f"Adresse des gemmes trouvée : {hex(GEMMES_ADDR)}")

        update_values()
    except Exception as e:
        print(f"Erreur lors de la localisation des adresses: {e}")

# Fonction pour lire la valeur à partir d'une adresse
def read_value(pm, address):
    return pm.read_int(address)

# Fonction pour écrire une nouvelle valeur à une adresse
def write_value(pm, address, value):
    pm.write_int(address, value)

# Fonction pour mettre à jour l'affichage des valeurs
def update_values():
    try:
        pid = find_process()
        if not pid:
            raise Exception("Processus non trouvé.")
        
        pm = Pymem(pid)
        
        if GEMMES_ADDR is None or PIECES_ADDR is None:
            raise Exception("Les adresses ne sont pas encore localisées.")
        
        gemmes_value = read_value(pm, GEMMES_ADDR)
        pieces_value = read_value(pm, PIECES_ADDR)
        gemmes_var.set(gemmes_value)
        pieces_var.set(pieces_value)
    except Exception as e:
        print(f"Erreur lors de la lecture des valeurs: {e}")

# Fonction pour modifier les valeurs
def modify_values():
    try:
        pid = find_process()
        if not pid:
            raise Exception("Processus non trouvé.")
        
        pm = Pymem(pid)
        
        new_gemmes = gemmes_var.get()
        new_pieces = pieces_var.get()
        
        if GEMMES_ADDR is None or PIECES_ADDR is None:
            raise Exception("Les adresses ne sont pas encore localisées.")
        
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

# Variables pour les valeurs actuelles saisies
gemmes_current_var = tk.IntVar()
pieces_current_var = tk.IntVar()

# Interface pour entrer les valeurs actuelles des gemmes et pièces
tk.Label(root, text="Valeur actuelle des gemmes:").grid(row=0, column=0)
tk.Entry(root, textvariable=gemmes_current_var).grid(row=0, column=1)

tk.Label(root, text="Valeur actuelle des pièces:").grid(row=1, column=0)
tk.Entry(root, textvariable=pieces_current_var).grid(row=1, column=1)

tk.Button(root, text="Localiser adresses", command=locate_addresses).grid(row=2, column=0, columnspan=2)

# Interface pour modifier les valeurs des gemmes et pièces
tk.Label(root, text="Nouvelle valeur des gemmes:").grid(row=3, column=0)
tk.Entry(root, textvariable=gemmes_var).grid(row=3, column=1)

tk.Label(root, text="Nouvelle valeur des pièces:").grid(row=4, column=0)
tk.Entry(root, textvariable=pieces_var).grid(row=4, column=1)

tk.Button(root, text="Modifier", command=modify_values).grid(row=5, column=0, columnspan=2)
tk.Button(root, text="Mettre à jour", command=update_values).grid(row=6, column=0, columnspan=2)

# Lancer la boucle principale de l'interface
root.mainloop()
