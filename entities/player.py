"""
Třída hráče pro Arena Survival.

Zpracovává pohyb pomocí klávesnice (WASD) a střelbu směrem k myši.
"""

import pygame
from entities.entity import Entity
from entities.bullet import Bullet
from settings import PLAYER_SPEED, WIDTH, HEIGHT

class Player(Entity):
    """
    Herní postava ovládaná hráčem.
    
    Ovládání:
        W/A/S/D - Pohyb
        Myš - Zaměřování
        Klik myši - Střelba
    """

    def __init__(self, game, pos):
        """
        Inicializuje hráče.
        
        Args:
            game: Reference na Game objekt
            pos: Tuple (x, y) - počáteční pozice
        """
        # Modrý čtverec 40x40 pixelů
        super().__init__(game, pos, (40, 40), (50, 200, 255))
        self.image = pygame.image.load("assets/robot.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))

    def update(self, dt):
        """
        Aktualizuje pozici hráče na základě klávesových vstupů.
        
        Args:
            dt: Delta time v sekundách
            
        Zajišťuje:
        - Plynulý pohyb ve všech směrech
        - Normalizaci diagonálního pohybu
        - Omezení pohybu uvnitř herní plochy
        """
        # Získání stavu klávesnice
        keys = pygame.key.get_pressed()
        # Inicializace rychlosti na nulu
        vel = pygame.Vector2(0, 0)

        # Vstup pohybu (WASD)
        if keys[pygame.K_w]: vel.y = -1  # Nahoru
        if keys[pygame.K_s]: vel.y = 1   # Dolů
        if keys[pygame.K_a]: vel.x = -1  # Doleva
        if keys[pygame.K_d]: vel.x = 1   # Doprava

        # Normalizace rychlosti, aby diagonální pohyb nebyl rychlejší
        if vel.length() > 0:
            vel = vel.normalize()

        # Aplikace rychlosti na pozici
        self.pos += vel * dt * PLAYER_SPEED
        
        # Omezení pohybu uvnitř herní plochy
        half_width = self.rect.width / 2
        half_height = self.rect.height / 2
        
        # Clamp pozice, aby hráč nemohl opustit obrazovku
        self.pos.x = max(half_width, min(self.pos.x, WIDTH - half_width))
        self.pos.y = max(half_height, min(self.pos.y, HEIGHT - half_height))
        
        # Aktualizace rect pro kolize
        self.rect.center = self.pos

    def shoot(self):
        """
        Vystřelí projektil směrem k pozici myši.
        
        Vytvoří nový Bullet objekt a přidá ho do příslušných sprite skupin.
        """
        # Získání pozice myši
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        
        # Výpočet směru od hráče k myši
        direction = mouse_pos - self.pos

        # Normalizace směru (jednotkový vektor)
        if direction.length() > 0:
            direction = direction.normalize()

        # Vytvoření a přidání projektilu do hry
        bullet = Bullet(self.game, self.pos, direction)
        self.game.bullets.add(bullet)
        self.game.all_sprites.add(bullet)
