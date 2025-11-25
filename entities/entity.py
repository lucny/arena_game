"""
Bázová třída pro všechny herní entity.

Poskytuje společnou funkcionalitu pro všechny herní objekty
(hráč, nepřátelé, projektily).
"""

import pygame

class Entity(pygame.sprite.Sprite):
    """
    Rodičovská třída pro všechny herní objekty.
    
    Dědí z pygame.sprite.Sprite pro podporu sprite skupin a kolizí.
    
    Attributes:
        game: Reference na hlavní herní objekt
        image: Pygame Surface - vizuální reprezentace entity
        pos: pygame.Vector2 - přesná pozice entity
        rect: pygame.Rect - obdélník pro kolize a vykreslování
    """

    def __init__(self, game, pos, size, color):
        """
        Inicializuje entitu.
        
        Args:
            game: Reference na Game objekt
            pos: Tuple (x, y) - počáteční pozice
            size: Tuple (width, height) - rozměry entity
            color: Tuple (r, g, b) - barva entity
        """
        super().__init__()
        self.game = game

        # Vytvoření obrázku (surface) s danou barvou
        self.image = pygame.Surface(size)
        self.image.fill(color)

        # Pozice a rect pro kolize
        self.pos = pygame.Vector2(pos)  # Přesná pozice s desetinnými čísly
        self.rect = self.image.get_rect(center=pos)  # Obdélník pro kolize

    def update(self, dt):
        """
        Aktualizuje stav entity.
        
        Args:
            dt: Delta time v sekundách
            
        Potomci přepíší tuto metodu vlastní logikou.
        """
        pass
