# 🚀 **Pokročilá témata pro rozšíření hry**

Tady najdeš krátké návody, jak přidat profesionálnější prvky do vaší arénové hry.

---

# 🎵 **1. Zvuky**

## (střelba, exploze, hudba)

### Aktivace zvuku:

```python
pygame.mixer.init()
```

### Načtení zvuku:

```python
shoot_sound = pygame.mixer.Sound("assets/shoot.wav")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
```

### Použití:

```python
shoot_sound.play()
```

### Hudba na pozadí:

```python
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.play(-1)   # -1 = loop
```

---

# 🖼️ **2. Grafika – sprite sheety místo čtverců**

Místo `pygame.Surface` používej skutečné obrázky:

```python
self.image = pygame.image.load("assets/player.png").convert_alpha()
```

Pokud obrázek obsahuje více snímků (sheet):

* rozdělit na jednotlivé frames
* uložit do listu
* vybrat správný frame v update()

---

# 🎨 **3. Animace**

### 1. Načti snímky animace:

```python
self.frames = [frame1, frame2, frame3, ...]
self.frame_index = 0
```

### 2. V update():

```python
self.frame_index += animation_speed * dt
self.image = self.frames[int(self.frame_index) % len(self.frames)]
```

To vytvoří hladkou animaci postavičky / nepřítele.

---

# 💥 **4. Částicové efekty (Particle System)**

Použij:

* malé sprite (2–6 px)
* náhodný směr, rychlost a životnost

### Mini třída částice:

```python
class Particle(Entity):
    def __init__(self, pos):
        super().__init__(game, pos, (3,3), random_color)
        self.vel = Vector2(random_dir) * speed
        self.life = 0.5

    def update(self, dt):
        self.pos += self.vel * dt
        self.life -= dt
        if self.life <= 0:
            self.kill()
```

Volání při zásahu nepřítele:

```python
for _ in range(10):
    Particle(enemy.pos)
```

---

# ⚡ **5. Power-upy**

Např. **rychlost**, **štít**, **double-shot**, **heal**.

### Power-up objekt:

* sprite v aréně
* když hráč koliduje → aktivace efektu (např. zvýšení rychlosti na 5 sekund)

```python
player.speed *= 1.5
player.powerup_timer = 5
```

V update hráče odpočítávat:

```python
player.powerup_timer -= dt
if player.powerup_timer <= 0:
    player.speed = PLAYER_SPEED
```

---

# 🎯 **6. Různé typy nepřátel**

Vytvoř rodiče:

```python
class Enemy(Entity):
    speed = 100
    health = 1
```

A potomky:

### Rychlý nepřítel:

```python
class FastEnemy(Enemy):
    speed = 200
```

### Silný tank:

```python
class TankEnemy(Enemy):
    speed = 50
    health = 3
```

Spawner je bude generovat náhodně nebo podle levelu.

---

# 🛡️ **7. Životy hráče (Health system)**

Do `Player`:

```python
self.health = 3
```

Když hráče zasáhne nepřítel:

```python
player.health -= 1
if player.health <= 0:
    game.running = False
```

Zobraz životy v HUD:

```python
draw_hearts(player.health)
```

---

# 📊 **8. Obtížnost (Difficulty Scaling)**

Zrychlování:

* zkracuj spawn interval
* zvyšuj rychlost nepřátel
* zvyšuj jejich HP

Příklad:

```python
self.difficulty_timer += dt
if self.difficulty_timer > 10:
    SPAWN_INTERVAL *= 0.9
    ENEMY_SPEED += 10
    self.difficulty_timer = 0
```

Každých 10 sekund obtížnější hra.

---

# 🏆 **9. High Score – ukládání nejlepšího skóre**

Do souboru:

```python
with open("highscore.txt", "w") as f:
    f.write(str(score))
```

Načtení:

```python
try:
    high = int(open("highscore.txt").read())
except:
    high = 0
```

Zobrazení v HUD:

```python
text = font.render(f"Highscore: {high}", True, white)
```

---

# 🌈 **10. Menu – start, pause, game over**

### Start screen:

* nápis hry
* stiskni Enter pro start

### Pause menu:

* `P` pozastaví hru
* zobrazí overlay

### Game Over:

* skóre
* možnost restartu

Struktura pomocí jednoduchého „state machine“:

```python
self.state = "menu"  # menu, game, pause, game_over
```

V herní smyčce:

```python
if self.state == "menu":
    draw_menu()
elif self.state == "game":
    update_game()
elif self.state == "pause":
    draw_pause()
```

---

# ⭐ BONUS: Doporučený postup pro studenty

1. Přidat **zvuk střelby**
2. Načíst vlastní **sprite hráče**
3. Vytvořit **animaci** nepřítele
4. Přidat jednoduchý **výbuch z částic**
5. Udělat **power-up** (např. speed boost)
6. Vytvořit dva typy nepřátel
7. Přidat **životy hráče**
8. Udělat **obtížnost**
9. Ukládat **high score**
10. Přidat **menu**

