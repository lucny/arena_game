# 🎮 1. Co je to herní smyčka (Game Loop)

Každá počítačová hra — ať je to Mario, Minecraft nebo malá arénovka v Pygame — běží uvnitř **nekonečné smyčky**, která:

1. **zpracuje vstupy od hráče**,
2. **aktualizuje stav hry**,
3. **vykreslí scénu na obrazovku**,
4. **a znovu se opakuje**.

Tato smyčka běží desítky až stovky krát za sekundu.
U Pygamea typicky **60× za sekundu**.

### Proč je to potřeba?

Protože svět hry se neustále mění:

* hráč mačká klávesy,
* nepřátelé se hýbou,
* střely letí,
* časové akce probíhají,
* obraz se musí stále obnovovat.

Bez smyčky by hra zobrazila jen jeden obrázek a zůstala statická.

---

# 🔁 2. Jak vypadá základní herní smyčka v Pygame

V praxi Pygame Game Loop vypadá takto:

```python
running = True
while running:
    # 1. Události (klávesnice, myš, zavření okna)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Aktualizace stavu hry
    update()

    # 3. Vykreslení
    draw()

    pygame.display.flip()
```

A teď si pojďme vysvětlit všechny části.

---

# 🔥 3. Část 1: Události (events)

## Co je událost?

Událost = něco, co se *stane mimo hru*, ale hra na to musí reagovat.

Například:

* hráč stiskne klávesu (`KEYDOWN`)
* hráč klávesu pustí (`KEYUP`)
* klikne myší (`MOUSEBUTTONDOWN`)
* pohne myší (`MOUSEMOTION`)
* zavře okno (`QUIT`)

Pygame všechny události ukládá do tzv. **event queue** (fronty událostí).

## Kde je vezmeme?

Jednoduše:

```python
for event in pygame.event.get():
    ...
```

Tím získáš **všechny události, které nastaly během posledního snímku**.

---

## Příklad: zavření okna

```python
if event.type == pygame.QUIT:
    running = False
```

Když klikneme na křížek v okně, Pygame vloží událost `QUIT` do fronty — a my na ni zareagujeme.

---

## Příklad: stisk klávesy

```python
if event.type == pygame.KEYDOWN:
    print("Stisknuto:", event.key)
```

**Není nutné říkat Pygame: „Poslouchej klávesnici“ — Pygame poslouchá automaticky.
My jen čteme, co se stalo.**

---

## Rozšířený příklad: klávesa ESC → ukončit hru

```python
if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_ESCAPE:
        running = False
```

---

# 🎯 4. Část 2: Aktualizace hry („update“)

Tady se hýbe *logika*.

Co typicky děláme:

* pohyb hráče podle kláves
* pohyb nepřátel
* střely → letí dopředu
* kolize → kontrola, zda se něco srazilo
* spawnování objektů
* počítání skóre nebo času

Například:

```python
player.update(dt)
enemies.update(dt)
bullets.update(dt)
```

Nebo elegantněji s Pygame Sprite Group:

```python
all_sprites.update(dt)
```

U každého objektu se zavolá jeho metoda `update()` → ukázka polymorfismu.

---

# 🎨 5. Část 3: Vykreslení („draw“)

Kreslíme vše v pořadí:

1. pozadí
2. hráče
3. nepřátele
4. střely
5. textové hlášky (HUD)

Typicky:

```python
screen.fill((0, 0, 0))       # vyčistit plátno
all_sprites.draw(screen)     # vykreslit objekty
pygame.display.flip()        # aktualizovat obrazovku
```

**Pozor:**

* `flip()` ZOBRAZÍ novou scénu najednou.
* Bez `flip()` by hráč nic neviděl.

---

# ⏱️ 6. FPS a čas (`dt` – delta time)

Aby pohyb ve hře nebyl závislý na výkonu počítače, používáme tzv. **delta time**:

```python
dt = clock.tick(60) / 1000
```

* `clock.tick(60)` dělá **přibližně 60 snímků za sekundu**
* vrací počet *milisekund* od posledního snímku
* vyděleno 1000 = sekundy (float)

Pak se pohyb počítá takto:

```python
player.pos += direction * speed * dt
```

Tím zajistíš:

🟢 Na rychlém PC – stále stejně
🟢 Na pomalém PC – stále stejně

To je moderní způsob řízení pohybu ve hrách.

---

# 🧠 7. Celkový přehled herní smyčky

Zjednodušeně:

```
+---------------------------+
| 1. Získej události        |
| 2. Aktualizuj stav hry    |
| 3. Nakresli scénu         |
+---------------------------+
| Opakuj ~60x za sekundu    |
+---------------------------+
```

To je „tlukoucí srdce“ každé hry.

---

# 🧩 8. Příklad kompletní smyčky (pro studenty)

```python
running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000

    # 1. ZPRACOVÁNÍ UDÁLOSTÍ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # 2. UPDATE
    player.update(dt)
    enemies.update(dt)
    bullets.update(dt)

    # 3. DRAW
    screen.fill((30, 30, 30))
    all_sprites.draw(screen)
    pygame.display.flip()
```

---

# ⭐ Shrnutí pro studenty

> Herní smyčka je nekonečný cyklus, který 60× za sekundu:
>
> 1. čte **události** (klávesnice, myš, zavření okna),
> 2. **aktualizuje** pozice, pohyb a logiku hry,
> 3. **vykresluje** novou scénu na obrazovku.

> Události jsou vstupy uživatele nebo systému: kliknutí myší, stisk klávesy, zavření okna.
> Získáváme je pomocí `pygame.event.get()`.

