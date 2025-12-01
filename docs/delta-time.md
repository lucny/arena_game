# 🎯 Výukový materiál – **Delta time (dt)**

## Jak zajistit plynulý pohyb nezávislý na frameratu

---

# 1. Co je framerate (FPS)?

**FPS = Frames Per Second**
= kolikrát se za sekundu překreslí obrazovka.

* běžné: **60 FPS**
* slabší PC: **30 FPS**
* výkonnější: **120+ FPS**

Každý „frame“ (snímek) se skládá z:

1. zpracování vstupů
2. výpočtů (update)
3. vykreslení scény (draw)

---

# 2. Problém bez delta time

Pokud bychom pohyb zapisovali jako:

```python
player.x += 5   # 5 pixelů za frame
```

Tak:

* při **60 FPS** → pohne se 5 × 60 = **300 px/s**
* při **30 FPS** → 5 × 30 = **150 px/s**

💥 **Rychlost hry závisí na rychlosti počítače!**
Na slabším počítači by byla hra o polovinu pomalejší.

To je špatně — chceme spravedlivý, konzistentní pohyb.

---

# 3. Řešení: Delta time

**Delta time (dt)** = čas mezi dvěma snímky.

Hra si změří, kolik milisekund uplynulo od posledního frame.

V Pygame:

```python
dt = clock.tick(60) / 1000
```

Co to dělá?

* `clock.tick(60)` → říká, že chceme max. 60 FPS
* vrací **čas v milisekundách**, který uplynul od posledního snímku
* děleno `1000` → převedeme na **sekundy**

Např.:

| FPS     | čas jednoho frame | dt        |
| ------- | ----------------- | --------- |
| 60 FPS  | 16 ms             | **0.016** |
| 30 FPS  | 33 ms             | **0.033** |
| 120 FPS | 8 ms              | **0.008** |

Delta time je tedy **nezávislé měřítko času**, které se v pohybu použije jako násobitel.

---

# 4. Jak delta time použít v pohybu

Místo „na frame“ počítáme rychlost **za sekundu**.

Např. chceme, aby se hráč pohyboval rychlostí:

```python
PLAYER_SPEED = 200   # 200 px za sekundu
```

Použití:

```python
player.x += PLAYER_SPEED * dt
```

Výsledek:

* při 60 FPS → 200 * 0.016 ≈ **3.2 px**
* při 30 FPS → 200 * 0.033 ≈ **6.6 px**
* při 120 FPS → 200 * 0.008 ≈ **1.6 px**

Všimni si:

* různé počty pixelů **za frame**,
* ale za jednu sekundu je to **vždy 200 px**.

➡️ **Rychlost je stabilní a nezávislá na výkonu počítače.**

---

# 5. Delta time v Pygame – kompletní příklad

### Herní smyčka:

```python
clock = pygame.time.Clock()

while True:
    dt = clock.tick(60) / 1000   # delta time v sekundách

    player.update(dt)
    game.update(dt)

    draw()
```

### Pohyb hráče:

```python
self.pos += self.velocity * dt
self.rect.center = self.pos
```

---

# 6. Proč je delta time důležitá?

### ✔ spravedlivá hra

Nemůže se stát, že na slabém počítači se hra zpomalí
(př. multiplayer → všichni běží rozdílně rychle).

### ✔ konzistentní fyzika

Výpočty závislé na čase (skoky, gravitace, rychlost střel).

### ✔ správné animace

Animace založené na čase, ne na počtu framů.

### ✔ profesionální standard

Každý herní engine (Unity, Unreal, Godot) používá dt.

---

# 7. Typické chyby studentů

### ❌ 1. Zaměnění rychlosti a delta time

Špatně:

```python
player.pos += 5    # nelze řídit rychlost
```

Správně:

```python
player.pos += SPEED * dt
```

---

### ❌ 2. Zapomenutý dt v jedné části logiky

Např. nepřátelé se hýbou podle dt, ale střely ne →
→ různé rychlosti podle FPS.

---

### ❌ 3. dt v milisekundách místo sekund

Špatně:

```python
dt = clock.tick(60)   # 16 nebo 33 (příliš velké číslo)
```

Správně:

```python
dt = clock.tick(60) / 1000
```

---

# 8. Ukázkový příklad – enemy jde směrem k hráči

```python
direction = (player.pos - enemy.pos)
if direction.length() > 0:
    direction = direction.normalize()

enemy.pos += direction * ENEMY_SPEED * dt
enemy.rect.center = enemy.pos
```

Díky dt:

* na rychlém PC → více krátkých kroků
* na pomalém PC → méně dlouhých kroků
* ale **stejná rychlost v čase**.

---

# 9. Shrnutí pro studenty

> **Delta time (dt)** je čas mezi dvěma snímky.
> Používá se k tomu, aby pohyb nebyl závislý na FPS.
> Správný pohyb = `rychlost_za_sekundu × dt`.

Tři klíčové řádky:

```python
dt = clock.tick(60) / 1000
position += velocity * dt
```


