import numpy as np

def main(Chemin, Duree):

    if Duree == 1:
        DureeExperience = 20
    elif Duree == 2:
        DureeExperience = 40
    #Je fais juste une mesure de plus, est ce qu'il faut que je sois plus precis ?

    MatriceTimeTempo = np.array([[0,0,0,0],
                        [0,0,0,0]])


    # Ouvrir le fichier en mode lecture
    with open(Chemin, 'r') as file:
        # Skip la premiere ligne
        next(file)
        # Lire toutes les autres lignes du fichier
        lines = file.readlines()

        # Parcourir chaque ligne
        for line in lines:
            # Diviser la ligne en colonnes en utilisant la virgule comme délimiteur
            Colonne = line.split(',')
            TimeDebut = float(Colonne[0])
            Tempo = float(Colonne[3])
            # 20 sec car (16pulse + ~5seconde de processus) * 60 sec / bpm
            Temps = (DureeExperience * 60 / Tempo)
            TimeFin = TimeDebut+Temps
            NumeroSequence = float(Colonne[2])
            Complexite = float(Colonne[4])

            
            NouvelleLigne = [TimeDebut,TimeFin,NumeroSequence,Complexite]
            MatriceTimeTempo = np.insert(MatriceTimeTempo, -1, NouvelleLigne, axis=0)


    MatriceTimeTempo = np.delete(MatriceTimeTempo, 0, axis=0)
    MatriceTimeTempo = np.delete(MatriceTimeTempo, -1, axis=0)
    #print(MatriceTimeTempo[:][:])

    
    """
    for Sequence in MatriceTimeTempo:
        print(Sequence[0], Sequence[1], Sequence[2])
    """
    
    return MatriceTimeTempo


#main("PremiereDonneePourEDA/DataDanielPovel.csv")