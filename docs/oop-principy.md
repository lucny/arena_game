# 🧠 Co je OOP (Object-Oriented Programming)?

**OOP = programování orientované na objekty.**
Objekt = „věc“, která má **vlastnosti** a **chování**.

Například:

* hráč ve hře má *pozici, rychlost, životy* (vlastnosti)
* umí *pohybovat se, skákat, střílet* (chování)

Python umožňuje tvořit vlastní typy objektů pomocí **tříd (class)**.

---

# 🧩 1. Zapouzdření (Encapsulation)

### 📌 Definice

**Zapouzdření znamená, že data a funkce, které s těmito daty pracují, patří k sobě a tvoří jeden celek – objekt.**

Třída obsahuje:

* data (atributy)
* metody (funkce patřící objektu)

Díky zapouzdření:

* víme, kde co patří,
* kód je přehlednější,
* chování objektu je „uzamčeno“ uvnitř něj.

---

## 🧱 Příklad: Auto jako objekt

```python
class Car:
    def __init__(self):
        self.speed = 0  # vlastnost

    def accelerate(self):
        self.speed += 10  # chování

    def brake(self):
        self.speed = max(0, self.speed - 10)
```

### Co je zapouzdřeno?

* **rychlost auta** je chráněná uvnitř objektu,
* **akcelerace** i **brzdění** se provádí metodami auta,
* ostatní části programu nemusí vědět „jak přesně auto zrychluje“.

Objekt se stará sám o sebe → zjednodušuje zbytek programu.

---

## ⚠️ V Pythonu neexistují „skutečně soukromé“ atributy

Ale existuje konvence:

* `_atribut` = „interní, neměl by se používat zvenčí“
* `__atribut` = silnější ochrana (name mangling)

Například:

```python
class BankAccount:
    def __init__(self):
        self.__balance = 0  # soukromé

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance
```

---

# 🧬 2. Dědičnost (Inheritance)

### 📌 Definice

**Dědičnost umožňuje vytvářet nové třídy založené na třídách existujících.**

Nová třída:

* dědí vlastnosti a metody rodičovské třídy,
* může je rozšířit nebo změnit.

Je to princip **„je to druh / is-a“**.

---

## 🧱 Příklad: Třída Animal → Dog

```python
class Animal:
    def eat(self):
        print("Animal is eating")

class Dog(Animal):
    def bark(self):
        print("Woof!")
```

* `Dog` dědí metodu `eat()`.
* `Dog` přidává svou vlastní metodu `bark()`.

Použití:

```python
rex = Dog()
rex.eat()   # zděděno
rex.bark()  # vlastní metoda
```

---

## 🏗️ Přepis metody (override)

Potomek může přepsat metodu rodiče:

```python
class Cat(Animal):
    def eat(self):
        print("Cat eats quietly.")
```

Použití:

```python
cat = Cat()
cat.eat()  # zavolá se přepsaná verze
```

---

## 🚀 Použití super()

Když chceme použít původní logiku rodiče:

```python
class Dog(Animal):
    def eat(self):
        super().eat()
        print("Dog eats loudly.")
```

---

# 🌀 3. Polymorfismus (Polymorphism)

### 📌 Definice

**Polymorfismus = různé objekty mohou reagovat na stejnou metodu každý trochu jinak.**

Jinými slovy:

> Voláme stejnou metodu, ale výsledek závisí na tom, jaké objekty ji implementují.

---

## 🧱 Příklad: Tři zvířata, tři různé zvuky

```python
class Animal:
    def sound(self):
        pass

class Dog(Animal):
    def sound(self):
        return "Woof!"

class Cat(Animal):
    def sound(self):
        return "Meow!"

class Cow(Animal):
    def sound(self):
        return "Moo!"
```

Použití:

```python
animals = [Dog(), Cat(), Cow()]

for animal in animals:
    print(animal.sound())
```

Výstup:

```
Woof!
Meow!
Moo!
```

### 🔍 Všude se volá `sound()`, ale chování závisí na typu objektu.

To je **polymorfismus**.

---

## 🟦 Polymorfismus v Pygame – krásný příklad

V herní smyčce:

```python
all_sprites.update(dt)
```

Pygame volá `update(dt)` pro všechny objekty:

* Player.update()
* Enemy.update()
* Bullet.update()

Každý z nich dělá něco jiného, ale **hra se o jejich konkrétní chování nestará**.

---

# 🧩 4. Jak principy spolu souvisí

| Princip       | Otázka                        | Vysvětlení                                            |
| ------------- | ----------------------------- | ----------------------------------------------------- |
| Zapouzdření   | **Co objekt obsahuje?**       | Data + metody jsou pohromadě.                         |
| Dědičnost     | **Co mají objekty společné?** | Společné části jsou v rodiči, odlišnosti v potomcích. |
| Polymorfismus | **Jak se objekty liší?**      | Každý reaguje na stejnou metodu jinak.                |

Tyto principy dohromady tvoří **flexibilní a přehlednou architekturu**.

---

# 🌟 5. Shrnutí pro studenty

### 🔹 **Zapouzdření**

Objekt si nese vlastní data a metody.
Nemusíme řídit vše zvenčí → objekt „se stará sám o sebe“.

### 🔹 **Dědičnost**

Když dvě třídy sdílejí vlastnosti, vytvoříme rodiče.
Potomci dědí a rozšiřují.

### 🔹 **Polymorfismus**

Voláme stejnou metodu, ale každý objekt ji provede po svém.
Např. `sprite.update()` u hráče, střely i nepřítele.

