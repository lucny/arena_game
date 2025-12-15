"""
Hlavní herní třída pro Arena Survival.

Spravuje herní smyčku, sprite skupiny, kolize a vykreslování.
"""

import pygame
from settings import WIDTH, HEIGHT, FPS
from entities.player import Player
from systems.spawner import Spawner

class Game:
    """
    Hlavní třída hry, která orchestruje všechny herní systémy.
    
    Attributes:
        screen: Pygame surface pro vykreslování
        clock: Pygame Clock pro kontrolu FPS
        all_sprites: Skupina všech viditelných sprite objektů
        enemies: Skupina nepřátelských entit
        bullets: Skupina projektilů
        player: Instance hráče
        spawner: Systém pro generování nepřátel
        running: Flag pro běh herní smyčky
        score: Aktuální skóre hráče
    """

    def __init__(self):
        """Inicializuje hru, vytváří okno a herní objekty."""
        # Vytvoření herního okna
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Arena Survival – OOP Version")
        self.clock = pygame.time.Clock()

        # Sprite skupiny pro správu kolizí a vykreslování
        self.all_sprites = pygame.sprite.Group()  # Všechny viditelné objekty
        self.enemies = pygame.sprite.Group()       # Pouze nepřátelé
        self.bullets = pygame.sprite.Group()       # Pouze projektily

        # Vytvoření hráče ve středu obrazovky
        self.player = Player(self, (WIDTH // 2, HEIGHT // 2))
        self.all_sprites.add(self.player)

        # Inicializace systému pro spawn nepřátel
        self.spawner = Spawner(self)

        # Herní stav
        self.running = True
        self.score = 0
        self.shoots = 0

    # ------------------------------------------------------------------
    def run(self):
        """
        Hlavní herní smyčka.
        
        Běží, dokud je self.running True. Každý snímek:
        1. Omezuje FPS a vypočítá delta time
        2. Zpracovává vstupy
        3. Aktualizuje herní stav
        4. Vykresluje scénu
        """
        while self.running:
            # Delta time v sekundách - čas od posledního snímku
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()

    # ------------------------------------------------------------------
    def handle_events(self):
        """
        Zpracovává uživatelské vstupy a pygame eventy.
        
        Kontroluje:
        - QUIT event pro ukončení hry
        - Kliknutí myši pro střelbu
        """
        for event in pygame.event.get():
            # Zavření okna
            if event.type == pygame.QUIT:
                self.running = False

            # Střelba na kliknutí myši
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.shoot()

    # ------------------------------------------------------------------
    def update(self, dt):
        """
        Aktualizuje herní logiku.
        
        Args:
            dt: Delta time v sekundách od posledního snímku
            
        Provádí:
        - Update všech sprite objektů
        - Update spawn systému
        - Detekci a zpracování kolizí
        """
        # Aktualizace všech entit
        self.all_sprites.update(dt)
        self.spawner.update(dt)

        # Detekce kolizí projektilů s nepřáteli
        for bullet in self.bullets:
            hits = pygame.sprite.spritecollide(bullet, self.enemies, True)
            if hits:
                bullet.kill()  # Zničení projektilu
                self.score += len(hits)  # Přičtení bodů za každého zabitého nepřítele

        # Detekce kolize nepřátel s hráčem (game over)
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.running = False

    # ------------------------------------------------------------------
    def draw(self):
        """
        Vykresluje všechny herní objekty na obrazovku.
        
        Postup:
        1. Vyplní pozadí tmavou barvou
        2. Vykreslí všechny sprite objekty
        3. Vykreslí HUD (skóre)
        4. Aktualizuje display
        """
        # Vyplnění pozadí tmavě šedou barvou
        self.screen.fill((30, 30, 30))
        
        # Vykreslení všech sprite objektů
        self.all_sprites.draw(self.screen)

        # Vykreslení uživatelského rozhraní
        self.draw_hud()

        # Aktualizace obrazovky
        pygame.display.flip()

    # ------------------------------------------------------------------
    def draw_hud(self):
        """
        Vykresluje HUD (Head-Up Display) - informace na obrazovce.
        
        Zobrazuje aktuální skóre v levém horním rohu.
        """
        font = pygame.font.SysFont(None, 36)
        score = font.render(f"Score: {self.score}", True, (255,255,255))
        time = font.render(f"Time: {int(pygame.time.get_ticks() / 1000)}", True, (255,255,255))
        shoots = font.render(f"Shoots: {self.shoots}", True, (255,255,255))
        accuracy = font.render(f"Accuracy: {int((self.score / self.shoots * 100) if self.shoots > 0 else 0)}%", True, (255,255,255))
        self.screen.blit(score, (10, 10))
        self.screen.blit(time, (210, 10))
        self.screen.blit(shoots, (410, 10))
        self.screen.blit(accuracy, (610, 10))