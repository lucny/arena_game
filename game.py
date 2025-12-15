"""
Hlavní herní třída pro Arena Survival.

Spravuje herní smyčku, sprite skupiny, kolize a vykreslování.
"""

import pygame
from settings import WIDTH, HEIGHT, FPS, DIFFICULTY_LEVELS, ENEMY_SIZE_BY_DIFFICULTY
from entities.player import Player
from systems.spawner import Spawner
from ui.menu import Menu
from ui.settings_menu import SettingsMenu
from ui.score_menu import ScoreMenu
from ui.widgets import draw_hud, draw_input_panel, draw_panel

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
        
        # Herní menu a nastavení
        self.state = "menu"  # Začínáme menu
        self.menu = Menu(self)
        self.waiting_for_name = False  # Flag pro čekání na jméno před hrou
        self.settings_menu = SettingsMenu(self)
        self.score_menu = ScoreMenu(self)

        # Herní nastavení
        self.difficulties = DIFFICULTY_LEVELS
        self.difficulty_index = 0  # Výchozí: "Lama"
        self.sound_on = True
        self.sounds = self._load_sounds()
        self.player_name = ""
        self.last_result = None

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
        self.game_start_time = None  # Zaznamenání času startu hry

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
            
            if self.state == "menu":
                self.menu.draw(self.screen)
                pygame.display.flip()

            elif self.state == "name_entry":
                self.draw_name_entry()
                pygame.display.flip()

            elif self.state == "game":
                # Hra je spuštěna
                if self.game_start_time is None:
                    # Poprvé vstupujeme do běhu hry
                    self.game_start_time = pygame.time.get_ticks()
                    self.reset_game()
                self.update(dt)
                self.draw()
                
            elif self.state == "settings":
                self.settings_menu.draw(self.screen)
                pygame.display.flip()
                
            elif self.state == "scores":
                self.score_menu.draw(self.screen)
                pygame.display.flip()

            elif self.state == "game_over":
                self.draw_game_over()
                pygame.display.flip()

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

            if self.waiting_for_name:
                self._handle_name_event(event)

            elif self.state == "menu":
                self.menu.handle_event(event)

            elif self.state == "settings":
                self.settings_menu.handle_event(event)
                
            elif self.state == "scores":
                self.score_menu.handle_event(event)

            elif self.state == "game":
                # Střelba na kliknutí myši
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.shoot()

            elif self.state == "game_over":
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    self.reset_game()
                    self.state = "menu"

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
                self.play_sound("hit")

        # Detekce kolize nepřátel s hráčem (game over)
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.last_result = {
                "name": self.player_name or "Anon",
                "score": self.score,
                "shoots": self.shoots,
                "accuracy": int((self.score / self.shoots * 100) if self.shoots > 0 else 0),
                "difficulty": self.difficulties[self.difficulty_index],
            }
            self.state = "game_over"

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
        elapsed = 0
        if self.game_start_time is not None:
            elapsed = int((pygame.time.get_ticks() - self.game_start_time) / 1000)
        draw_hud(
            self.screen,
            score=self.score,
            time_value=elapsed,
            shoots=self.shoots,
            accuracy=int((self.score / self.shoots * 100) if self.shoots > 0 else 0),
        )
    
    # ------------------------------------------------------------------
    def reset_game(self):
        """
        Resetuje hru do počátečního stavu.
        
        Vyčistí všechny sprite skupiny a vytvoří nové objekty.
        """
        # Vyčištění všech sprite skupin
        self.all_sprites.empty()
        self.enemies.empty()
        self.bullets.empty()
        
        # Vytvoření nového hráče
        self.player = Player(self, (WIDTH // 2, HEIGHT // 2))
        self.all_sprites.add(self.player)
        
        # Reset spawneru
        self.spawner = Spawner(self)
        
        # Reset skóre a statistik
        self.score = 0
        self.shoots = 0

    # ------------------------------------------------------------------
    def start_new_game(self):
        """Přechod na zadávání jména a následně na hru."""
        self.player_name = ""
        self.waiting_for_name = True
        self.state = "name_entry"

    # ------------------------------------------------------------------
    def get_enemy_size(self):
        """Vrátí velikost nepřítele podle aktuální obtížnosti."""
        difficulty = self.difficulties[self.difficulty_index]
        return ENEMY_SIZE_BY_DIFFICULTY.get(difficulty, (30, 30))

    # ------------------------------------------------------------------
    def set_difficulty(self, name):
        """Nastaví obtížnost podle názvu, pokud existuje."""
        if name in self.difficulties:
            self.difficulty_index = self.difficulties.index(name)

    # ------------------------------------------------------------------
    def toggle_sound(self):
        """Přepíná stav zvuku."""
        self.sound_on = not self.sound_on

    # ------------------------------------------------------------------
    def play_sound(self, name):
        if not self.sound_on:
            return

        sound = self.sounds.get(name)
        if sound:
            sound.play()

    # ------------------------------------------------------------------
    def _load_sounds(self):
        return {
            "shoot": self._safe_load_sound("assets/sounds/ding.wav"),
            "hit": self._safe_load_sound("assets/sounds/chord.wav"),
        }

    # ------------------------------------------------------------------
    def _safe_load_sound(self, path):
        try:
            return pygame.mixer.Sound(path)
        except pygame.error:
            return None

    def _handle_name_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_RETURN:
            if self.player_name.strip():
                self.waiting_for_name = False
                self.state = "game"
            return

        if event.key == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]
            return

        # Přidání znaku, pouze pokud je tisknutelný
        if event.unicode.isprintable() and len(self.player_name) < 12:
            self.player_name += event.unicode

    # ------------------------------------------------------------------
    def draw_name_entry(self):
        draw_input_panel(
            self.screen,
            "Zadejte jméno hráče",
            self.player_name or "_",
            "Enter pro potvrzení, Backspace smaže",
        )

    # ------------------------------------------------------------------
    def draw_game_over(self):
        name = self.last_result.get("name") if self.last_result else ""  # type: ignore[attr-defined]
        score = self.last_result.get("score", 0) if self.last_result else 0
        shoots = self.last_result.get("shoots", 0) if self.last_result else 0
        acc = self.last_result.get("accuracy", 0) if self.last_result else 0
        difficulty = self.last_result.get("difficulty", "?") if self.last_result else "?"

        lines = [
            f"Hráč: {name}",
            f"Skóre: {score}",
            f"Výstřely: {shoots}",
            f"Úspěšnost: {acc}%",
            f"Obtížnost: {difficulty}",
        ]
        draw_panel(self.screen, "Konec hry", lines, "Enter nebo ESC pro návrat do menu")