import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR_BONUS1 = (0, 255, 0)     # Vert pour Agrandir
COLOR_BONUS2 = (255, 0, 0)     # Rouge pour Rapetisser
COLOR_BONUS3 = (0, 0, 255)     # Bleu pour Vitesse
COLOR_BONUS4 = (255, 255, 0)   # Jaune pour Puissance

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
        self.base_speed = PADDLE_SPEED
        self.speed = self.base_speed
        self.power_hit = False

    def move(self, dy):
        self.y += dy * (self.speed / self.base_speed)
        self.y = max(self.y, 0)
        self.y = min(self.y, SCREEN_HEIGHT - self.height)

    def reset_stats(self):
        # Réinitialiser la taille, la vitesse et le pouvoir
        diff_height = PADDLE_HEIGHT - self.height
        self.y -= diff_height // 2 # Recentrer la raquette si elle avait changé de taille
        self.height = PADDLE_HEIGHT
        self.speed = self.base_speed
        self.power_hit = False

class Ball(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, BALL_SIZE, BALL_SIZE)
        self.exact_x = float(x)
        self.exact_y = float(y)
        self.vx = float(BALL_SPEED_X)
        self.vy = float(BALL_SPEED_Y)

    def move(self):
        self.exact_x += self.vx
        self.exact_y += self.vy
        self.x = int(self.exact_x)
        self.y = int(self.exact_y)

        # Rebond haut/bas
        if self.top <= 0 or self.bottom >= SCREEN_HEIGHT:
            self.vy *= -1

    def reset(self):
        self.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.exact_x = float(self.x)
        self.exact_y = float(self.y)
        # On réinitialise la vitesse de base, tout en l'envoyant vers celui qui a perdu
        direction_x = 1 if self.vx > 0 else -1
        direction_y = 1 if self.vy > 0 else -1
        self.vx = float(BALL_SPEED_X) * direction_x * -1
        self.vy = float(BALL_SPEED_Y) * direction_y
        
        # Sur chaque "reset", on remet tout à 0
        bonuses.clear()
        player.reset_stats()
        opponent.reset_stats()
        global last_hit, bonus_spawn_timer
        last_hit = None
        bonus_spawn_timer = 0
class Bonus(pygame.Rect):
    def __init__(self):
        super().__init__(0, 0, 20, 20)
        self.x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4)
        self.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.type = random.randint(1, 4)
        self.timer = 500  # Disparaît après environ 8-10 secondes si 60 FPS

    def render(self, screen):
        if self.type == 1:
            color = COLOR_BONUS1 # Agrandir
        elif self.type == 2:
            color = COLOR_BONUS2 # Rapetisser (Adversaire)
        elif self.type == 3:
            color = COLOR_BONUS3 # Vitesse
        elif self.type == 4:
            color = COLOR_BONUS4 # Frappe
        pygame.draw.rect(screen, color, self)

# Création des objets
player = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
opponent = Paddle(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Variables d'état
game_state = "MENU" # "MENU", "SOLO", "MULTI"
bonuses = []
bonus_spawn_timer = 0
last_hit = None

def draw_menu():
    screen.fill(BLACK)
    title = pygame.font.Font(None, 74).render("PONG", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
    
    texte_solo = font.render("Appuyez sur '1' pour Jouer en Solo", True, WHITE)
    screen.blit(texte_solo, (SCREEN_WIDTH // 2 - texte_solo.get_width() // 2, 250))
    
    texte_multi = font.render("Appuyez sur '2' pour Jouer en Multi (Z/S et Flèches)", True, WHITE)
    screen.blit(texte_multi, (SCREEN_WIDTH // 2 - texte_multi.get_width() // 2, 350))
    
    pygame.display.flip()

def main_loop():
    global game_state, last_hit, bonus_spawn_timer
    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = "MENU"
            
            if game_state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        game_state = "SOLO"
                        player.score = 0
                        opponent.score = 0
                        ball.reset()
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        game_state = "MULTI"
                        player.score = 0
                        opponent.score = 0
                        ball.reset()

        if game_state == "MENU":
            draw_menu()
            clock.tick(60)
            continue

        # Mouvements
        keys = pygame.key.get_pressed()
        
        # Mouvements Joueur 1 (Gauche)
        if keys[pygame.K_w] or keys[pygame.K_z]: # Z/W pour haut (AZERTY/QWERTY)
            player.move(-PADDLE_SPEED)
        if keys[pygame.K_s]: # S pour bas
            player.move(PADDLE_SPEED)

        if game_state == "SOLO":
            # IA simple pour l'adversaire
            if opponent.centery < ball.centery:
                opponent.move(PADDLE_SPEED)
            elif opponent.centery > ball.centery:
                opponent.move(-PADDLE_SPEED)
        elif game_state == "MULTI":
            # Mouvements Joueur 2 (Droite)
            if keys[pygame.K_UP]:
                opponent.move(-PADDLE_SPEED)
            if keys[pygame.K_DOWN]:
                opponent.move(PADDLE_SPEED)

        ball.move()

        # Collisions avec les raquettes
        if ball.colliderect(player) and ball.vx < 0:
            # Rebond standard
            ball.vx *= -1.1
            ball.vy *= 1.1
            last_hit = player
            # Frappe propulsée (Bonus 4)
            if player.power_hit:
                ball.vx *= 2.0
                player.power_hit = False # Consomme la frappe
            # On annule la propulsion adverse s'il y en avait une (reset vitesse) en touchant
            elif abs(ball.vx) > float(BALL_SPEED_X) * 2:
                ball.vx = float(BALL_SPEED_X) * 1.1

        elif ball.colliderect(opponent) and ball.vx > 0:
            ball.vx *= -1.1
            ball.vy *= 1.1
            last_hit = opponent
            if opponent.power_hit:
                ball.vx *= 2.0
                opponent.power_hit = False
            elif abs(ball.vx) > float(BALL_SPEED_X) * 2:
                ball.vx = float(BALL_SPEED_X) * 1.1 * -1

        # Apparition et disparition des bonus
        bonus_spawn_timer += 1
        if bonus_spawn_timer >= 300: # ~5 secondes
            if random.random() < 0.6 and len(bonuses) < 3: # 60% chance
                bonuses.append(Bonus())
            bonus_spawn_timer = 0
        
        # Update des bonus à l'écran
        for b in bonuses[:]:
            b.timer -= 1
            if b.timer <= 0:
                bonuses.remove(b)
            # Collision Balle / Bonus
            elif ball.colliderect(b):
                bonuses.remove(b)
                # Appliquer le bonus au last_hit
                if last_hit is not None:
                    if b.type == 1: # Agrandir (limite max = 200)
                        if last_hit.height < 200:
                            last_hit.y -= 25
                            last_hit.height += 50
                    elif b.type == 2: # Rapetisser (Adversaire, max = 50)
                        victim = opponent if last_hit == player else player
                        if victim.height > 50:
                            victim.y += 25
                            victim.height -= 50
                    elif b.type == 3: # Rapide
                        last_hit.speed += 2
                    elif b.type == 4: # Puissance
                        last_hit.power_hit = True
        
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

        # Dessiner les bonus actifs
        for b in bonuses:
            b.render(screen)
    
        player_text = font.render(str(player.score), True, WHITE)
        screen.blit(player_text, (SCREEN_WIDTH // 4, 20))
        
        opponent_text = font.render(str(opponent.score), True, WHITE)
        screen.blit(opponent_text, (3 * SCREEN_WIDTH // 4, 20))
    
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_loop()
    pygame.quit()
    sys.exit()
