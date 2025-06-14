import threading
import pygame
import tkinter as tk
import time
import sys

def lire_fichier_midi(chemin_fichier):
    """Lit et joue un fichier MIDI en utilisant pygame."""
    try:
        # Initialiser pygame mixer
        pygame.mixer.init()

        # Charger le fichier MIDI
        pygame.mixer.music.load(chemin_fichier)

        # Jouer le fichier MIDI
        pygame.mixer.music.play()

        # Attendre que la lecture soit terminée
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except pygame.error as e:
        print(f"Erreur pygame : {e}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    finally:
        # Quitter pygame mixer
        pygame.mixer.quit()

def on_button_click():
    """Gère le clic sur le bouton en enregistrant le temps actuel."""
    temps_debut = time.time()
    print("time : ", temps_debut)
    ListeInput.append(temps_debut)

def close_program():
    """Ferme la fenêtre principale."""
    root.destroy()

def combined_action():
  root.focus_force()
  on_button_click()

def touchpad(temps, fichier):
    """Crée une interface graphique avec un bouton et enregistre les clics dans un fichier."""
    global ListeInput
    ListeInput = []

    # Créer la fenêtre principale
    root.title("Si si si, si si si, ré# si si la sol la si")

    root.lift()
    root.attributes('-topmost', True)
    root.after(500, lambda: root.attributes('-topmost', False))
    root.after(500, lambda: root.focus_force())


    # Centrer la fenêtre
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    # Configurer la grille pour que le bouton prenne tout l'espace
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # Créer et placer le bouton
    button = tk.Button(root, text="Battre la pulsation", bg="light blue", fg="black", font=("Arial", 12), command=combined_action)
    button.grid(row=0, column=0, sticky="nsew")

    root.update_idletasks()

    temporisateur = int(temps) * 1000

    # Lancer la boucle principale
    with open(fichier, 'a') as f:
        root.after(temporisateur, close_program)
        root.mainloop()

        if ListeInput:
            print(ListeInput, file=f)
        else:
            print([1, 2, 3], file=f)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <chemin_du_fichier_midi> <temps> <fichier_sortie>")
        sys.exit(1)

    # Arguments pour les fonctions
    chemin_fichier_midi = sys.argv[1]
    temps = sys.argv[2]
    fichier_sortie = sys.argv[3]

    # Initialiser la fenêtre principale
    root = tk.Tk()
    ListeInput = []

    # Créer un thread pour exécuter la fonction lire_fichier_midi
    thread1 = threading.Thread(target=lire_fichier_midi, args=(chemin_fichier_midi,))

    # Démarrer le thread pour lire_fichier_midi
    thread1.start()

    # Exécuter la fonction touchpad dans le thread principal
    touchpad(temps, fichier_sortie)
    close_program()
    # Attendre que le thread lire_fichier_midi se termine
    # thread1.join() 