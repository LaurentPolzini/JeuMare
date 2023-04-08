# -*- coding: utf-8 -*- 
import os
import random
import time


PV : str = '○' # Pion Vide
PP : str = '☻' # Pion Plein
CV : str = ' ' # Case Vide

NB_PV = 0
NB_PP = 0


JOUEUR = {1: PV, 2 : PP} # repartition des pions selon les 2 joueurs

SIMPLE = "simple"
SAUT = "saut"

grille_depart = [[PP, PP, PP, PP, PP, PP, PV],
                 [PP, PP, PP, PP, PP, PV, PV], 
                 [PP, PP, PP, PP, PV, PV, PV], 
                 [PP, PP, PP, CV, PV, PV, PV],
                 [PP, PP, PP, PV, PV, PV, PV],
                 [PP, PP, PV, PV, PV, PV, PV],
                 [PP, PV, PV, PV, PV, PV, PV]]


grille_milieu = [[PP, PP, PP, CV, CV, CV, CV],
                 [CV, PP, CV, CV, PP, PV, PV], 
                 [CV, CV, CV, PP, PV, PV, CV], 
                 [CV, PP, CV, CV, PV, PV, CV],
                 [CV, CV, CV, PV, PV, PV, CV],
                 [PP, PP, CV, PV, CV, CV, CV],
                 [CV, PV, PV, CV, CV, CV, CV]]

grille_enchainement = [[PP, PP, PV, PP, CV, PP, CV],
                       [CV, CV, PP, CV, PP, CV, PP],
                       [CV, PP, CV, PP, CV, PP, CV],
                       [CV, CV, CV, CV, CV, CV, CV],
                       [CV, CV, CV, CV, CV, CV, CV],
                       [CV, CV, CV, CV, CV, CV, CV],
                       [CV, CV, CV, CV, CV, CV, CV]]

"""
    Enchainement possible des Noirs et des Blancs mettant fin à la partie 
        en 1 coup (plutot plusieurs sauts mais en 1 seul enchainement)
"""
grille_fin = [[CV, CV, CV, CV, CV, CV, CV],
              [CV, PP, CV, PP, PP, PV, CV], 
              [CV, CV, CV, PP, CV, CV, PV], 
              [CV, CV, CV, CV, CV, PV, CV],
              [CV, CV, CV, CV, PV, PV, CV],
              [CV, PP, PV, PP, CV, CV, CV],
              [CV, PV, PP, CV, CV, PP, CV]]


########  ATELIER 2 ########    


"""
    Fonction qui vérifie que les coordonnées appartiennent effectivement à la grille.
        La grille est de taille 7 * 7, elle s'étend donc de la case A1 à G7.
    
    Compare le code Ascii et retourne un booleen
"""
def est_dans_grille(ligne : str, colonne : int) -> bool:
    ligne = str(ligne).upper()
    colonne = str(colonne)
    if len(ligne) != 1 or len(colonne) != 1:
        return False
    
    return (ord('A') <= ord(ligne) <= ord('G') and \
            ord('1') <= ord(colonne) <= ord('7'))


"""
    Fonction ayant pour but de vérifier le bon formatage de l'utilisateur lorsqu'il entre
        des informations.
"""
def est_au_bon_format(coord : str) -> bool: #compare le code Ascii et retourne un booleen
    coord = str(coord).upper()
    if len(coord) != 2:
        return False
    
    return (ord('A') <= ord(coord[0]) <= ord('Z')) and \
        (48 <= ord(coord[1]) <= 57)


"""
    Fonction demandant à l'utilisateur de saisir des coordonnées. Il va sans dire qu'elles
        appartiendront à la grille -nous utiliserons les fonctions précédentes-.
        
        
    Modifications sur cette fonction: ajout de 2 parametres: grille et joueur pour etre
        sur que le joueur a saisie une coordonnée d'un de ses pions.
    
    Autre modification: ajout de la possibilité de sauvegarder une partie
        LA SAUVEGARDE EST ENREGISTREE DANS LE DOSSIER COURANT DU FICHIER PYTHON
"""
def saisir_coord(grille, joueur) -> str:
    coord = str(input("Entrez une coordonnée d'un de vos pions (entre A1 et G7) (save ou abandonner): ")).upper()

    if coord == "SAVE":
        sauvegarde_partie(grille, joueur)
    
    elif coord == "ABANDONNER":
        return -1

    while not (est_au_bon_format(coord) and est_dans_grille(coord[0], coord[1])):
        coord = str(input("Entrez une coordonnée d'un de vos pions (entre A1 et G7) (save ou abandonner): ")).upper()
        if coord == "ABANDONNER":
            return -1
    
    while not (est_au_bon_format(coord) and est_dans_grille(coord[0], coord[1])) \
        or case(grille, coord) != JOUEUR.get(joueur):
        print("Etes vous sur de jouer le bon pion ? ")
        coord = str(input("Entrez une coordonnée d'un de vos pions (entre A1 et G7) (save ou abandonner): ")).upper()
        if coord == "ABANDONNER":
            return -1
    
    
    return coord


"""
    Pour eviter les effets de bords
"""
def copie_grille(grille):
    nouvelle_grille = []
    for i in range(7):
        nouvelle_grille.append([])
        for j in range(7):
            nouvelle_grille[i].append(grille[i][j])
    
    return nouvelle_grille



"""
    Fonction qui affiche la grille.
"""
def affiche_grille(grille):
    for i in range(1, 8):
        print(f"\t| {i}", end="")
   
    for i in range(65, 72): # on utilisera i comme code ascii, d'où ces nombres "aléatoire"
        print("\n", end="")
        for k in range(8):
            print("----", end = "")
        print("--\n", end="") # J'affiche 2 traits car sous Mac la ligne serait trop
                                    #trop courte sans, sous Windows elle peut etre un peu
                                    #plus longue car sous Windows il y a un écart entre 2 "-"
       
        print(chr(i), end="")
        for j in range(1, 8):
            print("\t| {}" .format(grille[i-65][j-1]), end="")
    
    print("\n")
    print("\nJoueur 1: ○        Joueur 2: ☻ \n")


########  ATELIER 3 ########   



"""
    Fonction affichant 2 grilles l'une a cote de l'autre. Utile pour un "avant / apres"
"""
def affiche_deux_grilles(grille1, grille2):
    print("\nGrilles avant                         Après")
    for j in range(2):
        for i in range(1, 8):
            print(f"\t| {i}", end="")
        print("\t \t", end = "")
    
    for i in range(65, 72):
        print("\n", end="")
        for j in range(2):
            for k in range(8):
                print("----", end = "")
            print("--\t", end="")
        print("\n", end = "")
        
        
        print(chr(i), end = "")
        for j in range(1, 8):
            print("\t| {}" .format(grille1[i-65][j-1]), end = "")
        print(f"\t \t{chr(i)}", end = "")
        for j in range(1, 8):
            print("\t| {}" .format(grille2[i-65][j-1]), end = "")
            
            
    print("\n")
    print("\nJoueur 1: ○        Joueur 2: ☻ \n")


# Retourne le contenu de la case entrée
def case(grille, coord) -> str:
    return (grille[ord(coord[0].upper()) - 65][ord(coord[1]) - 49])


# Retourne les pions de l'opposant
def get_pion_opposant(joueur):
    if joueur == 1:
        return PP # les pions opposés aux pions vides sont les pions pleins
    return PV


# decroit le nombre de pion du joueur adverse de "joueur"
def decroit_nb_pion(joueur):
    if joueur == 1:
        global NB_PP # mot clé global permet de changer la variable globale
        NB_PP -= 1
    
    else:
        global NB_PV
        NB_PV -= 1
        


"""
    Permet la saisie d'une direction et retourne un nombre entre 0 et 3 selon la direction
    0 pour droite; 1 pour gauche; 2 pour haut; 3 pour bas.
    
    La saisie d'une direction plutot que d'une case d'arrivee permet d'eviter les erreurs.
                La case d'arrivee sera calculee dans une fonction idoine
"""

def saisie_direction(directions_possibles) -> int:
    print("\nEt quelle serait votre direction ?: ", end = "")
    for i in range(len(directions_possibles)):
        print(" ", get_direction(directions_possibles[i]), end = "")
    print("\n")
    
    direction = str(input("Votre choix: ")).lower()
    
    differente_possibilite_dEntree = ["est", "e", "droite", "d",
                                      "ouest", "o", "gauche", "g",
                                      "nord", "n", "haut", "h",
                                      "sud", "s", "bas", "b"]
    
    while (direction not in differente_possibilite_dEntree):
        direction = str(input("Etes vous sur de ne pas avoir fait d'erreur de frappe? : "))\
            .lower()
    
    print("\n")
    return differente_possibilite_dEntree.index(direction) // 4


"""
    Renvoie la direction selon un int entré en parametre, bien entendu, pour 
        chacunes des fonctions, 0 signifie la droite, etc...
    Cette fonction est utile pour donner les directions possibles à l'utilisateur
"""
def get_direction(direction):
    if direction == 0:
        return "droite"
    elif direction == 1:
        return "gauche"
    elif direction == 2:
        return "haut"
    else:
        return "bas"


"""
    Verifie qu'un mouvement est bien valide
    
    Verifie que les informations entrées par l'utilisateur aboutiront bien à quelque chose
    
"""
def est_mouvement_valide(grille, joueur, mouvement, direction, depart, arriveeSimple):
    valide = True
    
    if not ( est_au_bon_format(arriveeSimple) and \
        est_dans_grille(arriveeSimple[0], arriveeSimple[1]) ):
        return False
    
    if mouvement == SIMPLE:
        if case(grille, arriveeSimple) != CV:
            valide = False
    
    else: # mouvement = SAUT
        arriveeSaut = arrivee_saut(depart, direction)
        if not est_dans_grille(arriveeSaut[0], arriveeSaut[1]):
            return False
        
        if case(grille, arriveeSimple) != get_pion_opposant(joueur) or \
            case(grille, arriveeSaut) != CV:
                valide = False
    
    return valide


"""
    Si le joueur choisit un pion mais qu'aucun mouvement n'est disponnible
"""
def aucun_mouvement(grille, joueur, depart):
    while mouvement_possible(grille, joueur, depart) == -1:
        print("Vous ne pouvez faire aucun mouvement a partir de cette case. Je vous suggère" +
              " de redonner des coordonnées.")
        depart = saisir_coord(grille, joueur)
    
    return depart


"""
    Si le pion choisi ne peut se deplacer qu'avec le mouvement simple et qu'il n'y a
    qu'une possibilite
    Permet aussi au joueur de valider le mouvement
    
    return -1 si l'utilisateur n'est pas d'accord pour effectuer le mouvement.
"""
def seul_mouv_simple_possible(grille, joueur, depart, direction):
    print(f"Il n'y a qu'une seule direction possible ({get_direction(direction)})," +
          " le mouvement simple s'effectue tout seul")
    consentant = str(input("Est ce que cela vous convient (entrée | n)? ")).upper()
    if consentant == "O" or consentant == "Y" or consentant == "OUI" or consentant == "":
        return direction
    else:
        print("Il va falloir tout refaire.\n")
        return -1


"""
    Seul le saut est possible; retourne la direction si l'utilisateur est d'accord
        sinon retourne -1
"""
def seul_mouv_saut_possible(grille, joueur, depart, direction):
    print(f"Il n'y a qu'une seule direction possible ({get_direction(direction)})," +
          " le mouvement saut s'effectue tout seul")
    consentant = str(input("Est ce que cela vous convient (entree | n)? ")).upper()
    if consentant == "O" or consentant == "Y" or consentant == "OUI" or consentant == "":
        return direction
    else:
        print("Il va falloir tout refaire.\n")
        return -1


"""
    Si les 2 mouvements sont possibles il faut les demander; demande le mouvement
        tant que l'utilisateur n'a pas fait une bonne saisie.
    Nb: Si un seul mouvement est possible, il est demandé à l'utilisateur son accord
        pour le deplacement automatique du pion. (Cette proposition ne se fait pas
                                                          dans cette fonction)  
    
    
    Retourne le mouvement entré
"""
def demande_mouvement():
    mouv = str(input("\nQuel mouvement souhaitez-vous faire ? (simple (si) ou" +
                         " saut (sa)): "))
    mouv = mouv.lower()
    different_mouvement = [SIMPLE, SAUT, "si", "sa"]
    while (mouv not in different_mouvement):
        mouv = str(input("Il y a une faute de frappe, veuillez retaper svp: "))
     
    if mouv == "si":
        mouv = SIMPLE
    else:
        mouv = SAUT
    
    return mouv
    


"""
    Demande le triplet depart mouvement et direction et le retourne
    
    Est appellé au debut de chaque tour ou s'il y a un probleme dans les informations entrées
            par exemple le joueur demande de faire un deplacement en dehors de la grille
"""
def demande_depart_mouv_dir(grille, joueur):
    print("Quel pion souhaitez vous deplacer ? ")
    depart = saisir_coord(grille, joueur)
    if depart == -1:
        return -1, -1, ""
    
    direction = -1 # j'initialise la direction et le mouvement
    mouv = ""
    
    mouv_possible = mouvement_possible(grille, joueur, depart)
    
    if mouv_possible == -1:
        depart = aucun_mouvement(grille, joueur, depart)
        mouv_possible = mouvement_possible(grille, joueur, depart)
        
    
    if mouv_possible == 1:
        mouv = SIMPLE
        direction = direction_selon_mouv(grille, joueur, depart, mouv)
        
        
    elif mouv_possible == 2:
        mouv = SAUT
        direction = direction_selon_mouv(grille, joueur, depart, mouv)
    
    else: # 2 mouvements possible, il faut tout demander
        mouv = demande_mouvement()
        direction = direction_selon_mouv(grille, joueur, depart, mouv)
        
    while direction == -1:
        depart, mouv, direction= demande_depart_mouv_dir(grille, joueur)
    

    return depart, mouv, direction




"""
    Trouve la direction soit s'il n'y a qu'une possibilite renvoie la direction de celle derniere
    S'il y en a plusieurs, demande la direction.
    
    Peut retourner -1 si l'utilisateur ne veut pas effectuer le mouvement 
        (voir fonctions seul_mouv_simple_possible et seul_mouv_saut_possible)
"""
def direction_selon_mouv(grille, joueur, depart, mouvement):
    direction = -1
    if mouvement == SIMPLE:
        simple_possibilite = possibilite_simple(grille, joueur, depart)
        if simple_possibilite != 5: # une seule direction possible (entre 0 et 3 compris)
            direction = seul_mouv_simple_possible(grille, joueur, depart, simple_possibilite)
        else:
            print("Vous ne pouvez faire que le deplacement SIMPLE")
            direction = saisie_direction(liste_directions_simple(grille, joueur, depart)) 
            #plusieurs directions possible car simple_possibilite= 5
    
    elif mouvement == SAUT:
        saut_possibilite = possibilite_sauts(grille, joueur, depart)
        if saut_possibilite != 5:
            direction = seul_mouv_saut_possible(grille, joueur, depart, saut_possibilite)
        else:
            print("Vous ne pouvez faire que le deplacement SAUT")
            direction = saisie_direction(liste_directions_saut(grille, joueur, depart))
    
    return direction





"""
    Retourne -1 si aucun mouvement possible
    Retourne 1 si mouvement simple possible (et pas saut)
    Retourne 2 si mouvement saut possible (et pas simple)
    Retourne 3 si les 2 mouvements sont possibles
"""
def mouvement_possible(grille, joueur, depart):
    simple = possibilite_simple(grille, joueur, depart)
    saut = possibilite_sauts(grille, joueur, depart)
    
    if simple == -1 and saut == -1:
            return -1
    
    elif simple >= 0 and saut == -1:
            return 1
        
    elif simple == -1 and saut >= 0:
            return 2
    
    return 3



"""
    Elle appelle la fonction d'appel de mouvement avec le triplet depart mouv direction
    
    Si un autre saut est possible, propose d'enchainer.
    
    La grille changée est retournée par la fonction
"""
def tourJoueur(grille, joueur) -> list:
    
    depart, mouv, direction = demande_depart_mouv_dir(grille, joueur)
    if depart == -1 and mouv == -1 and direction == "":
        return -1
    
    arriveeSimple = arrivee_simple(depart, direction)
    
    while not(est_mouvement_valide(grille, joueur, mouv, direction,\
                                   depart, arriveeSimple)):
        print("Le mouvement ne colle pas avec la direction, veuillez tout ressaisir.\n")
        depart, mouv, direction = demande_depart_mouv_dir(grille, joueur)
    
    nouvelle_grille = appel_mouvement(grille, joueur, depart, direction, mouv)
    
    if mouv == SAUT:
        depart = arrivee_saut(depart, direction)
        nouvelle_grille = enchainement(nouvelle_grille, joueur, depart)
        
    
    return nouvelle_grille


"""
    Prend toutes les positions de pions possibles
    Y associe toutes les directions possibles
    
    Choisi un pion au hasard tant qu'il y a des deplacements possibles
    Choisi un déplacement au hasard et enfin y associe un direction
    
    Entre toutes ces coordonéees et effectue le mouvement
    Si deplacement = saut, regarde si peut refaire saut
    si oui, choisi au hasard d'en refaire.
"""
def tourOrdinateur(grille, joueur):
    pionDepart, mouvement, direction = determineDepartMouvementDirection(grille, joueur)
    
    nouvelle_grille = appel_mouvement(grille, joueur, pionDepart, direction, mouvement)
    
    # ce qui suit est l'enchainement
    while (2 <= mouvement_possible(grille, joueur, pionDepart) <= 3):
        pionDepart = arrivee_saut(pionDepart, direction)
        enchaine = random.randint(0, 1) # 1 enchaine sinon non
        if (enchaine == 1):
            directions = liste_directions_saut(grille, joueur, pionDepart)
            if (directions != []):
                direction = directions[random.randint(0, len(directions) - 1)]
                nouvelle_grille = appel_mouvement(grille, joueur, pionDepart, direction, SAUT)
            else:
                break
        
        else:
            break
    
    return nouvelle_grille


def determineDepartMouvementDirection(grille, joueur):
    # toutesDirection est du style {'A3' : {SAUT : [1,2], SIMPLE : [3, 4]}}
    toutPionsEtDeplacements = initieDeplacement(grille, joueur, pionDepartOrdi(grille, joueur))
    # pionDepart est donc égal à une valeur du style A3
    pionDepart = list(toutPionsEtDeplacements)[random.randint(0, len(toutPionsEtDeplacements) - 1)]
    
    # tousMouvementsPionDepart est du style {SAUT : [1,2], SIMPLE : [3, 4]}
    tousMouvementsPionDepart = toutPionsEtDeplacements[pionDepart]
    # ainsi, mouvement = SAUT ou SIMPLE

    while (len(tousMouvementsPionDepart) == 0):
        pionDepart = list(toutPionsEtDeplacements)[random.randint(0, len(toutPionsEtDeplacements) - 1)]
        tousMouvementsPionDepart = toutPionsEtDeplacements[pionDepart]

    mouvement = list(tousMouvementsPionDepart)[random.randint(0, len(tousMouvementsPionDepart) - 1)]
    # direction = une direction parmis le mouvement
    
    toutesDirection = toutPionsEtDeplacements[pionDepart][mouvement]
    direction = toutesDirection[random.randint(0, len(toutesDirection) - 1)]
    
    return pionDepart, mouvement, direction
    



"""
    Va stocker dans un dictionnaire toutes les positions des pions alliés
"""
def pionDepartOrdi(grille, joueur):
    pionsDispo = {}
    for i in range(7):
        for j in range(7):
            if grille[i][j] == JOUEUR.get(joueur):
                pionsDispo[chr(i + 65) + chr(j + 49)] = {}
                
    return pionsDispo


"""
    Initie toutes les directions possibles:
        un dictionnaire pour tous les mouvements simple
        et un autre pour tous les sauts.
"""
def initieDeplacement(grille, joueur, pionsDict):
    pionsAvecDirections = pionsDict
    for coord in pionsDict:
        directSimple = liste_directions_simple(grille, joueur, coord)
        if len(directSimple) != 0:
            pionsAvecDirections[coord][SIMPLE] = directSimple
            
        directSaut = liste_directions_saut(grille, joueur, coord)
        if len(directSaut) != 0:
            pionsAvecDirections[coord][SAUT] = directSaut
    
    return pionsAvecDirections



"""
    Appelle le mouvement entré en paramètre et retourne la nouvelle grille
"""
def appel_mouvement(grille, joueur, depart, direction, mouvement):
    
    nouvelle_grille = grille
    arriveeSimple = arrivee_simple(depart, direction)
    
    if mouvement == SIMPLE:
        
        nouvelle_grille = mouvement_simple(grille, joueur, depart, arriveeSimple, direction)
        
    elif mouvement == SAUT:
        arrivee = arrivee_saut(depart, direction)
        nouvelle_grille = mouvement_saut(grille, joueur, depart, arrivee, direction, arriveeSimple)
    
    
    return nouvelle_grille



"""
    Calcul la case d'arrivée selon une case de départ et une direction
"""
def arrivee_simple(depart, direction) -> str:
    arrivee = ""
    if direction == 0:
        arrivee = depart[0] + str(int(depart[1]) + 1) # a droite
    elif direction == 1:
        arrivee = depart[0] + str(int(depart[1]) - 1) # a gauche
    elif direction == 2:
        arrivee = chr(ord(depart[0]) - 1) + depart[1] # en haut
    elif direction == 3:
        arrivee = chr(ord(depart[0]) + 1) + depart[1] # en bas
    
    return arrivee


"""
    Meme commentaire
"""
def arrivee_saut(depart, direction) -> str:
    arrivee = ""
    if direction == 0:
        arrivee = depart[0] + str(int(depart[1]) + 2) # a droite
    elif direction == 1:
        arrivee = depart[0] + str(int(depart[1]) - 2) # a gauche
    elif direction == 2:
        arrivee = chr(ord(depart[0]) - 2) + depart[1] # en haut
    elif direction == 3:
        arrivee = chr(ord(depart[0]) + 2) + depart[1] # en bas
    
    return arrivee


"""
    Retourne -1 si il n'y a pas de saut possibles, si 1 seul saut possible retourne la direction
        si plusieurs saut possibles retourne 5
        
    Si ce qui est retourné est compris entre 0 et 4 c'est une direction; -1 pas de saut;
        5 c'est qu'il y a plusieurs sauts possibles
        
    Utile pour: enchainement (si possibilité de faire un saut) et faire le saut automatiquement
        si possibilité unique
"""
def possibilite_sauts(grille, joueur, depart):
    direction_possibles = []
    
    for i in range(4): # 4 cases orthogonales
        arriveeSimple = arrivee_simple(depart, i)
        if est_mouvement_valide(grille, joueur, SAUT, i, depart, arriveeSimple): # validité du saut
            direction_possibles.append(i) # on ajoute la direction possible dans le tableau
    
    if len(direction_possibles) == 1:
        return direction_possibles[0] # s'il n'y a qu'une direction possible la retourne
    
    elif len(direction_possibles) == 0:
        return -1
    
    return 5



"""
    Retourne la liste des directions possibles pour le mouvement saut
        
"""
def liste_directions_saut(grille, joueur, depart):
    direction_possibles = []
    
    for i in range(4): # 4 cases orthogonales
        arriveeSimple = arrivee_simple(depart, i)
        if est_mouvement_valide(grille, joueur, SAUT, i, depart, arriveeSimple): # validité du saut
            direction_possibles.append(i)
    
    return direction_possibles

"""
    Si retour entre 0 et 3: direction unique case vide autour
    Si retour == 5: plusieurs directions possible
    Si retour == -1: aucune case vide autour
"""
def possibilite_simple(grille, joueur, depart) -> int:
    case_vide_autour = []
    for i in range(4):
        arriveeSimple = arrivee_simple(depart, i)
        if est_mouvement_valide(grille, joueur, SIMPLE, i, depart, arriveeSimple):
            case_vide_autour.append(i)
    
    if len(case_vide_autour) == 1:
        return case_vide_autour[0]
    
    elif len(case_vide_autour) == 0:
        return -1
    
    return 5


"""
    Retourne la liste des directions possibles pour le mouvement simple
"""
def liste_directions_simple(grille, joueur, depart):
    case_vide_autour = []
    for i in range(4):
        arriveeSimple = arrivee_simple(depart, i)
        if est_mouvement_valide(grille, joueur, SIMPLE, i, depart, arriveeSimple):
            case_vide_autour.append(i)
    
    return case_vide_autour


"""
    Change la grille selon les conséquences du mouvement
"""
def mouvement_simple(grille, joueur, depart, arrivee, direction):
    grille[ord(arrivee[0]) - 65][ord(arrivee[1]) - 49] = JOUEUR.get(joueur) # Deplace le pion
    grille[ord(depart[0]) - 65][ord(depart[1]) - 49] = CV # Rend la case de départ vide
    
    return grille


"""
    Change la grille selon les conséquences du mouvement
"""
def mouvement_saut(grille, joueur, depart, arrivee, direction, caseEntreDepartArrivee):
    grille[ord(depart[0]) - 65][ord(depart[1]) - 49] = CV # Rend la case de départ vide
    grille[ord(caseEntreDepartArrivee[0]) - 65]\
        [ord(caseEntreDepartArrivee[1]) - 49] = CV # Rend la case de saut vide
        
    grille[ord(arrivee[0]) - 65][ord(arrivee[1]) - 49] = JOUEUR.get(joueur) # Deplace le pion
    
    decroit_nb_pion(joueur) # decroit les pions du joueur ennemi
    
    return grille



def enchainement(grille, joueur, depart):
    nouvelle_grille = grille
    while 2 <= mouvement_possible(grille, joueur, depart) <= 3: #saut possible a l'arrivee
        print("Voici la grille après avoir sauté: \n")
        affiche_grille(nouvelle_grille)
        
        print(f"Votre case d'arrivee: {depart}\n")
        consentant = str(input("Vous pouvez refaire au moins un saut, voulez vous enchainer (entree | n) : ")).upper()
        if consentant == "O" or consentant == "YES" or consentant == "OUI" \
            or consentant == "":
            direction = direction_selon_mouv(grille, joueur, depart, SAUT)
            if direction == -1:
                break # direction non valide, joueur ne veut pas continuer
            
            nouvelle_grille = appel_mouvement(grille, joueur, depart, direction, SAUT)
            depart = arrivee_saut(depart, direction)
        else:
            break # fin enchainement, plus de saut possible
    
    return nouvelle_grille


"""
    Fonction de jeu: permet de charger une partie si l'utilisateur le veut et a en effet
        une sauvegarde de faite.
    Tant que un des 2 joueurs a plus de 6 pions, appelle la fonction saisie pour mouvement
"""
def jeuJcJ(grille):
    global NB_PP, NB_PV
    joueur = 1
    
    charger_partie = str(input("Voulez-vous charger la derniere partie sauvegardée (o | n)? ")).upper()
    
    if charger_partie == "O":
        grille, joueur = charge_partie(grille, joueur)
    
    
    affiche_grille(grille)
    NB_PV, NB_PP = get_nb_pions(grille)
    
    while (NB_PP > 6) and (NB_PV > 6):
        ancienne_grille = copie_grille(grille)
        
        print(f"C'est au joueur {joueur} de se deplacer. \n")
        nouvelle_grille = tourJoueur(grille, joueur)
        if nouvelle_grille == -1:
            break
        
        joueur = (joueur % 2) + 1
        
        affiche_deux_grilles(ancienne_grille, nouvelle_grille)
        grille = copie_grille(nouvelle_grille)
        print(f"\n\nNombre de pions vide: {NB_PV}, nombre de pions plein: {NB_PP}\n")
    
    
    print(f"\nLa partie est finie, le joueur {(joueur % 2) + 1} a gagné !!")


def jeuOcO(grille):
    global NB_PV, NB_PP
    print("Vous allez observer un jeu entre 2 ordinateurs:\n")
    affiche_grille(grille)
    NB_PV, NB_PP = get_nb_pions(grille)
    joueur = 1
    
    while (NB_PP > 6) and (NB_PV > 6):
        ancienne_grille = copie_grille(grille)
        nouvelle_grille = tourOrdinateur(grille, joueur)
        time.sleep(1)
        joueur = (joueur % 2) + 1
        
        affiche_deux_grilles(ancienne_grille, nouvelle_grille)
        grille = copie_grille(nouvelle_grille)
        print(f"\n\nNombre de pions vide: {NB_PV}, nombre de pions plein: {NB_PP}\n")
    
    
    print(f"\nLa partie est finie, le joueur {(joueur % 2) + 1} a gagné !!")


def jeuJcO(grille):
    global NB_PV, NB_PP
    print("Vous allez jouer contre un ordinateur. Voulez-vous être le premier joueur (entrée ou 2)?: ")
    joueur = str(input(""))
    
    charger_partie = str(input("Voulez-vous charger la derniere partie sauvegardée (o | n)? ")).upper()
    
    if charger_partie == "O":
        grille, joueur = charge_partie(grille, joueur)
    
    
    affiche_grille(grille)
    NB_PV, NB_PP = get_nb_pions(grille)
    
    if joueur == "" or joueur == "1":
        joueur = 1
        jeuJcOJ1(grille)
    else:
        joueur = 2
        jeuJcOJ2(grille)
    
    #preuve intengible que le joueur en question est gagnant
    print(f"\n\nNombre de pions vide: {NB_PV}, nombre de pions plein: {NB_PP}\n")
    print(f"\nLa partie est finie, le joueur {(joueur % 2) + 1} a gagné !!")
 
    
 
def jeuJcOJ1(grille):
    while (NB_PP > 6) and (NB_PV > 6):
        ancienne_grille = copie_grille(grille)
        print("C'est à vous de jouer (J1).\n")
        
        nouvelle_grille = tourJoueur(grille, 1)
        if nouvelle_grille == -1:
            break
        
        print("Voici votre déplacement:\n")
        affiche_deux_grilles(ancienne_grille, nouvelle_grille)
        time.sleep(3)
        
        
        grille = copie_grille(nouvelle_grille)
        
        if (NB_PP > 6) and (NB_PV > 6):
            ancienne_grille = copie_grille(grille)
            nouvelle_grille = tourOrdinateur(grille, 2)
   
        else:
            break
        
        
        print("Le déplacement de l'odinateur\n")
        affiche_deux_grilles(ancienne_grille, nouvelle_grille)
        grille = copie_grille(nouvelle_grille)
       
        
       
def jeuJcOJ2(grille):
    while (NB_PP > 6) and (NB_PV > 6):
        ancienne_grille = copie_grille(grille)
        nouvelle_grille = tourOrdinateur(grille, 2)
        affiche_deux_grilles(ancienne_grille, nouvelle_grille)
        
        grille = copie_grille(nouvelle_grille)
        
        if (NB_PP > 6) and (NB_PV > 6):
            ancienne_grille = copie_grille(grille)
            
            print("C'est à vous de jouer (J1).\n")
            nouvelle_grille = tourJoueur(grille, 1)
            
            if nouvelle_grille == -1:
                break
            
        else:
            break
        
        print("Voici votre déplacement:\n")
        affiche_deux_grilles(ancienne_grille, nouvelle_grille)
        time.sleep(3)
        grille = copie_grille(nouvelle_grille)
    


"""
    Cree un fichier si non existant qui s'appelle sauvegarde_partie sinon écrase sauvegarde
        précédente.
    Dans ce fichier il y a le joueur et la grille entrée en paramètre
"""
def sauvegarde_partie(grille, joueur):
    file = open("sauvegarde_partie.txt", "w")
    file.write(str(joueur) + " " + "\n")
    for x in grille:
        file.write(str(x))
        file.write("\n")
    
    print("Sauvegarde bien effectuée !\n")

"""
    Retourne le grille chargée à partir du fichier sauvegarde_partie et le joueur actuel
"""
def charge_partie(grille, joueur):
    if os.path.exists("sauvegarde_partie.txt"):
        file = open("sauvegarde_partie.txt", "r")
        lecture_fichier = file.readlines()
        new_joueur = int(lecture_fichier[0][0])
        nouvelle_grille = [[], [], [], [], [], [], []]
        
        for i in range(1, len(lecture_fichier)):
            for j in range(len(lecture_fichier[i])):
                caractere = lecture_fichier[i][j]
                if caractere in [PP, PV, CV] and lecture_fichier[i][j-1] != ",":
                    nouvelle_grille[i-1].append(caractere)
        
        return nouvelle_grille, new_joueur
            
    else:
        print("Vous n'avez pas de parties sauvegardées."+
              " Vous jouerez avec la grille séléctionnée précédement.")
        return grille, joueur



def get_nb_pions(grille):
    nb_pp = 0
    nb_pv = 0
    for i in range(7):
        for j in range(7):
            if grille[i][j] == PP:
                nb_pp += 1
            elif grille[i][j] == PV:
                nb_pv += 1
    
    return nb_pv, nb_pp


def test_est_dans_grille():
    print("\nTest de la fonction est_dans_grille...")
    assert not est_dans_grille("X", 32)
    assert est_dans_grille("B", 2)
    assert not est_dans_grille("C", 8)
    assert not est_dans_grille(8, 1)
    assert not est_dans_grille(0, "A")
    assert not est_dans_grille((), ())
    assert est_dans_grille("a", 5)
    print("Ok !")


"""
    Rappel: bon format = LETTRE (maj) + chiffre : U9 est au bon format meme si
        cette case n'est pas dans la grille
"""
def test_est_au_bon_format():
    print("\nTest de la fonction est_au_bon_format...")
    assert not est_au_bon_format("22")
    assert est_au_bon_format("Y2")
    assert not est_au_bon_format(-9999)
    assert not est_au_bon_format("3U")
    assert not est_au_bon_format("DC")
    assert not est_au_bon_format(())
    assert est_au_bon_format("z9")
    print("Ok !")



def test_est_mouvement_valide():
    grille = grille_milieu
    depart = "F4"
    direction = 2
    joueur = 1
    print("\nTest de la fonction test_est_mouvement_valide...")
    assert not est_mouvement_valide(grille, joueur, SIMPLE, direction, depart)
    assert not est_mouvement_valide(grille, joueur, SAUT, direction, depart)
    assert est_mouvement_valide(grille, joueur, SAUT, direction, "G2")
    assert not est_mouvement_valide(grille, 2, SAUT, 0, "c4")
    assert est_mouvement_valide(grille, 2, SIMPLE, 3, "c4")
    assert not est_mouvement_valide(grille, 2, SAUT, 0, "A3")
    assert not est_mouvement_valide(grille, joueur, SIMPLE, 3, "g2")
    print("Ok !")


def test_possibilite_sauts():
    grille = grille_milieu
    joueur = 1
    print("\nTest de la fonction test_possibilite_sauts...")
    assert possibilite_sauts(grille, joueur, "c5") == 5
    assert possibilite_sauts(grille, joueur, "g3") == -1
    assert possibilite_sauts(grille, joueur, "g2") == 2
    assert possibilite_sauts(grille, 2, "f2") == -1
    print("Ok !")

    
def test_possibilite_simple():
    grille = grille_milieu
    joueur = 1
    print("\nTest de la fonction test_possibilite_simple...")
    assert possibilite_simple(grille, joueur, "g2") == 1
    assert possibilite_simple(grille, joueur, "g3") == 5
    assert possibilite_simple(grille, 2, "a2") == -1
    print("Ok !")


def test_mouvement_uniq():
    grille = grille_milieu
    joueur = 1
    print("\nTest de la fonction test_mouvement_uniq...")
    assert mouvement_possible(grille, 2, "a2") == -1
    assert mouvement_possible(grille, joueur, "g3") == 1
    assert mouvement_possible(grille, joueur, "c5") == 2
    assert mouvement_possible(grille, joueur, "g2") == 3
    print("Ok !")


def fnct_generale_de_tests():
    test_est_mouvement_valide()
    test_possibilite_sauts()
    test_possibilite_simple()
    test_mouvement_uniq()
    test_est_au_bon_format()
    test_est_dans_grille()
    

# 
if __name__ == "__main__":
    print("\nRappel des règles: lorsqu'un joueur a moins de 6 pions, il perd. Les deplacements ne" + 
          " se font qu'orthogonalement. Il y a 2 deplacements possibles, le mouvement simple " + 
          "qui permet de deplacer un pion de 1 case (case vide); il y a aussi le mouvement saut qui permet " +
          "de faire un deplacement de 2 cases et de manger un pion ennemi par la même occasion." +
          " lorsque d'autres sauts sont possibles, le joueur peut les enchainer en un seul tour.\n")
    print("\n Vous pourrez à chaque saisie de pions choisir de sauvegarder la partie avec le" +
          " mot clé: \"save\". Vous écraserez la sauvegarde précédente. Vous pourrez également"
          + " abandonner avec le mot clé \"abandonner\".\n")
    
    print("\nVoulez-vous faire une partie joueur contre joueur (1)" +
          " ou plûtot contre ordinateur (2) (avec 3 vous pourrez voir"+
          " une partie ordi contre ordi?")
    
    JoueurContreOrdiOUJoueur = str(input(""))
    while JoueurContreOrdiOUJoueur not in ["1", "2", "3"]:
        JoueurContreOrdiOUJoueur = str(input("Veuillez taper 1 ou 2 svp: "))
    
    print("Si vous n'entrez rien (mauvaise saisie ou juste entrée), le grille est celle de départ.")
    saisie_grille = str(input("Sur quelle grille souhaitez-vous jouer (milieu(2) | fin(3))? "))
    grille = grille_depart
    
    if saisie_grille == "milieu" or saisie_grille == 2:
        grille = grille_milieu
    elif saisie_grille == "fin" or saisie_grille == 3:
        grille = grille_fin
    else:
        print("La grille de départ a été choisi.\n")
    
    if JoueurContreOrdiOUJoueur == "1":
        jeuJcJ(grille)
    
    elif JoueurContreOrdiOUJoueur == "2":
        jeuJcO(grille)
    
    elif JoueurContreOrdiOUJoueur == "3":
        jeuOcO(grille)


    
