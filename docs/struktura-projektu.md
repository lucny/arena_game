# **Struktura projektu a princip „Separation of Concerns“**

## 🧠 1. Co je Separation of Concerns (SoC)?

📌 **SoC = princip, podle kterého má každá část programu řešit jednu konkrétní věc.**

Jedna část → jedna odpovědnost.

Příklady z běžného života:

* mobilní telefon nemá vše na jedné obrazovce → aplikace jsou oddělené
* auto má motor, brzdy, volant → každá část dělá svou věc

Stejné je to v kódu.

---

## 🧩 2. Proč projekty nesmí být „v jednom souboru“

Když studenti začínají, často vytvoří:

* **1 soubor `main.py`**
* ve kterém je:

  * herní smyčka
  * pohyb hráče
  * správa kolizí
  * logika nepřátel
  * grafika
  * načítání assetů
  * vše ostatní

To vede k:

* nepřehlednosti
* opakovanému kódu
* chybám, které se těžko hledají
* nemožnosti projekt rozšířit

Separation of Concerns tomu zabrání.

---

## 🏛️ 3. Ideální projekt má vrstvy (moduly)

Každá část hry má být v **jiné části projektu**.

## Příklad vrstev:

1. **core** – úvodní soubor, který vše spouští
2. **game** – hlavní třída hry
3. **entities** – objekty hry (hráč, nepřítel, střela…)
4. **systems** – logika mimo objekty (spawner, fyzika, UI…)
5. **settings** – konfigurace projektu (konstanty)
6. **assets** – obrázky, zvuky

Takto oddělené části mají **jasný účel**.

---

## 📁 4. Ukázková struktura projektu (herní aréna)

```
arena_game/
│
├── main.py            ← start hry
├── game.py            ← hlavní smyčka, řízení hry
├── settings.py        ← konfigurace
│
├── entities/          ← všechno, co „existuje“ ve hře
│   ├── entity.py      
│   ├── player.py
│   ├── enemy.py
│   └── bullet.py
│
└── systems/           ← komponenty, které nejsou objekty hry
    └── spawner.py
```

Každý soubor má **jednu odpovědnost**.

---

## 🧩 5. Co patří do které části?

### 5.1 `main.py`

* inicializace Pygame
* vytvoření instance Game
* spuštění hry

*Nemá obsahovat herní logiku.*

---

### 5.2 `game.py`

* hlavní **herní smyčka**
* volání update a draw všech objektů
* správa skupin spriteů
* načítání levelů, skóre, menu
* komunikace mezi systémy a entitami

Třída game je **ředitel hry**.

---

### 5.3 `settings.py`

* šířka okna
* výštra okna
* rychlosti objektů
* barvy
* časové intervaly
* FPS

Proč je to dobré?

* nemusíme hledat čísla v kódu
* vše je na jednom místě
* studenti mohou snadno experimentovat

---

### 5.4 `entities/`

Sem patří objekty (sprite):

* Player
* Enemy
* Bullet
* cokoliv, co „je fyzicky v herním světě“

Každá entita:

* má **vzhled (Surface)**
* **pozici (rect + Vector2)**
* metodu **update()** – své chování
* nemá řídit hru jako celek

---

## 5.5 `entity.py`

Rodič předurčený pro dědičnost:

```python
class Entity(Sprite):
    image
    rect
    pos
    update()
```

To je krásná ukázka **zapouzdření** a **dědičnosti**.

---

## 5.6 `systems/`

Patří sem logické systémy:

* spawner nepřátel
* systém kolizí (pokud by byl složitý)
* systém dialogů
* správa UI

Tyto části **nejsou** objekty hry — nepatří do entities.

---

## ⚡ 6. Proč je separace concerns výhodná?

| Výhoda                  | Popis                                             |
| ----------------------- | ------------------------------------------------- |
| **Přehlednost**         | Každý soubor je krátký a jasný.                   |
| **Snadné hledání chyb** | Vím, kde hledat problém – podle účelu modulu.     |
| **Znovupoužitelnost**   | Třídy lze použít v jiných projektech.             |
| **Možnost rozšíření**   | Přidání nových funkcí je jednoduché (nový modul). |
| **Teamwork**            | Každý student může pracovat na jiné části.        |
| **Profesionální praxe** | Velké hry a aplikace používají přesně tento styl. |

---

## 🧠 7. Přehled příkladů podle Separation of Concerns

### ❌ Špatně (vše v jednom souboru):

```python
# stovky řádků:
player_x += 5
enemy_ai()
spawn_enemy()
draw_enemy()
update_bullets()
check_collision()
```

* chaos
* obtížné rozšiřování
* neorientovatelný kód

---

### ✔ Správně (rozdělení):

**game.py**

```python
self.player.update(dt)
self.spawner.update(dt)
self.all_sprites.update(dt)
```

**player.py**

```python
def update(self, dt):
    self.handle_input(dt)
```

**spawner.py**

```python
def update(self, dt):
    if time > interval:
        create_enemy()
```

---

## 📘 8. Shrnutí pro studenty

> **Separation of Concerns = každá část programu řeší JEN svou věc.**
>
> Hra není jeden velký soubor, ale mozaika jednoduchých částí:
>
> * `main.py` = start hry
> * `game.py` = herní smyčka a řízení
> * `entities/` = objekty hry
> * `systems/` = logika mimo objekty
> * `settings.py` = konfigurace
>
> Díky tomu je projekt čistý, přehledný a profesionální.
