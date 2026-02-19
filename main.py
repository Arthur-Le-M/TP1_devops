import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Paramètres de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Paramètres de la raquette
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5

# Paramètres de la balle
BALL_SIZE = 10
BALL_SPEED_X = 4
BALL_SPEED_Y = 4

class Paddle(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.score = 0

    def move(self, dy):
        self.y += dy
        self.y = max(self.y, 0)
        self.y = min(self.y, SCREEN_HEIGHT - PADDLE_HEIGHT)

class Ball(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, BALL_SIZE, BALL_SIZE)
        self.vx = BALL_SPEED_X
        self.vy = BALL_SPEED_Y

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Rebond haut/bas
        if self.top <= 0 or self.bottom >= SCREEN_HEIGHT:
            self.vy *= -1

    def reset(self):
        self.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.vx *= -1

# Création des objets
player = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
opponent = Paddle(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Boucle principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mouvements
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_z]: # Z/W pour haut (AZERTY/QWERTY)
        player.move(-PADDLE_SPEED)
    if keys[pygame.K_s]: # S pour bas
        player.move(PADDLE_SPEED)

    # IA simple pour l'adversaire
    if opponent.centery < ball.centery:
        opponent.move(PADDLE_SPEED)
    elif opponent.centery > ball.centery:
        opponent.move(-PADDLE_SPEED)

    ball.move()

    # Collisions
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball.vx *= -1
    
    # Score
    if ball.left <= 0:
        opponent.score += 1
        ball.reset()
    elif ball.right >= SCREEN_WIDTH:
        player.score += 1
        ball.reset()

    # Affichage
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, opponent)
    pygame.draw.rect(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    player_text = font.render(str(player.score), True, WHITE)
    screen.blit(player_text, (SCREEN_WIDTH // 4, 20))
    
    opponent_text = font.render(str(opponent.score), True, WHITE)
    screen.blit(opponent_text, (3 * SCREEN_WIDTH // 4, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
