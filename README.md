# 🐍 SNAKE AI

<picture>
  <source
    media="(prefers-color-scheme: dark)"
    srcset="https://raw.githubusercontent.com/platane/snk/output/github-contribution-grid-snake-dark.svg"
  />
  <source
    media="(prefers-color-scheme: light)"
    srcset="https://raw.githubusercontent.com/platane/snk/output/github-contribution-grid-snake.svg"
  />
  <img
    alt="github contribution grid snake animation"
    src="https://raw.githubusercontent.com/platane/snk/output/github-contribution-grid-snake.svg"
  />
</picture>

## 🎯 Cíl projektu

Cílem tohoto projektu je vytvořit **AI hada**, který **sám dokončí hru** tím, že zaplní celé hrací pole, aniž
by narazil do sebe nebo do stěn. AI se bude snažit najít **co nejoptimálnější cestu** k jablku a zároveň přežít co
nejdéle.

## 🧠 Jak to funguje

Had se pohybuje na základě pokročilých **algoritmů pro hledání cest**, které mu umožní efektivně navigovat po hrací
ploše. AI bude průběžně vyhodnocovat situaci a volit nejlepší strategii.

## 🏆 Použité algoritmy

- **A* algoritmus** 🟢 – Hledá nejkratší cestu z bodu A do bodu B a optimalizuje pohyb.
- **Hamiltonovská kružnice** 🔵 – Snaží se vytvořit cestu, která navštíví každé pole právě jednou a vrátí se na start.
- **Další algoritmy** 🟠 – Experimentování s různými přístupy pro optimalizaci výkonu.

## 🛠️ Použité technologie

- **Krajta** 🐍
- **Pygame** 🎮
- **Algoritmy pro hledání cest** 📍

## 🚀 Jak spustit projekt na svém počítači

Tento návod vám ukáže, jak si tento projekt snadno spustíte na vašem počítači. Stačí postupovat podle následujících
kroků.

### 🛠️ Požadavky

Nejdříve si ověřte, že máte nainstalovaný **Python 3.7+**. Pokud ne, stáhněte si ho z oficiálních
stránek: [Stáhnout Python](https://www.python.org/downloads/).

### 1️⃣ Klonování repozitáře

Klonujte tento repozitář do vašeho počítače a přejděte do složky projektu:

```bash
git clone https://github.com/gyarab/2024-4e-merkulov-SnakeAI.git
cd 2024-4e-merkulov-SnakeAI
```

### 2️⃣ Vytvoření virtuálního prostředí

Vytvořte a aktivujte virtuální prostředí. To vám umožní izolovat závislosti pro tento projekt:

**Na Linuxu nebo macOS:**

```shell
python3 -m venv .venv
source .venv/bin/activate
```

**Na Windows:**

```shell
python3 -m venv .venv
source .venv\Scripts\activate
```

### 3️⃣ Instalace knihoven

Po aktivaci virtuálního prostředí nainstalujte všechny potřebné knihovny pomocí:

```shell
pip install -r requirements.txt
```

### 4️⃣ Spuštění hry

Jakmile máte všechny potřebné knihovny nainstalované, můžete hru spustit jednoduše tímto příkazem:

**Na Linux nebo macOS**

```shell
python3 snake_game.py
```

**Na Windows**

```shell
python snake_game.py
```
