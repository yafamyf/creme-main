import pyaudio
import numpy as np
import time
import sys

fichier = sys.argv[1]
#print(fichier)
enceinte = int(sys.argv[2])

def detect_sound():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2  # Stéréo
    RATE = 44100
    THRESHOLD = 20  # Seuil de détection ajustable

    p = pyaudio.PyAudio()

    """
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        print(f"Device {i}: {device_info['name']}")
    

    print("test")
"""
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=enceinte)  # Indice de l'entrée virtuelle VAC

    # mettre l'argument ici
    with open(fichier, 'a') as f:

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

if __name__ == "__main__":
    detect_sound()


