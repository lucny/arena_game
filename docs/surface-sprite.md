# 1. Co je to `Surface` v Pygame?

🔹 **`Surface` je v Pygame základní „plátno“ – obrázek, na který se kreslí.**
Může to být:

* celé **herní okno** (hlavní surface),
* **sprite hráče**,
* **pozadí**, tlačítko, text, ikona…

Každý obrázek v Pygame je nějaký `Surface`.

---

## 1.1 Vytvoření nového Surface

### a) Jednoduchý barevný čtverec

```python
import pygame

# vytvoření surface o velikosti 50x50 pixelů
square_surface = pygame.Surface((50, 50))

# vyplnění barvou (R,G,B)
square_surface.fill((255, 0, 0))  # červená
```

* `pygame.Surface((šířka, výška))` vytvoří prázdný obrázek.
* `fill((R,G,B))` ho celé vyplní barvou.

### b) Hlavní herní okno je také Surface

```python
screen = pygame.display.set_mode((800, 600))
```

Proměnná `screen` je taky `Surface`.
Rozdíl je jen v tom, že se vykresluje na obrazovku (je „zvláštní“ surface).

---

## 1.2 Kreslení na Surface a „blit“

Když chceme obrázek zobrazit na obrazovce, používáme:

```python
screen.blit(square_surface, (100, 100))
```

* `blit` = „otisknout jeden surface na jiný surface“.
* první argument: co kreslíme
* druhý argument: **kam** (x, y) na cílovém surface

Typický kus kódu v herní smyčce:

```python
screen.fill((0, 0, 0))               # vyčistit obrazovku (černá)
screen.blit(square_surface, (100, 100))
pygame.display.flip()                # aktualizovat okno
```

---

## 1.3 Načítání obrázků do Surface

Často nechceme jen barevný čtverec, ale skutečný obrázek (PNG, JPG…).

```python
image = pygame.image.load("player.png")
image = image.convert_alpha()   # optimalizace + zachování průhlednosti
```

* `load` vrátí Surface.
* `convert()` / `convert_alpha()` obrázek „přizpůsobí“ formátu obrazovky → rychlejší vykreslování.
* `convert_alpha()` zachová alfa kanál (průhlednost).

Pak ho vykreslíme:

```python
screen.blit(image, (x, y))
```

---

## 1.4 Průhlednost (alpha) a Surface

Na `Surface` můžeme nastavit:

* **průhlednou barvu** (colorkey),
* nebo **alfa kanál** (průhledné pixely v PNG).

### Colorkey:

```python
surface = pygame.Surface((50, 50))
surface.fill((255, 0, 255))           # růžová
surface.set_colorkey((255, 0, 255))   # tato barva bude průhledná
```

### Alfa kanál už je v PNG:

* obrázek má poloprůhledné pixely,
* použijeme `convert_alpha()` a máme průhledný sprite.

---

## 1.5 Shrnutí k Surface

* **Surface = obrázek / plátno** v paměti.
* Vytváří se `pygame.Surface((w, h))` nebo `pygame.image.load()`.
* Kreslí se na jiný surface (třeba `screen`) pomocí `blit`.
* Může mít barvu, texturu, průhlednost.
* Pygame prakticky pořád „jen“ kreslí Surface na Surface.

---

# 2. Co je to `Sprite` v Pygame?

`Surface` je jen obrázek.
Ale **hra potřebuje víc**: pozici, rychlost, kolize, logiku…

🔹 **`Sprite` je třída, která reprezentuje herní objekt** s nějakým chováním.
V Pygame se používá třída:

```python
pygame.sprite.Sprite
```

Když si vytvoříme vlastní třídu, která dědí z `Sprite`, dostaneme:

* možnost dát jí **image** (Surface),
* **rect** (obdélník pro pozici a kolize),
* možnost zařadit ji do **Group** (skupina spriteů),
* automatické volání `update()` u všech spriteů ve skupině
* jednodušší práci s kolizemi (`spritecollide`, `groupcollide`).

---

## 2.1 Základní vlastní Sprite

### Jednoduchý příklad – bílý čtverec, který nic nedělá:

```python
import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        
        # každý Sprite MUSÍ mít atribut image a rect
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 255))

        # rect určuje pozici a velikost na obrazovce
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        # sem přijde logika pohybu, animace, atd.
        pass
```

* `image` je `Surface` = jak objekt vypadá.
* `rect` říká, kde je na obrazovce.
* `update()` je metoda, kterou může volat herní smyčka (přes Group).

---

## 2.2 Sprite Groups – správa mnoha objektů najednou

Velká výhoda Pygame Sprite systému jsou **skupiny**:

```python
all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
```

Přidání objektu:

```python
block = Block((100, 100))
all_sprites.add(block)
blocks.add(block)
```

### V herní smyčce:

```python
all_sprites.update(dt)    # zavolá update(dt) u všech spriteů
all_sprites.draw(screen)  # vykreslí všechny sprite na screen
```

✅ **Tohle je klíčové:**
Nemusíme ručně volat `update()` pro každý objekt, stačí jednou na Group.

---

## 2.3 Kolize s pomocí Spriteů

Pygame nabízí funkce:

* `pygame.sprite.spritecollide(sprite, group, dokill)`
* `pygame.sprite.groupcollide(group1, group2, dokill1, dokill2)`

Příklad: střely vs. nepřátelé

```python
hits = pygame.sprite.spritecollide(bullet, enemies_group, dokill=True)
if hits:
    bullet.kill()   # odstranit střelu
```

Díky tomu:

* **nemusíme ručně procházet všechny dvojice objektů**,
* použití je jednoduché a přehledné.

---

# 3. Jak spolu souvisí `Surface` a `Sprite`?

📌 **Shrnutí vztahu:**

* `Surface` = „jak sprite vypadá“ (obrázek).
* `Sprite` = „objekt s chováním“, který obsahuje:

  * `image` (Surface),
  * `rect` (pozice a rozměr),
  * logiku v `update()`.

Typická třída sprite:

```python
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)

    def update(self, dt):
        # pohyb, vstupy, animace...
        pass
```

Tady je krásně vidět:

* **Surface (`image`) říká, jak to vypadá**,
* **Sprite + rect říká, kde to je a co to dělá**.

---

# 4. Jak jsme to použili v projektu „Arena Survival“

V naší arénové hře jsme udělali ještě jeden krok:

* vytvořili jsme **společného rodiče** `Entity`,
* ten dědí z `pygame.sprite.Sprite`,
* a **Player, Enemy, Bullet** dědí z `Entity`.

```python
class Entity(pygame.sprite.Sprite):
    def __init__(self, game, pos, size, color):
        super().__init__()
        self.game = game

        # Surface (jak objekt vypadá)
        self.image = pygame.Surface(size)
        self.image.fill(color)

        # rect + Vector2 pozice
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)

    def update(self, dt):
        pass
```

Díky tomu:

* máme **jedno místo**, kde řešíme `image`, `rect`, `pos`,
* potomci jen mění chování v `update()`.

---

# 5. Doporučené shrnutí pro studenty

Na závěr můžeš studentům dát krátké shrnutí:

> * **`Surface` = obrázek**.
>   Vytváří se `pygame.Surface()` nebo `pygame.image.load()`.
>   Kreslí se pomocí `blit()` na jiný Surface (např. `screen`).
>
> * **`Sprite` = herní objekt**.
>   Je to třída, která má `image` (Surface), `rect` (pozici) a metodu `update()`.
>   Vkládá se do `Group()`, která umí všechny sprite:
>
>   * hromadně `update()`
>   * hromadně `draw()`
>   * testovat kolize.
>
> * V praxi používáme obojí:
>   `Sprite` se stará o logiku, `Surface` o vzhled.

