"""
Systém pro spawování (generování) nepřátel.

Pravidelně vytváří nové nepřátele na náhodných pozicích
na okrajích herní obrazovky.
"""

import random
from entities.enemy import Enemy
from settings import SPAWN_INTERVAL, WIDTH, HEIGHT

class Spawner:
    """
    Systém pro automatické generování nepřátel.
    
    V pravidelných intervalech vytváří nové nepřátele na náhodných
    pozicích na okrajích obrazovky (top, bottom, left, right).
    
    Attributes:
        game: Reference na Game objekt
        timer: float - odpočet do příštího spawnu
    """

    def __init__(self, game):
        """
        Inicializuje spawner.
        
        Args:
            game: Reference na Game objekt
        """
        self.game = game
        self.timer = 0  # Časovač pro spawn interval

    def update(self, dt):
        """
        Aktualizuje časovač a spawnuje nepřátele.
        
        Args:
            dt: Delta time v sekundách
            
        Každých SPAWN_INTERVAL sekund vytvoří nového nepřítele.
        """
        self.timer += dt
        
        # Pokud uplynul spawn interval, vytvořit nepřítele
        if self.timer >= SPAWN_INTERVAL:
            self.timer = 0  # Reset časovače
            self.spawn_enemy()

    def spawn_enemy(self):
        """
        Vytvoří nového nepřítele na náhodné pozici na okraji obrazovky.
        
        Náhodně vybere jednu ze čtyř stran obrazovky a umístí
        nepřítele na náhodnou pozici na této straně.
        """
        # Náhodný výběr strany obrazovky
        side = random.choice(["top", "bottom", "left", "right"])

        # Určení pozice podle vybrané strany
        if side == "top":
            # Horní okraj - náhodná X pozice, Y = 0
            pos = (random.randint(0, WIDTH), 0)
        elif side == "bottom":
            # Dolní okraj - náhodná X pozice, Y = výška obrazovky
            pos = (random.randint(0, WIDTH), HEIGHT)
        elif side == "left":
            # Levý okraj - X = 0, náhodná Y pozice
            pos = (0, random.randint(0, HEIGHT))
        else:  # right
            # Pravý okraj - X = šířka obrazovky, náhodná Y pozice
            pos = (WIDTH, random.randint(0, HEIGHT))

        # Vytvoření nepřítele a přidání do sprite skupin
        enemy = Enemy(self.game, pos, size=self.game.get_enemy_size())
        self.game.enemies.add(enemy)
        self.game.all_sprites.add(enemy)
