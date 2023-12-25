import pygame
import sys
import random
pygame.init()
pygame.mixer.music.load('sound/music.mp3')
pygame.mixer.music.play(-1)
screen_width = 800
screen_height = 600
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
brick_colors = [(200, 0, 0), (0, 200, 0), (0, 0, 200), (200, 200, 0), (0, 200, 200)]
paddle_width = 100
paddle_height = 10
paddle_speed = 9
ball_radius = 12
ball_speed = 5
brick_width = 80
brick_height = 20
brick_rows = 5
brick_cols = 10
brick_gap = 5
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Арканоид")
paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - paddle_height - 10, paddle_width, paddle_height)

ball = pygame.Rect(screen_width // 2 - ball_radius, screen_height // 2 - ball_radius, ball_radius * 2, ball_radius * 2)
ball_direction = [1, -1]  
def create_bricks():
    return [
        pygame.Rect(col * (brick_width + brick_gap), row * (brick_height + brick_gap), brick_width, brick_height)
        for row in range(brick_rows) for col in range(brick_cols)
    ]
bricks = create_bricks()
score = 0
font = pygame.font.Font(None, 36)
game_started = False
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_started = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-paddle_speed, 0)
    if keys[pygame.K_RIGHT] and paddle.right < screen_width:
        paddle.move_ip(paddle_speed, 0)

    if game_started:
        ball.move_ip(ball_speed * ball_direction[0], ball_speed * ball_direction[1])

        if ball.left <= 0 or ball.right >= screen_width:
            ball_direction[0] *= -1
        if ball.top <= 0:
            ball_direction[1] *= -1

        if ball.colliderect(paddle):
            ball_direction[1] *= -1

        for brick in bricks[:]:
            if ball.colliderect(brick):
                ball_direction[1] *= -1
                bricks.remove(brick)
                score += 10

        if ball.bottom >= screen_height or ball.top <= 0:
            game_started = False
            ball.x = screen_width // 2 - ball_radius
            ball.y = screen_height // 2 - ball_radius
            bricks = create_bricks()
            score = 0

    if not bricks:
        game_started = False
        ball.x = screen_width // 2 - ball_radius
        ball.y = screen_height // 2 - ball_radius
        bricks = create_bricks()
        score_surface = font.render("Ты был(а) умницей!", True, (0, 255, 0))
        screen.blit(score_surface, (screen_width // 2 - 150, screen_height // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        score = 0

    screen.fill(white)
    pygame.draw.rect(screen, blue, paddle)
    pygame.draw.ellipse(screen, red, ball)

    for i, brick in enumerate(bricks):
        pygame.draw.rect(screen, brick_colors[i % len(brick_colors)], brick)

    score_surface = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))
    pygame.display.flip()
    clock.tick(60)