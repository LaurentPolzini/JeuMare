# -*- coding: utf-8 -*- 

from atelier2.py import *


def deplacement():
    deplacement = str(input("Quel déplacement voulez-vous faire (simple, saut, enchainement): "))
    print("Veuillez saisir vos coordonnées:\n")
    saisir_coord()
    
    return deplacement


if __name__ == "__main__":
    deplacement()