"""
Menu nastavení pro Arena Survival.

Volba obtížnosti (Lama, Machr, Superman) mění velikost nepřátel,
zvuk je přepínač.
"""

import pygame
from settings import DIFFICULTY_LEVELS
from ui.widgets import draw_menu

DIFFICULTY_LABEL = "Obtížnost"
SOUND_LABEL = "Zvuk"
BACK_LABEL = "Zpět"


class SettingsMenu:
    """Menu pro změnu nastavení hry."""

    def __init__(self, game):
        self.game = game
        self.options = [DIFFICULTY_LABEL, SOUND_LABEL, BACK_LABEL]
        self.selected = 0

    # ------------------------------------------------------------------
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.options)
        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.options)
        elif event.key == pygame.K_LEFT:
            self._adjust_option(-1)
        elif event.key == pygame.K_RIGHT:
            self._adjust_option(1)
        elif event.key == pygame.K_RETURN:
            self._activate_option()
        elif event.key == pygame.K_ESCAPE:
            self.game.state = "menu"

    # ------------------------------------------------------------------
    def _activate_option(self):
        current = self.options[self.selected]
        if current == DIFFICULTY_LABEL:
            self._change_difficulty(1)
        elif current == SOUND_LABEL:
            self.game.toggle_sound()
        elif current == BACK_LABEL:
            self.game.state = "menu"

    # ------------------------------------------------------------------
    def _adjust_option(self, direction):
        current = self.options[self.selected]
        if current == DIFFICULTY_LABEL:
            self._change_difficulty(direction)
        elif current == SOUND_LABEL:
            self.game.toggle_sound()

    # ------------------------------------------------------------------
    def _change_difficulty(self, step):
        total = len(DIFFICULTY_LEVELS)
        self.game.difficulty_index = (self.game.difficulty_index + step) % total

    # ------------------------------------------------------------------
    def draw(self, screen):
        option_texts = [
            f"{DIFFICULTY_LABEL}: {self._current_difficulty_name()}",
            f"{SOUND_LABEL}: {'Zapnutý' if self.game.sound_on else 'Vypnutý'}",
            BACK_LABEL,
        ]

        draw_menu(
            screen,
            "NASTAVENÍ",
            option_texts,
            self.selected,
            hint=[
                "Šipky nahoru/dolů: výběr položky",
                "Šipky vlevo/vpravo nebo Enter: změna hodnoty",
                "ESC: zpět do menu",
            ],
            start_y=200,
            option_spacing=50,
            hint_y_offset=80,
        )

    # ------------------------------------------------------------------
    def _current_difficulty_name(self):
        return DIFFICULTY_LEVELS[self.game.difficulty_index]