# 👾 Space Invaders — Java Swing

A fully-featured, single-file Space Invaders clone built with **Java Swing**. No external libraries or dependencies required — just a JDK and you're ready to play.

---

## 🚀 Getting Started

### Prerequisites

- Java Development Kit (JDK) 8 or higher

Check your version:
```bash
java -version
```

### Compile & Run

```bash
javac SpaceInvaders.java
java SpaceInvaders
```

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| `←` / `A` | Move left |
| `→` / `D` | Move right |
| `Space` / `↑` | Shoot |
| `P` | Pause / Resume |
| `R` | Restart game |
| `N` | Next level *(after winning)* |

---

## 🕹️ Gameplay

- Destroy all **55 aliens** arranged in 5 rows of 11 to clear a level
- Aliens **speed up** as their numbers dwindle — don't get comfortable
- A **UFO** occasionally streaks across the top of the screen for bonus points
- Take cover behind **4 destructible shields** — they degrade block-by-block from both your bullets and alien bombs
- You have **3 lives**; lose them all and it's game over

### Scoring

| Target | Points |
|--------|--------|
| Bottom row alien | 10 × level |
| Middle row alien | 20 × level |
| Top row alien | 30–50 × level |
| UFO | 50–300 (random) |

---

## 🌊 Levels

Each new level resets the alien grid and shields but **increases difficulty**:

- Aliens start faster
- Alien bomb frequency increases
- UFO appears more often

Progress through levels by pressing `N` after clearing the board.

---

## 🏗️ Project Structure

```
SpaceInvaders.java   ← entire game in one file (~500 lines)
README.md
```

### Key Classes & Sections

| Section | Description |
|---------|-------------|
| Constants | Window size, speeds, dimensions |
| `initGame()` | Resets all state for a new game |
| `buildAliens()` | Spawns the 5×11 alien grid |
| `buildShields()` | Creates the 4 destructible shield bunkers |
| `actionPerformed()` | Main game loop (~62 fps via `javax.swing.Timer`) |
| `drawAlienShape()` | Pixel-art alien sprites with 2-frame animation |
| `checkCollisions()` | Bullet/bomb vs aliens, shields, player, UFO |
| `paintComponent()` | Full scene rendering |

---

## ✨ Features

- 🎨 **Pixel-art alien sprites** — three distinct shapes (squid, crab, octopus) with 2-frame walking animation
- 🌈 **5 alien colors** — each row is uniquely colored
- 🛸 **Animated UFO** with random score bonus and score flash on kill
- 🟩 **Destructible shields** with per-block damage and opacity decay
- 💥 **Zigzag bomb rendering** for alien projectiles
- ⭐ **Starfield background** for atmosphere
- 📈 **Dynamic alien speed** — ramps up as the board clears
- 🔁 **Multi-level progression** with scaling difficulty

---

## 📋 Requirements

- JDK 8+
- No external dependencies
- Works on Windows, macOS, and Linux

---

## 📄 License

Free to use and modify. Built for fun. 🚀