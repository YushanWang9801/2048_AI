import pygame
import random
import sys
import os
from utils import *

pygame.init()


class Game2048:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2048")

        self.font = pygame.font.SysFont("Arial", FONT_SIZE, bold=True)
        self.small_font = pygame.font.SysFont("Arial", SMALL_FONT_SIZE, bold=True)
        self.large_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.prompt_font = pygame.font.SysFont("Arial", 12)

        self.score = 0
        self.best_score = 0
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.game_over = False
        self.won = False

        self.add_new_tile()
        self.add_new_tile()

        # Buttons
        self.restart_rect = pygame.Rect(WIDTH - 130, 100, 100, 40)
        self.continue_rect = pygame.Rect(WIDTH - 130, 160, 100, 40)

        # Try load button images
        self.restart_img = self.load_image("assets/restart.svg")
        self.continue_img = self.load_image("assets/continue.svg")

    def load_image(self, path):
        if os.path.exists(path):
            return pygame.transform.scale(pygame.image.load(path), (40, 40))
        return None

    def add_new_tile(self):
        empty = [
            (i, j)
            for i in range(GRID_SIZE)
            for j in range(GRID_SIZE)
            if self.grid[i][j] == 0
        ]
        if empty:
            value = 2 if random.random() < 0.9 else 4
            i, j = random.choice(empty)
            self.grid[i][j] = value

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        title_text = self.large_font.render("2048", True, TEXT_COLOR)
        self.screen.blit(title_text, (20, 20))

        # Score Panel
        score_surf = pygame.Surface((200, 70))
        score_surf.fill((187, 173, 160))
        pygame.draw.rect(score_surf, GRID_COLOR, score_surf.get_rect(), border_radius=8)

        score_label = self.small_font.render("Score", True, BRIGHT_TEXT_COLOR)
        score_val = self.small_font.render(str(self.score), True, BRIGHT_TEXT_COLOR)
        best_label = self.small_font.render("Highest", True, BRIGHT_TEXT_COLOR)
        best_val = self.small_font.render(str(self.best_score), True, BRIGHT_TEXT_COLOR)

        score_surf.blit(score_label, (20, 8))
        score_surf.blit(score_val, (20, 35))
        score_surf.blit(best_label, (120, 8))
        score_surf.blit(best_val, (120, 35))
        self.screen.blit(score_surf, (WIDTH - 240, 20))

        # Grid
        grid_w = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * GRID_PADDING
        grid_h = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * GRID_PADDING
        start_x = (WIDTH - grid_w) // 2
        start_y = (HEIGHT - grid_h) // 2 + 70

        pygame.draw.rect(
            self.screen, GRID_COLOR, (start_x, start_y, grid_w, grid_h), border_radius=8
        )

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                val = self.grid[i][j]
                x = start_x + GRID_PADDING + j * (TILE_SIZE + GRID_PADDING)
                y = start_y + GRID_PADDING + i * (TILE_SIZE + GRID_PADDING)

                pygame.draw.rect(
                    self.screen,
                    TILE_COLORS.get(val, TILE_COLORS[0]),
                    (x, y, TILE_SIZE, TILE_SIZE),
                    border_radius=4,
                )

                if val != 0:
                    font = (
                        self.font
                        if val < 100
                        else pygame.font.SysFont(
                            "Arial", FONT_SIZE - (8 if val < 1000 else 12), bold=True
                        )
                    )
                    text = font.render(str(val), True, TEXT_COLORS.get(val, TEXT_COLOR))
                    text_rect = text.get_rect(
                        center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2)
                    )
                    self.screen.blit(text, text_rect)

        hint = self.prompt_font.render(
            "Use arrows to move | Click buttons to Restart/Continue", True, TEXT_COLOR
        )
        self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 25))

        # Draw buttons
        self.draw_buttons()

        if self.game_over:
            self.show_overlay("Game Over!", f"Score: {self.score}")
        elif self.won:
            self.show_overlay("You Win!", f"Score: {self.score}", show_continue=True)

    def draw_buttons(self):
        mouse_pos = pygame.mouse.get_pos()

        def draw_btn(rect, label, img, hover_color, base_color):
            hovered = rect.collidepoint(mouse_pos)
            color = hover_color if hovered else base_color
            pygame.draw.rect(self.screen, color, rect, border_radius=6)
            if img:
                self.screen.blit(img, img.get_rect(center=rect.center))
            else:
                txt = self.small_font.render(label, True, (255, 255, 255))
                self.screen.blit(txt, txt.get_rect(center=rect.center))

        draw_btn(
            self.restart_rect,
            "Restart",
            self.restart_img,
            (100, 120, 255),
            (255, 100, 100),
        )
        if self.won:
            draw_btn(
                self.continue_rect,
                "Continue",
                self.continue_img,
                (120, 255, 120),
                (100, 200, 100),
            )

    def show_overlay(self, title, score_text, show_continue=False):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        self.screen.blit(overlay, (0, 0))

        panel = pygame.Surface((400, 200), pygame.SRCALPHA)
        panel.fill((240, 240, 240, 240))
        pygame.draw.rect(
            panel, (100, 100, 100), panel.get_rect(), border_radius=10, width=2
        )

        title_surf = self.large_font.render(title, True, (0, 0, 0))
        score_surf = self.font.render(score_text, True, TEXT_COLOR)
        self.screen.blit(panel, (WIDTH // 2 - 200, HEIGHT // 2 - 100))
        self.screen.blit(
            title_surf, (WIDTH // 2 - title_surf.get_width() // 2, HEIGHT // 2 - 80)
        )
        self.screen.blit(
            score_surf, (WIDTH // 2 - score_surf.get_width() // 2, HEIGHT // 2 - 20)
        )

    def move(self, direction):
        if self.game_over:
            return False

        moved = False
        if direction == "left":
            for i in range(GRID_SIZE):
                row, did_move = self.merge_row(self.grid[i])
                self.grid[i] = row
                moved |= did_move
        elif direction == "right":
            for i in range(GRID_SIZE):
                row, did_move = self.merge_row(self.grid[i][::-1])
                self.grid[i] = row[::-1]
                moved |= did_move
        elif direction == "up":
            for j in range(GRID_SIZE):
                col = [self.grid[i][j] for i in range(GRID_SIZE)]
                new_col, did_move = self.merge_row(col)
                for i in range(GRID_SIZE):
                    self.grid[i][j] = new_col[i]
                moved |= did_move
        elif direction == "down":
            for j in range(GRID_SIZE):
                col = [self.grid[i][j] for i in range(GRID_SIZE)][::-1]
                new_col, did_move = self.merge_row(col)
                for i in range(GRID_SIZE):
                    self.grid[i][j] = new_col[::-1][i]
                moved |= did_move

        if moved:
            self.add_new_tile()
            self.check_game_state()
            self.best_score = max(self.best_score, self.score)

        return moved

    def merge_row(self, row):
        new = [i for i in row if i != 0]
        new += [0] * (GRID_SIZE - len(new))
        merged = []
        skip = False
        moved = False

        for i in range(len(new)):
            if skip:
                skip = False
                continue
            if i < len(new) - 1 and new[i] == new[i + 1]:
                merged.append(new[i] * 2)
                self.score += new[i] * 2
                skip = True
                moved = True
            else:
                merged.append(new[i])
                if new[i] != row[i]:
                    moved = True
        merged += [0] * (GRID_SIZE - len(merged))
        return merged, moved

    def check_game_state(self):
        if any(2048 in row for row in self.grid):
            self.won = True
        if not any(0 in row for row in self.grid):
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE - 1):
                    if self.grid[i][j] == self.grid[i][j + 1]:
                        return
            for j in range(GRID_SIZE):
                for i in range(GRID_SIZE - 1):
                    if self.grid[i][j] == self.grid[i + 1][j]:
                        return
            self.game_over = True

    def reset(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.add_new_tile()
        self.add_new_tile()

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_rect.collidepoint(event.pos):
                        self.reset()
                    elif self.won and self.continue_rect.collidepoint(event.pos):
                        self.won = False
                elif event.type == pygame.KEYDOWN:
                    if not self.game_over and not self.won:
                        if event.key == pygame.K_LEFT:
                            self.move("left")
                        elif event.key == pygame.K_RIGHT:
                            self.move("right")
                        elif event.key == pygame.K_UP:
                            self.move("up")
                        elif event.key == pygame.K_DOWN:
                            self.move("down")

            self.draw()
            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    Game2048().run()
