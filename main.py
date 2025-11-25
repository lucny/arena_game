"""
Hlavní vstupní bod aplikace Arena Survival.

Tento skript inicializuje pygame, spouští herní smyčku a po ukončení
hry provádí úklid pygame.
"""

import pygame
from game import Game

if __name__ == "__main__":
    # Inicializace všech pygame modulů
    pygame.init()
    
    # Vytvoření instance hry a spuštění hlavní herní smyčky
    Game().run()
    
    # Ukončení pygame a uvolnění zdrojů
    pygame.quit()
