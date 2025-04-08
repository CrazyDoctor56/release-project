import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_WIDTH = 100
PIPE_GAP = 200
PIPE_SPEED = 3

HIGHSCORE_FILE = "highscore.txt"
if not os.path.exists(HIGHSCORE_FILE):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write("0")

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Python")
clock = pygame.time.Clock()

bg = pygame.image.load("background.png").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

bird_img = pygame.image.load("bird.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (50, 50))
bird_rect = bird_img.get_rect()
bird_width, bird_height = bird_rect.width, bird_rect.height

pipe_img = pygame.image.load("pipe.png").convert_alpha()
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, 500))
pipe_img_flip = pygame.transform.flip(pipe_img, False, True)

def draw_text(text, size, x, y, center=True, color=(255, 255, 255)):
    font = pygame.font.SysFont("Arial", size)
    render = font.render(text, True, color)
    rect = render.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    sc.blit(render, rect)

def load_highscore():
    with open(HIGHSCORE_FILE, "r") as f:
        return int(f.read().strip())

def save_highscore(score):
    highscore = load_highscore()
    if score > highscore:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))

def show_menu():
    while True:
        sc.blit(bg, (0, 0))
        draw_text("FLAPPY PYTHON", 64, WIDTH//2, HEIGHT//3)
        draw_text("Натисни пробіл, щоб грати", 32, WIDTH//2, HEIGHT//2 + 50)
        draw_text(f"Рекорд: {load_highscore()}", 28, WIDTH//2, HEIGHT//2 + 100)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def create_pipe():
    height = random.randint(100, HEIGHT - PIPE_GAP - 100)
    top_rect = pygame.Rect(WIDTH, 0, PIPE_WIDTH, height)
    bottom_rect = pygame.Rect(WIDTH, height + PIPE_GAP, PIPE_WIDTH, HEIGHT - height - PIPE_GAP)
    return {
        "top": top_rect,
        "bottom": bottom_rect,
        "passed": False
    }

def main_game():
    bird_x = 100
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = [create_pipe()]
    score = 0
    show_hitboxes = False

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = JUMP_STRENGTH
                if event.key == pygame.K_g:
                    show_hitboxes = not show_hitboxes

        bird_velocity += GRAVITY
        bird_y += bird_velocity

        for pipe in pipes:
            pipe["top"].x -= PIPE_SPEED
            pipe["bottom"].x -= PIPE_SPEED

        if pipes[-1]["top"].x < WIDTH - 300:
            pipes.append(create_pipe())
        if pipes[0]["top"].x < -PIPE_WIDTH:
            pipes.pop(0)

        bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
        for pipe in pipes:
            if bird_rect.colliderect(pipe["top"]) or bird_rect.colliderect(pipe["bottom"]):
                save_highscore(score)
                return

        if bird_y < 0 or bird_y > HEIGHT:
            save_highscore(score)
            return

        for pipe in pipes:
            if pipe["top"].x + PIPE_WIDTH < bird_x and not pipe["passed"]:
                pipe["passed"] = True
                score += 1

        sc.blit(bg, (0, 0))
        sc.blit(bird_img, (bird_x, bird_y))

        for pipe in pipes:
            sc.blit(pipe_img_flip, (pipe["top"].x, pipe["top"].bottom - pipe_img_flip.get_height()))
            sc.blit(pipe_img, (pipe["bottom"].x, pipe["bottom"].y))

            if show_hitboxes:
                pygame.draw.rect(sc, (0, 255, 0), pipe["top"], 2)
                pygame.draw.rect(sc, (0, 255, 0), pipe["bottom"], 2)

        if show_hitboxes:
            pygame.draw.rect(sc, (255, 0, 0), bird_rect, 2)

        draw_text(f"Очки: {score}", 32, 10, 10, center=False)

        pygame.display.update()

while True:
    show_menu()
    main_game()