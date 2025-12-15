"""
Konfigurační soubor hry Arena Survival.

Obsahuje všechny globální konstanty a herní parametry.
"""

# Rozměry herního okna v pixelech
WIDTH = 800
HEIGHT = 600

# Počet snímků za sekundu (FPS)
FPS = 60

# Rychlosti pohybu entit v pixelech za sekundu
PLAYER_SPEED = 250   # Rychlost pohybu hráče
ENEMY_SPEED = 100    # Rychlost pohybu nepřátel
BULLET_SPEED = 400   # Rychlost projektilů

SHOOT_DISTANCE = 50  # Maximální vzdálenost pro střelbu v pixelech
MAX_SHOOTS = 20      # Maximální počet střel na hru

# Herní parametry
BULLET_LIFETIME = .5   # Doba života projektilu v sekundách
SPAWN_INTERVAL = 2.0    # Interval pro spawn nepřátel v sekundách

# Obtížnost a velikosti nepřátel
DIFFICULTY_LEVELS = ["Lama", "Machr", "Superman"]
ENEMY_SIZE_BY_DIFFICULTY = {
	"Lama": (40, 40),       # Největší nepřátelé - nejlehčí
	"Machr": (30, 30),      # Výchozí velikost
	"Superman": (22, 22),   # Nejmenší nepřátelé - nejtěžší
}
