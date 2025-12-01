"""
Třída projektilu pro Arena Survival.

Projektily se pohybují konstantní rychlostí daným směrem
a po určité době automaticky zmizí.
"""

import pygame
from entities.entity import Entity
from settings import BULLET_SPEED, BULLET_LIFETIME

class Bullet(Entity):
    """
    Projektil vystřelený hráčem.
    
    Pohybuje se přímočaře daným směrem a po vypršení doby života
    se automaticky odstraní.
    
    Attributes:
        direction: pygame.Vector2 - normalizovaný směrový vektor
        timer: float - čas existence v sekundách
    """

    def __init__(self, game, pos, direction):
        """
        Inicializuje projektil.
        
        Args:
            game: Reference na Game objekt
            pos: Tuple/Vector2 (x, y) - počáteční pozice (pozice hráče)
            direction: pygame.Vector2 - směr letu (normalizovaný vektor)
        """
        # Žlutý čtverec 10x10 pixelů
        super().__init__(game, pos, (10, 10), (255, 255, 0))
        self.direction = direction
        self.timer = 0  # Odpočet života projektilu

    def update(self, dt):
        """
        Aktualizuje pozici a životnost projektilu.
        
        Args:
            dt: Delta time v sekundách
            
        Projektil se pohybuje konstantní rychlostí daným směrem.
        Po vypršení BULLET_LIFETIME se sám odstraní.
        """
        # Pohyb v daném směru
        self.pos += self.direction * BULLET_SPEED * dt
        self.rect.center = self.pos

        # Odpočet životnosti
        self.timer += dt
        if self.timer >= BULLET_LIFETIME:
            
            self.kill()  # Odstranění ze všech sprite skupin
