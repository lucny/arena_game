# 🎯 Vektorová matematika pro programování her

### (směr, normalizace, vzdálenost)

## 1. Co je vektor?

📌 **Vektor = “šípka”, která má:**

* **směr** (kam ukazuje)
* **velikost** (jak je dlouhý)

V Pygame často používáme:

```python
pygame.Vector2(x, y)
```

Např.:

```python
v = pygame.Vector2(3, 4)
```

Tento vektor ukazuje z počátku směrem k bodu (3,4).

---

# 2. Rozdíl mezi pozicí a vektorem

* **Pozice** = kde objekt je (např. hráč, nepřítel).
* **Vektor** = buď pozice, nebo směr, nebo rychlost.

Příklad:

```python
player.pos = Vector2(200, 300)
enemy.pos = Vector2(100, 100)
```

Rozdíl mezi hráčem a nepřítelem:

```python
direction = player.pos - enemy.pos
```

👉 Tohle je **vektor směru** od nepřítele k hráči.

---

# 3. Velikost vektoru (délka)

Velikost vektoru (délka šipky) vypočítáme:

* Pythagorova věta
* nebo pomocí funkce `.length()` v Pygame

```python
v = Vector2(3, 4)
print(v.length())  # 5 (protože √(3² + 4²) = 5)
```

---

# 4. Normalizace vektoru

### „Chceme jen směr, nezáleží na délce.“

Normalizovaný vektor má:

* stejný **směr** jako původní,
* ale **délku 1**.

Proč je to užitečné?

🎮 Aby se objekt pohyboval stále stejnou rychlostí bez ohledu na vzdálenost cíle.

V Pygame:

```python
direction = (player.pos - enemy.pos).normalize()
```

* pokud je hráč daleko → vektor je delší
* pokud je blízko → kratší
* ale po `.normalize()` má vždy délku 1

Pak rychlostu nastavíme:

```python
velocity = direction * SPEED   # vždy rychlost SPEED
```

---

# 5. Vzdálenost mezi dvěma body

Velmi často potřebujeme:

* zjistit, jak daleko je nepřítel od hráče,
* kdy odpálit střelu,
* kdy zkontrolovat kolizi,
* kdy spustit AI logiku.

V Pygame:

```python
distance = player.pos.distance_to(enemy.pos)
```

Nebo ručně:

```python
distance = (player.pos - enemy.pos).length()
```

---

# 6. Směr pohybu (vektor cíle – zdroj)

Základní způsob, jak objekt nasměrovat:

```python
direction = target - source
```

Příklad: nepřítel běží k hráči:

```python
direction = (player.pos - enemy.pos)
if direction.length() > 0:
    direction = direction.normalize()

enemy.pos += direction * ENEMY_SPEED * dt
```

### Co se tu děje?

1. vzdálenost mezi hráčem a nepřítelem vytvoří vektor,
2. normalizací získáme čistý směr,
3. vynásobíme rychlostí,
4. posuneme.

To je **nejčastější vzorec v herní 2D matematice**.

---

# 7. Praktické příklady

## 7.1 Střela letí směrem k myši

```python
mouse_pos = Vector2(pygame.mouse.get_pos())
direction = (mouse_pos - bullet.pos).normalize()
bullet.pos += direction * BULLET_SPEED * dt
```

## 7.2 Zpomalení na místě (tlumení vektoru)

```python
velocity *= 0.95  # ztráta rychlosti vlivem tření
```

## 7.3 Vzdálenost od hráče rozhoduje o chování AI

```python
dist = player.pos.distance_to(enemy.pos)

if dist < 50:
    enemy.attack()
elif dist < 200:
    enemy.chase()
else:
    enemy.patrol()
```

---

# 8. Shrnutí pro studenty (krátké a zapamatovatelné)

> 🟦 **Vektor = směr + velikost**
> 🟩 **Směr k cíli = target - source**
> 🟨 **Normalizace = vektor délky 1**
> 🟧 **Rychlost = normalizovaný směr × SPEED**
> 🟥 **Vzdálenost = (a - b).length() nebo distance_to()**

Těchto 5 pravidel tvoří 90 % vektorové matematiky používané v 2D hrách.

