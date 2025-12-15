"""
Hlavní menu pro Arena Survival.

Poskytuje navigaci mezi různými částmi hry.
"""

import pygame
from settings import WIDTH, HEIGHT

class Menu:
    """
    Hlavní menu hry.
    
    Attributes:
        game: Reference na Game objekt
        options: Seznam možností menu
        selected: Index aktuálně vybrané možnosti
    """
    
    def __init__(self, game):
        """
        Inicializuje hlavní menu.
        
        Args:
            game: Reference na Game objekt
        """
        self.game = game
        self.options = [
            "Nová hra",
            "Nastavení",
            "Výsledky",
            "Konec"
        ]
        self.selected = 0

        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 32)

    def handle_event(self, event):
        """
        Zpracovává vstupy v hlavním menu.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)

            elif event.key == pygame.K_RETURN:
                self.activate_option()

    def activate_option(self):
        """
        Aktivuje vybranou možnost menu.
        """
        option = self.options[self.selected]

        if option == "Nová hra":
            self.game.reset_game()  # Reset hry před začátkem
            self.game.state = "game"

        elif option == "Nastavení":
            self.game.state = "settings"

        elif option == "Výsledky":
            self.game.state = "scores"

        elif option == "Konec":
            self.game.running = False

    def draw(self, screen):
        """
        Vykresluje hlavní menu na obrazovku.
        
        Args:
            screen: Pygame Surface pro vykreslování
        """
        screen.fill((20, 20, 20))

        # Nadpis
        title = self.font.render("ARENA SURVIVAL", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 150)))

        # Možnosti menu
        for i, option in enumerate(self.options):
            color = (255, 200, 50) if i == self.selected else (200, 200, 200)
            text = self.small_font.render(option, True, color)
            screen.blit(text, text.get_rect(center=(WIDTH // 2, 250 + i * 40)))
        
        # Nápověda
        hint = self.small_font.render("Použijte šipky a Enter pro výběr", True, (150, 150, 150))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 50)))
