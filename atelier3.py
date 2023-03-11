# -*- coding: utf-8 -*- 

PV : str = '○' # Pion Vide
PP : str = '☻' # Pion Plein
CV : str = '' # Case Vide

NB_PV = 24 # nombre de pion blancs
NB_PP = 24 # nombre de pions noirs

JOUEUR = {1: PV, 2 : PP} # repartition des pions selon les 2 joueurs

SIMPLE = "simple"
SAUT = "saut"
ENCHAINEMENT = "enchainement"


grille_depart = [[PP, PP, PP, PP, PP, PP, PV],
                 [PP, PP, PP, PP, PP, PV, PV], 
                 [PP, PP, PP, PP, PV, PV, PV], 
                 [PP, PP, PP, CV, PV, PV, PV],
                 [PP, PP, PP, PV, PV, PV, PV],
                 [PP, PP, PV, PV, PV, PV, PV],
                 [PP, PV, PV, PV, PV, PV, PV]]


grille_milieu = [[PP, CV, PP, CV, CV, CV, CV],
                 [CV, PP, CV, CV, PP, PV, PV], 
                 [CV, CV, CV, PP, PV, PV, CV], 
                 [CV, PP, CV, CV, PV, PV, CV],
                 [CV, CV, CV, PV, PV, PV, CV],
                 [PP, PP, CV, PV, CV, CV, CV],
                 [CV, PV, PV, CV, CV, CV, CV]]

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
    if len(str(ligne)) != 1 or len(str(colonne)) != 1:
        return False
    
    return (ord('A') <= ord(str(ligne).upper()) <= ord('G') and \
            ord('1') <= ord(str(colonne)) <= ord('7'))


"""
    Fonction ayant pour but de vérifier le bon formatage de l'utilisateur lorsqu'il entre
        des informations.
"""
def est_au_bon_format(coord : str) -> bool: #compare le code Ascii et retourne un booleen
    coord = str(coord)
    if len(str(coord)) != 2:
        return False
        
    return (ord('A') <= ord(str(coord[0]).upper()) <= ord('Z')) and \
        (48 <= ord(str(coord[1])) <= 57)



"""
    Fonction demandant à l'utilisateur de saisir des coordonnées. Il va sans dire qu'elles
        appartiendront à la grille -nous utiliserons les fonctions précédentes-.
        
        
    Modifications sur cette fonction: ajout de 2 parametres: grille et joueur pour etre
        sur que le joueur a saisie une coordonnée d'un de ses pions.
"""
def saisir_coord(grille, joueur) -> str:
    coord = str(input("Entrez une coordonnée d'un de vos pions (entre A1 et G7): "))
    while not (est_au_bon_format(coord) and est_dans_grille(coord[0], coord[1])):
        coord = str(input("Entrez une coordonnée d'un de vos pions (entre A1 et G7): "))
    
    while case(grille, coord) != JOUEUR.get(joueur):
        print("Etes vous sur de jouer le bon pion ? ")
        coord = str(input("Entrez une coordonnée d'un de vos pions (entre A1 et G7): "))
    
    coord = coord[0].upper() + coord[1] # au cas ou l'utilisateur aurait entré 
                                            #une lettre minuscule
    
    return coord


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
    Plan: demande le mouvement que le joueur veut effectuer (voir mouvement l.170).
        Cette fonction demande une case de départ et une direction selon s'il s'agit
        d'un mouvement simple ou un saut, autrement, il s'agit d'un enchainement.
    La fonction appellera les fonctions idoines. Les fonctions en question effectueront
    le mouvement demandé. Un affichage après chaque coup (tour / coup) se fera.
                                                        ##############
"""


"""
    Fonction affichant 2 grilles l'une a cote de l'autre. Utile pour un "avant / apres"
"""
def affiche_deux_grilles(grille1, grille2):
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


"""
    Retourne la direction d'un pion s'il est seul autour d'une case, sinon retourne -1
            Cette fonction est unique au mouvement saut
"""
def get_pions_autour_pour_saut(grille, joueur, depart) -> int:
    pions_autour = []
    for i in range(4):
        case_pion_orthogonaux = arrivee_simple(grille, joueur, depart, i)
        case_arrivee_orthogonaux = arrivee_saut(grille, joueur, depart, i)
        
        if est_dans_grille(case_pion_orthogonaux[0], case_pion_orthogonaux[1]) \
            and est_dans_grille(case_arrivee_orthogonaux[0], case_arrivee_orthogonaux[1]) \
                and case(grille, case_arrivee_orthogonaux) == CV:
                
            if joueur == 1 and case(grille, case_pion_orthogonaux) == PP:
                pions_autour.append(i)
            elif joueur == 2 and case_pion_orthogonaux == PV:
                pions_autour.append(i)
    
    if len(pions_autour) == 1:
        return pions_autour[0]
    
    return -1


"""
    Permet qu'a partir d'une case, effectuer le mouvement demandé s'il n'y a 
            qu'une possibilité. Par exemple, au debut, le mouvement simple sera effectuer
            tout seul. L'utilisateur saisira e4 par exemple, et le programme effectura
            le seul mouvement possible, d4.
"""


"""
    Retourne la direction de la seule case vide autour, sinon retourne -1
            Cette fonction est unique au mouvement simple
"""
def get_direction_cv_mouv_simple(grille, joueur, depart) -> int:
    case_vide_autour = []
    for i in range(4):
        case_autour = arrivee_simple(grille, joueur, depart, i)
        if est_dans_grille(case_autour[0], case_autour[1]):
            if case(grille, case_autour) == CV:
                case_vide_autour.append(i)
    
    if len(case_vide_autour) == 1:
        return case_vide_autour[0]
    
    return -1




"""
    Retourne le pion sur la case dont les coordonnées correspondent.
        (Dans la grille actuelle)
    Retourne constante PP, PV ou CV
"""
def case(grille, coord) -> str:
    return (grille[ord(coord[0].upper()) - 65][ord(coord[1]) - 49])




"""
    Permet la saisie d'une direction et retourne un nombre entre 0 et 3 selon la direction
    0 pour droite; 1 pour gauche; 2 pour haut; 3 pour bas.
    
    La saisie d'une direction plutot que d'une case d'arrivee permet d'eviter les erreurs.
                La case d'arrivee sera calculee dans une fonction idoine
"""
def saisir_direction() -> int:
    direction = str(input("Ouest | g, est | d, nord | h, sud | b : ")).lower()
    differente_possibilite_dEntree = ["est", "e", "droite", "d",
                                      "ouest", "o", "gauche", "g",
                                      "nord", "n", "haut", "h",
                                      "sud", "s", "bas", "b"]
    
    while (direction not in differente_possibilite_dEntree):
        direction = str(input("Etes vous sur de ne pas avoir fait d'erreur de frappe? : "))\
            .lower()
    
    return differente_possibilite_dEntree.index(direction) // 4


"""
    Demande la saisie d'un mouvement appelle le mouvement en question.
        Retourne False si quelque chose n'a pas marché (fautes de frappe non comprises)
    
    Retourne la nouvelle grille; a afficher avec affiche_grille # TODO
"""


def mouvement(grille, joueur) -> list:
    print(f"C'est au joueur {joueur} de se deplacer. \n")
    mouv = str(input("Quel mouvement souhaitez-vous faire ? (simple (s)," +
                     " saut (h), enchainement (e): "))
    mouv = mouv.lower()
    different_mouvement = [SIMPLE, "s", SAUT, "h", ENCHAINEMENT, "e"]
    while (mouv not in different_mouvement):
        mouv = str(input("Il y a une faute de frappe, veuillez retaper svp: "))
 
    if mouv == "s":
        mouv = SIMPLE
    elif mouv == "h":
        mouv = SAUT
    else:
        mouv = ENCHAINEMENT
    
    print("Quelle est votre case de départ ? ")
    depart = saisir_coord(grille, joueur)
    
    return appel_mouvement(grille, joueur, depart, mouv)



def changer_deplacement(grille, joueur):
    changer_mouvement = str(input("Voulez-vous faire un autre deplacement(o | n): "))
    if changer_mouvement == "n":
        return False
    
    return True


"""
    Decomposition de la fonction ci-dessus avec la fonction ci-apres.
        Retourne la grille apres le mouvement demandé
"""
def appel_mouvement(grille, joueur, depart, mouv) -> list:
    grille_apres_deplacement = grille
    
    if mouv == SIMPLE:
        direction_unique = get_direction_cv_mouv_simple(grille, joueur, depart)
        if direction_unique != -1:
            print("\nLe mouvement simple s'effectue tout seul car possibilité unique.")
            mouvement_simple(grille, joueur, depart, direction_unique)
            
        else:
            print("Quelle direction souhaitez vous prendre ?") # direction non demandée avant
            direction = saisir_direction()                # car non necessaire dans enchainement
            grille_apres_deplacement = mouvement_simple(grille, joueur, depart, direction)
        
    elif mouv == SAUT:
        direction_unique = get_pions_autour_pour_saut(grille, joueur, depart)
        if direction_unique != -1:
            print("\nLe mouvement saut s'effectue tout seul car possibilité unique.")
            mouvement_saut(grille, joueur, depart, direction_unique)
            
        else:
            print("Quelle direction souhaitez vous prendre ?")
            direction = saisir_direction()
            grille_apres_deplacement = mouvement_saut(grille, joueur, depart, direction)
        
    elif mouv == ENCHAINEMENT:
        grille_apres_deplacement = mouvement_enchainement(grille, joueur, depart)
        
    return grille_apres_deplacement



"""
    Si case pas vide, mouvement simple et saut font appel a cette fonction.
"""
def changer_saisie_car_erreur(grille, joueur, mouvement):
    depart = saisir_coord(grille, joueur)
    direction = saisir_direction()
    if mouvement == SIMPLE:
        mouvement_simple(grille, joueur, depart, direction)
    
    elif mouvement == SAUT:
        mouvement_saut(grille, joueur, depart, direction)



"""
    Retourne une case d'arrivee selon une case de depart et une direction
        Cette fonction est unique aux mouvements simples.
        
    Si la case d'arrivee est en dehors de la grille, fait appel a changement de deplacement
    ci-dessus.
"""
def arrivee_simple(grille, joueur, depart, direction) -> str:
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
    Effectue un deplacement simple. Si la case est vide appel changement deplacement 
            2 fonctions au dessus
    Remplace la case de depart par une case vide et la case d'arrivee par le pion du joueur
    
    Retourne une grille
"""
def mouvement_simple(grille, joueur, depart, direction) -> list:
    arrivee = arrivee_simple(grille, joueur, depart, direction)
    cd = False
    
    if not(est_dans_grille(arrivee[0], arrivee[1])):
        print("La case d'arrivee est en dehors de la grille, veuillez resaisir la case " + 
              "de depart ainsi que la direction.")
        cd = changer_deplacement(grille, joueur)
        if cd:
            mouvement(grille, joueur)
        
        else:
            changer_saisie_car_erreur(grille, joueur, SIMPLE)
    
    else:
        while case(grille, arrivee) != CV: # case non vide
            print("La case d'arrivee n'est pas vide, veuillez revoir votre deplacement.\n")
            cd = changer_deplacement(grille, joueur)
            if cd:
                mouvement(grille, joueur)
                
            else:
                changer_saisie_car_erreur(grille, joueur, SIMPLE)
        
        if not cd:
            grille[ord(arrivee[0]) - 65][ord(arrivee[1]) - 49] = JOUEUR.get(joueur) # change la 
                                                # valeur de la case d'arrivee en le pion du joueur
            grille[ord(depart[0]) - 65][ord(depart[1]) - 49] = CV # remplace case depart par case vide
            print(f"\nLe mouvement vers {arrivee} a été joué.")
            
            return grille
    
    return grille
    

"""  
    Retourne la case d'arrivee apres le saut dans la direction demandee.
"""
def arrivee_saut(grille, joueur, depart, direction) -> str:
    arrivee = depart
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
    Fonction permettant de savoir s'il y a des problemes de cases; case non vide a l'arrivee
        ou case occupee par autre chose qu'un pion de la couleur opposée (vide ou pion allié)
"""
def soucis_case_saut(grille, joueur, depart, direction, arrivee) -> bool:
    # S'il n'y a pas de pion de la couleur opposé entre case de depart et d'arrivee
    
    case_entre_depart_et_arrivee = case(grille, \
                                        arrivee_simple(grille, joueur, depart, direction))
    cd = False
    
    # si la case d'arrivee est en dehors de la grille
    if not(est_dans_grille(arrivee[0], arrivee[1])) and not cd:
        print("La case d'arrivee est en dehors de la grille, veuillez resaisir la case " + 
                 "de depart ainsi que la direction.")
        cd = changer_deplacement(grille, joueur)
        if cd:
            mouvement(grille, joueur)
        
        else:
            changer_saisie_car_erreur(grille, joueur, SAUT)    
    else:
        # si le joueur cherche a deplacer autre chose que son propre pion

        cd = est_pion_au_joueur(grille, joueur, case_entre_depart_et_arrivee)
    
        # Si la case d'arrivee n'est pas vide
        while (case(grille, arrivee) != CV):
            print(f"La case {arrivee} n'est pas vide, veuillez re-saisir les coordonnées: ")
            cd = changer_deplacement(grille, joueur)
            if cd:
                mouvement(grille, joueur)
            else:
                changer_saisie_car_erreur(grille, joueur, SAUT)
    
    return cd


# si le joueur cherche a deplacer autre chose que son propre pion
def est_pion_au_joueur(grille, joueur, case_coord):
    cd = False
    
    # Si c'est le tour du joueur 1 et qu'il veuillez deplacer autre chose que son pion
    if joueur == 1:
        while (case_coord != PP) and not cd:
            print("Il n'y a pas de pion plein entre votre case de depart et d'arrivee." + 
                  " Veuillez re-saisir les coordonnées svp (ou choisir un autre deplacement): ")
            cd = changer_deplacement(grille, joueur)
            if cd:
                mouvement(grille, joueur)
            
            else:
                changer_saisie_car_erreur(grille, joueur, SAUT)
    
    # Si c'est le tour du joueur 2 et qu'il veuillez deplacer autre chose que son pion
    elif joueur == 2:
        while (case_coord != PV) and not cd:
            print("Il n'y a pas de pion vide entre votre case de depart et d'arrivee." + 
                  " Veuillez re-saisir les coordonnées svp: ")
            cd = changer_deplacement(grille, joueur)
            if cd:
                mouvement(grille, joueur)
            
            else:
                changer_saisie_car_erreur(grille, joueur, SAUT)
    
    return cd


def get_opposant(joueur):
    if joueur == 1:
        return 2 # le joueur 2 est l'opposant du 1
    return 1


def decroit_nb_pion(joueur):
    global NB_PV, NB_PP
    
    if joueur == 1:
        NB_PV -= 1
        return NB_PV
    else:
        NB_PP -= 1
        return NB_PP



"""
    Les fonctions s'appellent entre elles: fonction mouvement appelle fonction mouvement saut
        saut appelle soucis pour et entre dans des boucles while tant qu'il y a un PV de cases
    
    soucis appelle la fonction de changement de deplacement qui elle meme appelle la fonction
    saut. Et ainsi de suite tant qu'il y a un soucis de cases.
"""
def mouvement_saut(grille, joueur, depart, direction) -> list:
    arrivee = arrivee_saut(grille, joueur, depart, direction)
    if not soucis_case_saut(grille, joueur, depart, direction, arrivee):
        
        case_entre_depart_et_arrivee = arrivee_simple(grille, joueur, depart, direction)
        
        grille[ord(depart[0]) - 65][ord(depart[1]) - 49] = CV # case depart maintenant vide
        grille[ord(case_entre_depart_et_arrivee[0]) - 65]\
            [ord(case_entre_depart_et_arrivee[1]) - 49] = CV # case entre les 2 maintenant vide
        grille[ord(arrivee[0]) - 65][ord(arrivee[1]) - 49] = JOUEUR.get(joueur)
            # case d'arrivee maintenant egal au pion du joueur.
        
        opposant = get_opposant(joueur)
        
        nb_pion = decroit_nb_pion(opposant)
        print(f"\nLe mouvement vers {arrivee} a été joué. Il reste {nb_pion} pion" +
              "au joueur {opposant}")
        
        return grille, arrivee # S'il y a eu un changement 

    return grille, arrivee # grille en parametre, sans changement


def mouvement_enchainement(grille, joueur, depart, arrivee):
    nb_enchainement = int(input("Combien de saut allez vous effectuer ?: "))
    cd = False
    grille_apres_deplacement = grille
    
    if nb_enchainement < 1:
        certitude = str(input\
        ("Le nombre entré ne convient pas, voulez-vous vraiment faire un enchainement (o | n)? "))
        
        if certitude == "o":
            while nb_enchainement < 1:
                nb_enchainement = int(input("Veuillez entrer le nombre de saut que vous voulez" + 
                                        " réellement faire: "))
        else:
            cd = changer_deplacement(grille, joueur)
            mouvement(grille, joueur)
    
    
    if not cd:
        #arrivee = arrivee_saut(grille, joueur, depart, direction) ### TROUVER L ARRIVEE
        grille_apres_deplacement = appel_mouvement(grille, joueur, depart, SAUT)
        
        for i in range(nb_enchainement):
            appel_mouvement(grille, joueur, depart, SAUT)
            

    return grille_apres_deplacement




def test_case_valide():
    assert case(grille_depart, "B3") == PP
    assert case(grille_fin, "a3") == CV



def test_valide_case_autour_Msimple():
    assert get_direction_cv_mouv_simple(grille_depart, 1, "e4") == 2
    assert get_direction_cv_mouv_simple(grille_depart, 1, "f6") == -1
    assert get_direction_cv_mouv_simple(grille_depart, 1, "G7") == -1
    assert get_direction_cv_mouv_simple(grille_depart, 1, "G3") == 0


def test_valide_case_autour_Msaut():
    assert get_pions_autour_pour_saut(grille_milieu, 1, "G2") == 2
    assert get_pions_autour_pour_saut(grille_milieu, 1, "G3") == -1
    assert get_pions_autour_pour_saut(grille_milieu, 2, "F1") == -1
    assert get_pions_autour_pour_saut(grille_milieu, 2, "F2") == -1
    assert get_pions_autour_pour_saut(grille_milieu, 1, "a3") == -1




if __name__ == "__main__":
#    test_case_valide()
#    mouvement(grille_depart, 1)
    # depart = saisir_coord()
    # direction = saisir_direction()
    # print(mouvement_simple(grille_depart, 1, depart, direction))
    #mouvement(grille_depart, 1)
    affiche_grille(grille_milieu)
    # test_valide_case_autour_Msimple()
    # test_valide_case_autour_Msaut()
    affiche_grille(mouvement(grille_milieu, 1))
    # grille_courante = grille_depart
    # affiche_deux_grilles(grille_depart, mouvement(grille_courante, 1))
    # affiche_grille(grille_courante)
    # affiche_grille(mouvement(grille_courante, 2))


"""
      a faire: permettre de changer de mouvement
"""  
    
# verifier que les lignes correspondent au "a voir"