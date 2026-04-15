import unittest
import os

# Configurer un affichage "dummy" pour ne pas ouvrir de fenêtre Pygame durant les tests CLI/CI
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame

# Import des éléments à tester (sans lancer la boucle principale)
from main import Paddle, Ball, Bonus, SCREEN_WIDTH, SCREEN_HEIGHT, PADDLE_HEIGHT, PADDLE_SPEED, BALL_SPEED_X, BALL_SPEED_Y

class TestPong(unittest.TestCase):

    def setUp(self):
        # Initialiser pygame (requis pour les Rects et autres fonctions internes si besoin)
        pygame.init()
        pygame.display.set_mode((1, 1))

    def tearDown(self):
        pygame.quit()

    def test_paddle_move(self):
        paddle = Paddle(50, 50)
        
        # Tester un mouvement simple
        paddle.move(10)
        self.assertEqual(paddle.y, 60)
        
        # Tester le blocage en bas
        paddle.y = SCREEN_HEIGHT - PADDLE_HEIGHT
        paddle.move(10)
        self.assertEqual(paddle.y, SCREEN_HEIGHT - PADDLE_HEIGHT)
        
        # Tester le blocage en haut
        paddle.y = 0
        paddle.move(-10)
        self.assertEqual(paddle.y, 0)

    def test_paddle_reset_stats(self):
        paddle = Paddle(50, 50)
        
        # Modification des statistiques
        paddle.height += 50
        paddle.speed += 5
        paddle.power_hit = True
        
        # Réinitialisation
        paddle.reset_stats()
        
        self.assertEqual(paddle.height, PADDLE_HEIGHT)
        self.assertEqual(paddle.speed, PADDLE_SPEED)
        self.assertFalse(paddle.power_hit)

    def test_ball_move_and_bounce(self):
        ball = Ball(SCREEN_WIDTH // 2, 0) # Balle tout en haut
        ball.vy = -10 # Mouvement vers le haut (collisions au top)
        
        ball.move()
        # Devrait rebondir (inversion vy) car elle tape le "top" (self.top <= 0)
        self.assertEqual(ball.vy, 10)
        
        ball.y = SCREEN_HEIGHT # Balle tout en bas
        ball.vy = 10 # Mouvement vers le bas
        ball.move()
        # Devrait rebondir
        self.assertEqual(ball.vy, -10)

    def test_ball_reset(self):
        ball = Ball(10, 10)
        ball.vx = 20 # Balle allant à droite
        ball.vy = 20
        
        ball.reset()
        
        # La balle doit être replacée au centre
        self.assertEqual(ball.centerx, SCREEN_WIDTH // 2)
        self.assertEqual(ball.centery, SCREEN_HEIGHT // 2)
        # La vitesse doit repartir dans le sens inverse (vers le perdant) avec une magnitude de base
        self.assertTrue(ball.vx < 0)
        self.assertEqual(abs(ball.vx), BALL_SPEED_X)

if __name__ == '__main__':
    unittest.main()
