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
        self.state = "menu"
        self.menu = Menu(self)
        self.settings_menu = SettingsMenu(self)
        self.score_menu = ScoreMenu(self)

        # Herní nastavení
        self.difficulties = DIFFICULTY_LEVELS
        self.difficulty_index = 0  # Výchozí: "Lama"
        self.sound_on = True
        self.sounds = self._load_sounds()

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
            
            if self.state == "menu":
                self.menu.draw(self.screen)
                pygame.display.flip()

            elif self.state == "game":
                self.update(dt)
                self.draw()
                
            elif self.state == "settings":
                self.settings_menu.draw(self.screen)
                pygame.display.flip()
                
            elif self.state == "scores":
                self.score_menu.draw(self.screen)
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

            if self.state == "menu":
                self.menu.handle_event(event)

            elif self.state == "settings":
                self.settings_menu.handle_event(event)
                
            elif self.state == "scores":
                self.score_menu.handle_event(event)

            elif self.state == "game":
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
                self.play_sound("hit")

        # Detekce kolize nepřátel s hráčem (game over)
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.state = "menu"
            self.reset_game()

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