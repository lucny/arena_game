"""
Menu výsledků pro Arena Survival.

Zobrazuje high score a statistiky hry.
"""

import pygame
from settings import WIDTH, HEIGHT

class ScoreMenu:
    """
    Menu pro zobrazení výsledků a statistik.
    
    Attributes:
        game: Reference na Game objekt
        font: Font pro nadpis
        small_font: Font pro text
    """
    
    def __init__(self, game):
        """
        Inicializuje score menu.
        
        Args:
            game: Reference na Game objekt
        """
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 32)
        
        # Placeholder pro high scores
        self.high_scores = [
            ("Hráč 1", 150),
            ("Hráč 2", 120),
            ("Hráč 3", 100),
            ("Hráč 4", 80),
            ("Hráč 5", 50)
        ]
    
    def handle_event(self, event):
        """
        Zpracovává vstupy v score menu.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.game.state = "menu"
    
    def draw(self, screen):
        """
        Vykresluje score menu na obrazovku.
        
        Args:
            screen: Pygame Surface pro vykreslování
        """
        screen.fill((20, 20, 20))
        
        # Nadpis
        title = self.font.render("NEJLEPŠÍ VÝSLEDKY", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))
        
        # High scores
        for i, (name, score) in enumerate(self.high_scores):
            color = (255, 200, 50) if i == 0 else (200, 200, 200)
            text = self.small_font.render(f"{i+1}. {name}: {score}", True, color)
            screen.blit(text, text.get_rect(center=(WIDTH // 2, 200 + i * 50)))
        
        # Aktuální skóre
        if self.game.score > 0:
            current = self.small_font.render(f"Vaše poslední skóre: {self.game.score}", True, (100, 255, 100))
            screen.blit(current, current.get_rect(center=(WIDTH // 2, HEIGHT - 100)))
        
        # Nápověda
        hint = self.small_font.render("Stiskněte Enter nebo ESC pro návrat", True, (150, 150, 150))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 50)))