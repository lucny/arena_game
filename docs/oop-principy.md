# 🧠 Co je OOP (Object-Oriented Programming)?

**OOP = programování orientované na objekty.**
Objekt = „věc“, která má **vlastnosti** a **chování**.

Například:

* hráč ve hře má *pozici, rychlost, životy* (vlastnosti)
* umí *pohybovat se, skákat, střílet* (chování)

Python umožňuje tvořit vlastní typy objektů pomocí **tříd (class)**.

---
## 🏗️ Třídy

**Třída** je jako šablona pro vytváření objektů. 
* Obsahuje atributy a metody.
* Základní metodou je `__init__()`, která inicializuje nový objekt. Nazýváme se **konstruktorem**.
* Objekt je konkrétní **instance třídy**. Vzniká voláním konstruktoru, např. `player = Player()`.
* Klíčové slovo `self` odkazuje na aktuální instanci objektu uvnitř metod třídy (je to jako „já“ pro objekt, v jiných jazycích se používá `this`).
* Atributy jsou proměnné uvnitř třídy, které uchovávají data objektu. Atributy se obvykle definují v metodě `__init__()` a přistupuje se k nim pomocí `self.atribut`.
* Metody jsou funkce definované uvnitř třídy, které pracují s daty objektu. Metody se volají pomocí `self.metoda()`.
* Prvním parametrem každé metody musí být `self`, aby metoda věděla, ke kterému objektu se vztahuje.

Podrobnější informace: [https://https://docs.python.org/3/tutorial/classes.html](https://https://docs.python.org/3/tutorial/classes.html)

---

### FAQ

**Proč používat třídy?**
* Umožňují organizovat kód kolem objektů, což zlepšuje čitelnost a údržbu.
* Podporují OOP principy jako zapouzdření, dědičnost a polymorfismus.
* Usnadňují opětovné použití kódu.

**Proč je `__init__` speciální metoda?**
* `__init__` je konstruktor, který se automaticky volá při vytvoření nové instance třídy.
* Slouží k inicializaci atributů objektu.

**Proč je nutné používat `self`?**
* `self` umožňuje metodám přístup k atributům a dalším metodám objektu.
* Bez `self` by metody nevěděly, ke kterému objektu se vztahují.

**Proč je v Pythonu `self` první parametr metod?**
* Je to konvence v Pythonu, která zvyšuje čitelnost kódu.
* Umožňuje explicitní přístup k instanci objektu.

---

## 🧩 Zapouzdření (Encapsulation)

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

### 🧱 Příklad: Auto jako objekt

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

### ⚠️ V Pythonu neexistují „skutečně soukromé“ atributy

Ale existuje konvence, které využívají podtržítka:

* `_atribut` = „interní, neměl by se používat zvenčí“, jedná se ale jen o dohodu bez skutečné ochrany,
* `__atribut` = silnější ochrana (name mangling), která ztěžuje přístup zvenčí (ale stále je to možné).

Například:

```python
class BankAccount:
    def __init__(self):
        self._balance = 0  # soukromé

    def deposit(self, amount):
        self._balance += amount

    def get_balance(self):
        return self._balance
```

---

### FAQ

**Kdy použít soukromé atributy?**
* Když chcete zabránit přímé manipulaci s daty zvenčí. Například v případě naší hry by to mohlo být užitečné pro atributy jako `health` nebo `score`, aby se předešlo nechtěným změnám.

**Proč neudělat všechny atributy soukromé?**
* Někdy je potřeba přístup zvenčí (např. pro čtení hodnoty).
* Může to zbytečně komplikovat kód.

**Jak přistupovat k soukromým atributům?**
* Pomocí veřejných metod (gettery/settery) definovaných ve třídě.
* Například `get_balance()` v našem příkladu.

**Je vhodné používat soukromé atributy v malých projektech?**
* V malých projektech to není vždy nutné, ale je dobré si na to zvyknout pro větší projekty, kde je důležitá struktura a ochrana dat.

**Jaký je rozdíl mezi `_atribut` a `__atribut`?**
* `_atribut` je pouze konvence, zatímco `__atribut` využívá name mangling pro silnější ochranu.
* Použití `__atribut` může být užitečné, pokud chcete opravdu zabránit přístupu zvenčí, ale mějte na paměti, že to může ztížit ladění a údržbu kódu.

---

## 🧬 Dědičnost (Inheritance)

### 📌 Definice

**Dědičnost umožňuje vytvářet nové třídy založené na třídách existujících.**

Nová třída:

* dědí vlastnosti a metody rodičovské třídy,
* může je rozšířit nebo změnit.

Je to princip **„je to druh / is-a“**.

---

### 🧱 Příklad: Třída Animal → Dog

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

### 🏗️ Přepis metody (override)

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

### 🚀 Použití super()

Když chceme použít původní logiku rodiče:

```python
class Dog(Animal):
    def eat(self):
        super().eat()
        print("Dog eats loudly.")
```

---
### FAQ

**Proč používat dědičnost?**
* Umožňuje opětovné použití kódu.
* Umožňuje vytvářet hierarchie tříd, což zlepšuje organizaci kódu.
* Umožňuje polymorfismus (více o tom později).

**Kdy použít dědičnost?**
* Když máte třídy, které sdílejí společné vlastnosti a chování. Například v naší hře mohou mít všechny postavy společné metody jako `update()` nebo `draw()`, které mohou být definovány v rodičovské třídě `Entity`.

**Proč používat super() a nepřistupovat přímo k metodám rodiče?**
* `super()` zajišťuje správné volání metod v hierarchii dědičnosti, což je důležité zejména při více dědičnosti.
* Zvyšuje čitelnost kódu a usnadňuje údržbu.
* Pomáhá předcházet chybám, pokud se změní struktura dědičnosti.

**Může třída dědit od více tříd?**
* Ano, Python podporuje více dědičnost, ale je třeba být opatrný, aby nedošlo k nejasnostem v hierarchii tříd.
* Vícenásobná dědičnost může vést k problémům s údržbou kódu, pokud není správně spravována.

**Má každá třída rodiče?**
* Ano, v Pythonu každá třída implicitně dědí od třídy `object`, pokud není specifikován jiný rodič.
* To znamená, že i třídy bez explicitního rodiče mají základní vlastnosti a metody zděděné od `object`.
* Dědičnost od `object` poskytuje základní funkce, jako je například metoda `__str__()` pro reprezentaci objektu jako řetězce.

---

## 🌀 Polymorfismus (Polymorphism)

### 📌 Definice

**Polymorfismus = různé objekty mohou reagovat na stejnou metodu každý trochu jinak.**

Jinými slovy:

> Voláme stejnou metodu, ale výsledek závisí na tom, jaké objekty ji implementují.

---

### 🧱 Příklad: Tři zvířata, tři různé zvuky

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

### 🟦 Polymorfismus v Pygame – krásný příklad

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

### FAQ

**Proč je polymorfismus užitečný?**
* Umožňuje psát flexibilní a rozšiřitelný kód.
* Umožňuje pracovat s různými objekty jednotným způsobem.
* Zjednodušuje správu kódu v komplexních systémech, jako jsou hry.

**Kdy použít polymorfismus?**
* Když máte různé třídy, které sdílejí společné metody, ale implementují je různými způsoby. Například v naší hře mohou mít všechny herní objekty metodu `update()`, ale každý objekt ji implementuje podle svých potřeb (hráč se pohybuje, nepřítel útočí, střela letí).

**Jak polymorfismus souvisí s dědičností?**
* Polymorfismus často využívá dědičnost, protože umožňuje různým třídám sdílet společné metody definované v rodičovské třídě.
* Díky dědičnosti mohou různé třídy implementovat stejné metody, což umožňuje polymorfní chování.

**Může polymorfismus existovat bez dědičnosti?**
* Ano, v Pythonu může polymorfismus existovat i bez dědičnosti díky dynamickému typování. Různé objekty mohou mít metody se stejným názvem, aniž by sdílely společného předka.
* Nicméně, dědičnost často usnadňuje implementaci polymorfismu a zlepšuje organizaci kódu.

---

## 🧩 4. Jak principy spolu souvisí

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

