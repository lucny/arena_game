"""
Třída nepřítele pro Arena Survival.

Nepřátelé se neustále pohybují směrem k hráči.
"""

import pygame
from entities.entity import Entity
from settings import ENEMY_SPEED

class Enemy(Entity):
    """
    Nepřátelská entita, která pronásleduje hráče.
    
    Automaticky se pohybuje směrem k pozici hráče konstantní rychlostí.
    Při kontaktu s hráčem způsobí game over.
    """

    def __init__(self, game, pos, size=(30, 30)):
        """
        Inicializuje nepřítele.
        
        Args:
            game: Reference na Game objekt
            pos: Tuple (x, y) - počáteční pozice (obvykle na okraji obrazovky)
            size: Tuple (width, height) - velikost nepřítele (pro obtížnost)
        """
        # Červený čtverec - velikost dle obtížnosti
        super().__init__(game, pos, size, (255, 60, 60))

    def update(self, dt):
        """
        Aktualizuje pozici nepřítele - pohyb směrem k hráči.
        
        Args:
            dt: Delta time v sekundách
            
        Vypočítá směr k hráči, normalizuje ho a aplikuje rychlost.
        """
        # Výpočet směru k hráči
        direction = (self.game.player.pos - self.pos)
        
        # Normalizace směru (jednotkový vektor)
        if direction.length() > 0:
           direction = direction.normalize()

        # Pohyb směrem k hráči
        self.pos += direction * ENEMY_SPEED * dt
        self.rect.center = self.pos
