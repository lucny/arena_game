"""
Hlavní menu pro Arena Survival.

Poskytuje navigaci mezi různými částmi hry.
"""

import pygame
from ui.widgets import draw_menu

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
            self.game.start_new_game()

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
        draw_menu(
            screen,
            "ARENA SURVIVAL",
            self.options,
            self.selected,
            hint="Použijte šipky a Enter pro výběr",
        )
