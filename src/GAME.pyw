import pygame
import os
import sys

pygame.init()

# --- Параметри екрану та блоків ---
BLOCKS_X = 40
BLOCKS_Y = 20

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

BLOCK_SIZE = min(screen_width // BLOCKS_X, screen_height // BLOCKS_Y)

screen = pygame.display.set_mode((BLOCKS_X * BLOCK_SIZE, BLOCKS_Y * BLOCK_SIZE), pygame.RESIZABLE)
pygame.display.set_caption("Minethon2D - Ламання блоків")
clock = pygame.time.Clock()

# --- Функція завантаження зображень ---
def load_block(name):
    """Завантажує текстуру блоку з assets/blocks/"""
    path = os.path.join("assets", "blocks", f"{name}.png")
    if not os.path.exists(path):
        print(f"[ERROR] Блок '{name}' не знайдено у {path}")
        sys.exit(1)
    return pygame.image.load(path).convert_alpha()

# --- Завантаження блоків із локальних файлів ---
block_names = ["grass", "dirt", "stone"]
blocks_original = {}
blocks_scaled = {}

for name in block_names:
    img = load_block(name)
    blocks_original[name] = img
    blocks_scaled[name] = pygame.transform.scale(img, (BLOCK_SIZE, BLOCK_SIZE))
    print(f"[INFO] Завантажено {name}.png")

# --- Створюємо карту з блоками та унікальним ID ---
map_layout = []
current_id = 1
for y in range(BLOCKS_Y):
    row = []
    for x in range(BLOCKS_X):
        if y == BLOCKS_Y - 5:
            row.append({"id": current_id, "name": "grass"})
        elif y > BLOCKS_Y - 5:
            row.append({"id": current_id, "name": "dirt"})
        else:
            row.append("air")
        current_id += 1
    map_layout.append(row)

# --- Функція для оновлення розміру блоків ---
def recalc_block_size():
    global BLOCK_SIZE
    new_w, new_h = pygame.display.get_window_size()
    block_w = new_w / BLOCKS_X
    block_h = new_h / BLOCKS_Y
    new_size = int(min(block_w, block_h))

    if new_size != BLOCK_SIZE:
        BLOCK_SIZE = new_size
        for name in blocks_original:
            blocks_scaled[name] = pygame.transform.scale(blocks_original[name], (BLOCK_SIZE, BLOCK_SIZE))
        print(f"[INFO] BLOCK_SIZE: {BLOCK_SIZE}, window: {new_w}x{new_h}")

# --- Основний цикл ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            block_x = mouse_x // BLOCK_SIZE
            block_y = mouse_y // BLOCK_SIZE

            if 0 <= block_x < BLOCKS_X and 0 <= block_y < BLOCKS_Y:
                if event.button == 1:  # ліва кнопка = ламаємо
                    block = map_layout[block_y][block_x]
                    if isinstance(block, dict):
                        print(f"Зламали блок ID={block['id']}, name={block['name']}")
                        map_layout[block_y][block_x] = "air"

                elif event.button == 3:  # права кнопка = ставимо grass
                    block = map_layout[block_y][block_x]
                    if block == "air":
                        new_id = max(
                            (b["id"] for row in map_layout for b in row if isinstance(b, dict)),
                            default=0
                        ) + 1
                        map_layout[block_y][block_x] = {"id": new_id, "name": "grass"}

    recalc_block_size()

    screen.fill((120, 180, 255))  # фон неба

    for y in range(BLOCKS_Y):
        for x in range(BLOCKS_X):
            block = map_layout[y][x]
            if isinstance(block, dict):
                screen.blit(blocks_scaled[block["name"]], (x * BLOCK_SIZE, y * BLOCK_SIZE))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
