"""
Menu nastavení pro Arena Survival.

Umožňuje uživateli měnit herní parametry.
"""

import pygame
from settings import WIDTH, HEIGHT

class SettingsMenu:
    """
    Menu pro změnu nastavení hry.
    
    Attributes:
        game: Reference na Game objekt
        options: Seznam dostupných nastavení
        selected: Index aktuálně vybrané možnosti
    """
    
    def __init__(self, game):
        """
        Inicializuje settings menu.
        
        Args:
            game: Reference na Game objekt
        """
        self.game = game
        self.options = [
            "Obtížnost: Normální",
            "Zvuk: Zapnuto",
            "Hudba: Zapnuta",
            "Zpět"
        ]
        self.selected = 0
        
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 32)
    
    def handle_event(self, event):
        """
        Zpracovává vstupy v settings menu.
        
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
            
            elif event.key == pygame.K_ESCAPE:
                self.game.state = "menu"
    
    def activate_option(self):
        """
        Aktivuje vybranou možnost.
        """
        option = self.options[self.selected]
        
        if "Zpět" in option:
            self.game.state = "menu"
        
        # TODO: Implementace změny nastavení
        # Zatím pouze placeholder pro budoucí funkcionalitu
    
    def draw(self, screen):
        """
        Vykresluje settings menu na obrazovku.
        
        Args:
            screen: Pygame Surface pro vykreslování
        """
        screen.fill((20, 20, 20))
        
        # Nadpis
        title = self.font.render("NASTAVENÍ", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))
        
        # Možnosti
        for i, option in enumerate(self.options):
            color = (255, 200, 50) if i == self.selected else (200, 200, 200)
            text = self.small_font.render(option, True, color)
            screen.blit(text, text.get_rect(center=(WIDTH // 2, 200 + i * 50)))
        
        # Nápověda
        hint = self.small_font.render("Použijte šipky a Enter pro výběr, ESC pro návrat", True, (150, 150, 150))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 50)))