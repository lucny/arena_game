"""
Menu výsledků pro Arena Survival.

Zobrazuje high score a statistiky hry.
"""

import pygame
from ui.widgets import draw_panel

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
        lines = [f"{i+1}. {name}: {score}" for i, (name, score) in enumerate(self.high_scores)]

        if self.game.score > 0:
            lines.append(f"Vaše poslední skóre: {self.game.score}")

        draw_panel(
            screen,
            "NEJLEPŠÍ VÝSLEDKY",
            lines,
            hint="Stiskněte Enter nebo ESC pro návrat",
            title_color=(255, 255, 255),
            line_color=(200, 200, 200),
            highlight_first=True,
            bg_color=(20, 20, 20),
            title_y=100,
            start_y=200,
            line_spacing=50,
            hint_y_offset=50,
        )