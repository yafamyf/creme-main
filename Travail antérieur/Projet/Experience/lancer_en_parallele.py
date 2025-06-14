import threading
import tkinter as tk
import time
import sys
import pyaudio
import numpy as np

import contextlib
with contextlib.redirect_stdout(None):
    import pygame

def detect_sound(identifiant, enceinte):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2  # Stéréo
    RATE = 44100
    THRESHOLD = 20  # Seuil de détection ajustable

    p = pyaudio.PyAudio()
    print("pyaudio lancé")

    # # Vérification des channels des devices actifs
    # for i in range(p.get_device_count()):
    #     dev = p.get_device_info_by_index(i)
    #     print(f"Device {i}: {dev['name']} (Max Input Channels: {dev['maxInputChannels']}, Max Output Channels: {dev['maxOutputChannels']}, Default Sample Rate: {dev['defaultSampleRate']})")
        
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=enceinte)  # Indice de l'entrée virtuelle VAC

    # mettre l'argument ici
    chemin_fichier = PathDonnee + "/DetectionSon.txt"
    print("chemin_fichier dans la fonction detect_sound", chemin_fichier)
    with open(chemin_fichier, 'a') as f:
        debutTime = time.time()
        while True:
            data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
            rms = np.sqrt(np.mean(np.square(data)))
            if rms > THRESHOLD:
                Timer = time.time()
                print(Timer, file=f)
                break
            if time.time()-debutTime > 40:
                print(1, file=f)
                break

    stream.stop_stream()
    stream.close()
    p.terminate()
    exit()


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

def touchpad(temps, fichier):
    """Crée une interface graphique avec un bouton et enregistre les clics dans un fichier."""
    global ListeInput
    ListeInput = []

    # Créer la fenêtre principale
    root.title("Ecoutez la séquence et tapez pour effectuer la tâche")

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
    if "Reproduction" in PathDonnee:
        text_button = "Tapez sur le touchpad pour battre le rythme de la séquence"
    else:
        if "Perception" in PathDonnee:
            text_button = "Tapez sur le touchpad pour battre la pulsation de la séquence"
    button = tk.Button(root, text=text_button, bg="light blue", fg="black", font=("Arial", 12), command=on_button_click)
    button.grid(row=0, column=0, sticky="nsew")

    root.update_idletasks()

    temporisateur = int(temps) * 1000

    # Lancer la boucle principale
    with open(fichier, 'a') as f:
        root.after(temporisateur, close_program)
        root.after(1, lambda: root.attributes('-topmost', True))
        root.after(1, lambda: root.focus_force())
        root.mainloop()

        if ListeInput:
            print(ListeInput, file=f)
        else:
            print([1, 2, 3], file=f)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script.py <chemin_du_fichier_midi> <temps> <identifiant> <enceinte> <PathDonnee>")
        sys.exit(1)

    # Arguments pour les fonctions
    chemin_fichier_midi = sys.argv[1]
    #print("chemin_fichier_midi = ", chemin_fichier_midi)
    temps = sys.argv[2]
    print("temps = ", temps)
    
    identifiant = sys.argv[3]
    print("identifiant = ", identifiant)
    
    enceinte = int(sys.argv[4])
    print("Enceinte : ", enceinte)

    PathDonnee = sys.argv[5]
    fichier_sortie = PathDonnee + "/RetranscriptionInput.txt"
    print("fichier_sortie = ", fichier_sortie)


    # Initialiser la fenêtre principale
    root = tk.Tk()
    ListeInput = []

    # Thread pour la détection de son
    thread1 = threading.Thread(target=detect_sound, args=(identifiant, enceinte))
    thread1.start()

    # Thread pour exécuter la fonction lire_fichier_midi
    thread2 = threading.Thread(target=lire_fichier_midi, args=(chemin_fichier_midi,))
    thread2.start()


    # Exécuter la fonction touchpad dans le thread principal
    touchpad(temps, fichier_sortie)
