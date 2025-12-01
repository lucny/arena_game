# 🎯 Výukový materiál – **Kolize v 2D hrách**

## Detekce, zpracování a principy

---

# 1. Co je kolize?

**Kolize (collision)** nastane, když se dva objekty ve hře **dotknou** nebo **protnou**.

Například:

* hráč narazí do zdi
* střela zasáhne nepřítele
* míček se odrazí od pálky (Pong)
* hráč sbírá mince

Kolize je základní stavební kámen herní logiky.

---

# 2. Co potřebujeme ke kolizím?

Abychom kolize mohli testovat, každý objekt musí mít:

* **pozici**
* **rozměr** (šířka, výška)
* často také **správný tvar kolizního objektu** (např. obdélník, kruh)

V Pygame to obvykle řeší:

### 🎨 `sprite.image`

grafický obrázek

### 📦 `sprite.rect`

obdélník popisující pozici a velikost
(`get_rect()` se získá automaticky z image)

---

# 3. Typy kolizí v 2D hrách

## 3.1 Kolize obdélníků (Axis-Aligned Bounding Box – AABB)

Dva osově zarovnané obdélníky se dotknou, pokud se jejich:

* horizontální projekce **překrývají**, a
* vertikální projekce také.

V Pygame velmi jednoduché:

```python
if rect1.colliderect(rect2):
    print("Kolize!")
```

To je nejčastější a nejrychlejší metoda.

---

## 3.2 Kolize bodu s obdélníkem

Používá se třeba u kliknutí myší:

```python
if rect.collidepoint(mouse_pos):
    print("Hit!")
```

---

## 3.3 Kolize kruh × kruh

Často se používá u střel, meteorů, kulečných her.

Podmínka:

```
vzdálenost mezi středy < součet poloměrů
```

Pygame to nenabízí přímo, ale dá se snadno spočítat:

```python
dist = center1.distance_to(center2)
if dist < r1 + r2:
    print("Kolize kruhů!")
```

---

# 4. Kolize v Pygame pomocí Sprite Group

Pygame umí hromadné testování kolizí mezi skupinami spriteů.

## 4.1 Jedna střela proti skupině nepřátel

```python
hits = pygame.sprite.spritecollide(bullet, enemies, dokill=True)
```

* první argument: *co testujeme*
* druhý: *proti kterým objektům*
* `dokill=True` → smaže nepřátele po kolizi
* funkce vrací seznam kolidujících objektů

Příklad:

```python
if hits:
    bullet.kill()   # zničíme i střelu
```

---

## 4.2 Skupina proti skupině

```python
collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)
```

Tohle smaže *střely i nepřátele*, kteří se střetli.

---

## 4.3 Jednotlivý sprite proti skupině

Typicky hráč vs. nepřátelé:

```python
if pygame.sprite.spritecollide(player, enemies, False):
    player.hit()
```

---

# 5. Jak kolize **zpracovat** (logika po detekci)

Kolize je jen informace.
Musíme rozhodnout, *co se stane*.

Typické reakce:

### 🎮 1. Odrážení

→ Pong, Arkanoid, Breakout
→ změníme směr:

```python
ball_direction.y *= -1
```

---

### 💥 2. Zničení objektu

→ střely, nepřátelé, bloky

```python
enemy.kill()
bullet.kill()
```

---

### ❤️ 3. Ztráta života / poškození

```python
player.health -= 1
```

---

### 🪙 4. Sebrání předmětu

```python
player.inventory.add("gold")
item.kill()
```

---

### 🧠 5. Aktivace AI nebo změna stavu hry

```python
if player.pos.distance_to(enemy.pos) < 50:
    enemy.change_state("attack")
```

---

# 6. Kolize a fyzika (odraz)

V arkádách (Breakout, Pong):

1. zjistíme, **ze které strany** objekt narazil
2. podle toho otočíme složku rychlosti

Např. náraz do stěny (vertikální plocha):

```python
ball.velocity.x *= -1
```

Náraz do vodorovné:

```python
ball.velocity.y *= -1
```

---

# 7. Vektorová kolizní logika

Vektorová matematika je u kolizí důležitá:

* **vzdálenost**
* **směr odrazu**
* **impakt síly**
* **posun mimo kolizi (push-back)**

Příklad: prosté odsunutí objektu:

```python
direction = (enemy.pos - player.pos).normalize()
enemy.pos += direction * 5  # odsunutí o 5 pixelů
```

---

# 8. Typické problémy s kolizemi a jejich řešení

## ❌ Objekt „proletí skrz“ jiný objekt

Příčina: vysoká rychlost.

Řešení:

* kontrolovat kolize po malých krocích,
* snížit rychlost,
* zvýšit FPS,
* použít diskrétní fyziku (více iterací update).

---

## ❌ Objekty se „zasekávají“

Příčina: objekt se po kolizi neposune ven.

Řešení:

* po kolizi objekt **vytlačit** mimo překryv,
* používat `rect` pro přesné umístění.

---

## ❌ Kolize spriteů nefungují

Možné příčiny:

* objekt není ve správné `Sprite Group`,
* nemá atribut `rect`,
* rect není aktualizován při pohybu,
* obrázek má nesprávné rozměry.

---

# 9. Kompletní příklad (Pygame – nepřítel po zásahu zmizí)

```python
for bullet in bullets:
    hits = pygame.sprite.spritecollide(bullet, enemies, True)
    if hits:
        bullet.kill()
        score += len(hits)
```

* střela se testuje proti skupině,
* když zasáhne: nepřítel zmizí,
* zničíme střelu,
* přičteme skóre.

---

# 10. Shrnutí pro studenty

> ✔ Kolize = dotyk / překrytí dvou objektů.
> ✔ V Pygame je každý objekt reprezentován `rect`.
> ✔ Kolize obdélníků = `rect.colliderect()`.
> ✔ Sprite Group umí hromadné kolize (`spritecollide`, `groupcollide`).
> ✔ Po kolizi vždy rozhodujeme: odraz? zničení? poškození? sběr předmětu?
> ✔ Nejčastější problém: příliš rychlé objekty → „proletí“.
> ✔ Vektorová matematika pomáhá při odrazech a posunech.


