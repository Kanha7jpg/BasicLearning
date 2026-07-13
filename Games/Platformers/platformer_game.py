"""A small side-scrolling platformer built with tkinter.

Controls:
- Left / Right arrows or A / D to move
- Space or Up arrow to jump
- R to restart the current level

Goal:
Collect every gem, avoid traps, and reach the exit door to advance.
"""

from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from typing import Iterable


WIDTH = 900
HEIGHT = 600
GROUND_FALL_LIMIT = HEIGHT + 120
TICK_MS = 16
GRAVITY = 0.7
MOVE_ACCEL = 0.8
MAX_SPEED_X = 6.0
JUMP_SPEED = 14.0
FRICTION = 0.82
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 42
PLAYER_START_LIVES = 3


@dataclass(frozen=True)
class RectSpec:
    x1: int
    y1: int
    x2: int
    y2: int


@dataclass(frozen=True)
class ItemSpec:
    x: int
    y: int
    r: int = 10


@dataclass(frozen=True)
class LevelSpec:
    name: str
    start: tuple[int, int]
    platforms: tuple[RectSpec, ...]
    traps: tuple[RectSpec, ...]
    items: tuple[ItemSpec, ...]
    exit_door: RectSpec
    hint: str


LEVELS: tuple[LevelSpec, ...] = (
    LevelSpec(
        name="Level 1: Training Grounds",
        start=(70, 470),
        platforms=(
            RectSpec(0, 520, 900, 600),
            RectSpec(140, 440, 300, 470),
            RectSpec(360, 380, 540, 410),
            RectSpec(610, 320, 770, 350),
        ),
        traps=(
            RectSpec(250, 500, 300, 520),
            RectSpec(500, 500, 560, 520),
        ),
        items=(
            ItemSpec(200, 410),
            ItemSpec(430, 350),
            ItemSpec(670, 290),
        ),
        exit_door=RectSpec(820, 260, 860, 320),
        hint="Collect all gems, then reach the glowing door.",
    ),
    LevelSpec(
        name="Level 2: Broken Bridge",
        start=(60, 470),
        platforms=(
            RectSpec(0, 520, 900, 600),
            RectSpec(90, 460, 210, 490),
            RectSpec(260, 410, 390, 440),
            RectSpec(440, 350, 580, 380),
            RectSpec(630, 290, 760, 320),
            RectSpec(770, 220, 900, 250),
        ),
        traps=(
            RectSpec(165, 500, 235, 520),
            RectSpec(335, 500, 405, 520),
            RectSpec(520, 500, 610, 520),
            RectSpec(705, 500, 780, 520),
        ),
        items=(
            ItemSpec(140, 420),
            ItemSpec(330, 370),
            ItemSpec(500, 310),
            ItemSpec(700, 250),
        ),
        exit_door=RectSpec(840, 170, 880, 230),
        hint="Use the higher platforms to bypass the spike pits.",
    ),
    LevelSpec(
        name="Level 3: Trap Tower",
        start=(70, 470),
        platforms=(
            RectSpec(0, 520, 900, 600),
            RectSpec(110, 470, 240, 500),
            RectSpec(280, 420, 420, 450),
            RectSpec(460, 370, 600, 400),
            RectSpec(640, 320, 780, 350),
            RectSpec(300, 250, 470, 280),
            RectSpec(560, 200, 760, 230),
        ),
        traps=(
            RectSpec(180, 500, 250, 520),
            RectSpec(365, 500, 455, 520),
            RectSpec(525, 500, 615, 520),
            RectSpec(720, 500, 800, 520),
            RectSpec(400, 230, 500, 250),
        ),
        items=(
            ItemSpec(155, 430),
            ItemSpec(345, 380),
            ItemSpec(515, 330),
            ItemSpec(685, 280),
            ItemSpec(640, 160),
        ),
        exit_door=RectSpec(830, 120, 870, 180),
        hint="The last climb rewards careful jumps and timing.",
    ),
)


class PlatformerGame:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Platformer Levels")
        self.root.resizable(False, False)
        self.root.configure(bg="#12151d")

        self.canvas = tk.Canvas(
            self.root,
            width=WIDTH,
            height=HEIGHT,
            bg="#0f1420",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.keys: set[str] = set()
        self.level_index = 0
        self.lives = PLAYER_START_LIVES
        self.score = 0
        self.message_until = 0
        self.message_text = ""

        self.player_x = 0.0
        self.player_y = 0.0
        self.player_vx = 0.0
        self.player_vy = 0.0
        self.on_ground = False

        self.platform_items: list[int] = []
        self.trap_items: list[int] = []
        self.collectible_items: list[tuple[int, int, int]] = []
        self.exit_item: int | None = None
        self.exit_unlocked = False
        self.level_complete = False
        self.current_level = LEVELS[0]

        self.hud = self.canvas.create_text(
            16,
            14,
            anchor="w",
            fill="#eef2ff",
            font=("Arial", 14, "bold"),
            text="",
        )
        self.subhud = self.canvas.create_text(
            16,
            36,
            anchor="w",
            fill="#94a3b8",
            font=("Arial", 11),
            text="",
        )
        self.message = self.canvas.create_text(
            WIDTH // 2,
            56,
            fill="#f8fafc",
            font=("Arial", 16, "bold"),
            text="",
        )

        self.player_item = self.canvas.create_rectangle(0, 0, 0, 0, fill="#38bdf8", outline="")

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)

        self.load_level(0)
        self.loop()

    def on_key_press(self, event: tk.Event) -> None:
        key = event.keysym.lower()
        self.keys.add(key)
        if key == "r":
            self.restart_current_level()

    def on_key_release(self, event: tk.Event) -> None:
        self.keys.discard(event.keysym.lower())

    def load_level(self, index: int) -> None:
        self.level_index = index
        self.current_level = LEVELS[index]
        self.canvas.delete("level")
        self.platform_items.clear()
        self.trap_items.clear()
        self.collectible_items.clear()
        self.exit_item = None
        self.exit_unlocked = False
        self.level_complete = False

        self.player_x, self.player_y = self.current_level.start
        self.player_vx = 0.0
        self.player_vy = 0.0
        self.on_ground = False

        self.draw_level()
        self.render_player()
        self.set_message(self.current_level.hint, duration=2200)

    def draw_level(self) -> None:
        self.canvas.delete("level")
        self.platform_items = [self.create_platform(spec) for spec in self.current_level.platforms]
        self.trap_items = [self.create_trap(spec) for spec in self.current_level.traps]
        self.collectible_items = [self.create_collectible(item) for item in self.current_level.items]
        self.exit_item = self.create_exit(self.current_level.exit_door)
        self.draw_background()

    def draw_background(self) -> None:
        for y in range(0, HEIGHT, 24):
            shade = "#101827" if (y // 24) % 2 == 0 else "#0f1623"
            self.canvas.create_rectangle(0, y, WIDTH, y + 24, fill=shade, outline="", tags="level")

        for x in range(0, WIDTH, 90):
            self.canvas.create_line(x, 0, x - 50, HEIGHT, fill="#172033", width=1, tags="level")

        self.canvas.create_rectangle(0, HEIGHT - 42, WIDTH, HEIGHT, fill="#1f2937", outline="", tags="level")

    def create_platform(self, spec: RectSpec) -> int:
        if spec.y2 >= HEIGHT - 1:
            color = "#334155"
        else:
            color = "#475569"
        return self.canvas.create_rectangle(
            spec.x1,
            spec.y1,
            spec.x2,
            spec.y2,
            fill=color,
            outline="#94a3b8",
            width=2,
            tags="level",
        )

    def create_trap(self, spec: RectSpec) -> int:
        return self.canvas.create_rectangle(
            spec.x1,
            spec.y1,
            spec.x2,
            spec.y2,
            fill="#ef4444",
            outline="#fecaca",
            width=1,
            tags="level",
        )

    def create_collectible(self, item: ItemSpec) -> tuple[int, int, int]:
        oid = self.canvas.create_oval(
            item.x - item.r,
            item.y - item.r,
            item.x + item.r,
            item.y + item.r,
            fill="#fbbf24",
            outline="#fef08a",
            width=2,
            tags="level",
        )
        spark = self.canvas.create_text(
            item.x,
            item.y - 18,
            text="✦",
            fill="#fde68a",
            font=("Arial", 12, "bold"),
            tags="level",
        )
        return oid, spark, item.r

    def create_exit(self, spec: RectSpec) -> int:
        return self.canvas.create_rectangle(
            spec.x1,
            spec.y1,
            spec.x2,
            spec.y2,
            fill="#4ade80" if self.exit_unlocked else "#334155",
            outline="#bbf7d0" if self.exit_unlocked else "#64748b",
            width=3,
            tags="level",
        )

    def set_message(self, text: str, duration: int = 1600) -> None:
        self.message_text = text
        self.message_until = self.root.winfo_exists() and self.root.after(duration, self.clear_message)
        self.canvas.itemconfigure(self.message, text=text)

    def clear_message(self) -> None:
        self.message_text = ""
        self.canvas.itemconfigure(self.message, text="")

    def restart_current_level(self) -> None:
        self.set_message("Level restarted.", duration=1000)
        self.load_level(self.level_index)

    def advance_level(self) -> None:
        if self.level_index + 1 < len(LEVELS):
            self.score += 100
            self.set_message(f"{self.current_level.name} cleared!", duration=1500)
            self.load_level(self.level_index + 1)
        else:
            self.level_complete = True
            self.set_message("You beat every level. Press R to play again.", duration=0)

    def lose_life(self, reason: str) -> None:
        self.lives -= 1
        if self.lives <= 0:
            self.set_message(f"{reason} Game over. Press R to restart.", duration=0)
            self.load_level(0)
            self.lives = PLAYER_START_LIVES
            self.score = 0
            return
        self.set_message(f"{reason} Lives left: {self.lives}", duration=1200)
        self.player_x, self.player_y = self.current_level.start
        self.player_vx = 0.0
        self.player_vy = 0.0
        self.on_ground = False

    def player_bounds(self) -> tuple[float, float, float, float]:
        return (
            self.player_x,
            self.player_y,
            self.player_x + PLAYER_WIDTH,
            self.player_y + PLAYER_HEIGHT,
        )

    def render_player(self) -> None:
        self.canvas.coords(
            self.player_item,
            self.player_x,
            self.player_y,
            self.player_x + PLAYER_WIDTH,
            self.player_y + PLAYER_HEIGHT,
        )

    def update_hud(self) -> None:
        self.canvas.itemconfigure(
            self.hud,
            text=f"{self.current_level.name}   Score: {self.score}   Lives: {self.lives}",
        )
        remaining = self.collectible_count()
        self.canvas.itemconfigure(
            self.subhud,
            text=f"Collectibles left: {remaining}   Move: A/D or arrows   Jump: Space or Up   Restart: R",
        )

    def collectible_count(self) -> int:
        count = 0
        for oid, spark, radius in self.collectible_items:
            if self.canvas.itemcget(oid, "state") != "hidden":
                count += 1
        return count

    def is_solid_platform(self, item_id: int) -> bool:
        return item_id in self.platform_items

    def move_player(self) -> None:
        if self.keys.intersection({"left", "a"}):
            self.player_vx -= MOVE_ACCEL
        if self.keys.intersection({"right", "d"}):
            self.player_vx += MOVE_ACCEL

        self.player_vx = max(-MAX_SPEED_X, min(MAX_SPEED_X, self.player_vx))
        self.player_vy += GRAVITY

        if self.on_ground and self.keys.intersection({"space", "up"}):
            self.player_vy = -JUMP_SPEED
            self.on_ground = False

        self.player_vx *= FRICTION if self.on_ground else 0.98

        dx = self.player_vx
        dy = self.player_vy

        self.resolve_horizontal(dx)
        self.resolve_vertical(dy)

    def resolve_horizontal(self, dx: float) -> None:
        self.player_x += dx
        player_rect = self.player_bounds()
        for platform in self.platform_items:
            if self.rectangles_overlap(player_rect, self.canvas.coords(platform)):
                platform_rect = self.canvas.coords(platform)
                if dx > 0:
                    self.player_x = platform_rect[0] - PLAYER_WIDTH
                elif dx < 0:
                    self.player_x = platform_rect[2]
                self.player_vx = 0.0
                player_rect = self.player_bounds()

        self.player_x = max(0, min(WIDTH - PLAYER_WIDTH, self.player_x))

    def resolve_vertical(self, dy: float) -> None:
        self.player_y += dy
        self.on_ground = False
        player_rect = self.player_bounds()
        for platform in self.platform_items:
            if self.rectangles_overlap(player_rect, self.canvas.coords(platform)):
                platform_rect = self.canvas.coords(platform)
                if dy > 0:
                    self.player_y = platform_rect[1] - PLAYER_HEIGHT
                    self.player_vy = 0.0
                    self.on_ground = True
                elif dy < 0:
                    self.player_y = platform_rect[3]
                    self.player_vy = 0.0
                player_rect = self.player_bounds()

        if self.player_y > GROUND_FALL_LIMIT:
            self.lose_life("You fell into the void.")

    def rectangles_overlap(self, a: Iterable[float], b: Iterable[float]) -> bool:
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1

    def handle_traps_and_items(self) -> None:
        player_rect = self.player_bounds()

        for trap in self.trap_items:
            if self.rectangles_overlap(player_rect, self.canvas.coords(trap)):
                self.lose_life("You hit a trap.")
                return

        remaining = 0
        for collectible_id, spark_id, _radius in self.collectible_items:
            if self.canvas.itemcget(collectible_id, "state") == "hidden":
                continue
            remaining += 1
            if self.rectangles_overlap(player_rect, self.canvas.coords(collectible_id)):
                self.canvas.itemconfigure(collectible_id, state="hidden")
                self.canvas.itemconfigure(spark_id, state="hidden")
                self.score += 25
                self.set_message("Gem collected!", duration=700)

        if remaining == 0 and not self.exit_unlocked:
            self.exit_unlocked = True
            if self.exit_item is not None:
                self.canvas.itemconfigure(self.exit_item, fill="#4ade80", outline="#bbf7d0")
            self.set_message("Exit unlocked!", duration=1000)

    def handle_exit(self) -> None:
        if self.exit_item is None or not self.exit_unlocked:
            return
        if self.rectangles_overlap(self.player_bounds(), self.canvas.coords(self.exit_item)):
            self.advance_level()

    def update_exit_visual(self) -> None:
        if self.exit_item is not None:
            fill = "#4ade80" if self.exit_unlocked else "#334155"
            outline = "#bbf7d0" if self.exit_unlocked else "#64748b"
            self.canvas.itemconfigure(self.exit_item, fill=fill, outline=outline)

    def loop(self) -> None:
        self.move_player()
        self.handle_traps_and_items()
        self.handle_exit()
        self.update_exit_visual()
        self.render_player()
        self.update_hud()
        self.root.after(TICK_MS, self.loop)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    PlatformerGame().run()
