"""
Menu výsledků pro Arena Survival.

Zobrazuje žebríčky nejlepších hráčů dle obtížnosti.
"""

import pygame
from ui.widgets import draw_panel
from systems.leaderboard import get_leaderboard, DIFFICULTIES


class ScoreMenu:
    """
    Menu pro zobrazení výsledků a žebríčků.
    
    Attributes:
        game: Reference na Game objekt
        selected_difficulty: Index vybrané obtížnosti
    """
    
    def __init__(self, game):
        """
        Inicializuje score menu.
        
        Args:
            game: Reference na Game objekt
        """
        self.game = game
        self.selected_difficulty = 0  # Výchozí: Lama
    
    def handle_event(self, event):
        """
        Zpracovává vstupy v score menu.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_difficulty = (self.selected_difficulty - 1) % len(DIFFICULTIES)
            elif event.key == pygame.K_RIGHT:
                self.selected_difficulty = (self.selected_difficulty + 1) % len(DIFFICULTIES)
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.game.state = "menu"
    
    def draw(self, screen):
        """
        Vykresluje score menu na obrazovku.
        
        Args:
            screen: Pygame Surface pro vykreslování
        """
        # Načti žebríček pro vybranou obtížnost
        difficulty = DIFFICULTIES[self.selected_difficulty]
        leaderboard = get_leaderboard(difficulty, limit=5)
        
        # Sestav řádky s výsledky
        lines = []
        if leaderboard:
            for i, result in enumerate(leaderboard):
                name = result.get("name", "?")
                score = result.get("score", 0)
                game_duration_ms = result.get("game_duration_ms", 0)
                game_duration_s = game_duration_ms // 1000
                minutes = game_duration_s // 60
                seconds = game_duration_s % 60
                accuracy = result.get("accuracy", 0)
                lines.append(f"{i+1}. {name}: {minutes}:{seconds:02d} ({score} bodů, {accuracy}%)")
        else:
            lines.append("Zatím žádné výsledky")
        
        # Zobraz panel s nápovědá o výběru obtížnosti
        hint = [
            f"Obtížnost: {difficulty}",
            "Šipky vlevo/vpravo pro zmenu obtížnosti",
            "Enter nebo ESC pro návrat"
        ]
        
        draw_panel(
            screen,
            "NEJLEPŠÍ VÝSLEDKY",
            lines,
            hint=hint,
            title_color=(255, 255, 255),
            line_color=(200, 200, 200),
            title_y=100,
            start_y=200,
            line_spacing=50,
            hint_y_offset=80,
        )