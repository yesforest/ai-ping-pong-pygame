import pygame
import sys

# 1. Pygame-i işə salırıq və ekranı qururuq
pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Ping-Pong")

# 2. Rənglər və Saat
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
clock = pygame.time.Clock()

# --- YENİ: Şriftin qurulması ---
# Pygame-in daxili standart şriftindən istifadə edirik (Ölçüsü: 50)
game_font = pygame.font.Font(None, 50)

# --- YENİ: Xal dəyişənləri ---
player_score = 0
enemy_score = 0

# 3. Raketkaların ölçüləri və ilkin mövqeləri
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100

player_x = 10
player_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
player_paddle = pygame.Rect(player_x, player_y, PADDLE_WIDTH, PADDLE_HEIGHT)

enemy_x = WIDTH - 25
enemy_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
enemy_paddle = pygame.Rect(enemy_x, enemy_y, PADDLE_WIDTH, PADDLE_HEIGHT)

paddle_speed = 6

# Topun parametrləri
BALL_SIZE = 15
ball_x = WIDTH // 2 - BALL_SIZE // 2
ball_y = HEIGHT // 2 - BALL_SIZE // 2
ball = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)

# Topun sürəti (X və Y oxu üzrə)
ball_speed_x = 6
ball_speed_y = 6

# 4. ƏSAS OYUN DÖVRÜ
while True:
    # Hadisələrin yoxlanılması
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Oyunçu raketkasının hərəkəti (W və S düymələri ilə)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= paddle_speed
    if keys[pygame.K_s] and player_paddle.bottom < HEIGHT:
        player_paddle.y += paddle_speed

    # Topun hərəkəti
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Topun yuxarı və aşağı divarlara dəyib qayıtması
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Rəqib AI-ın məntiqi
    if enemy_paddle.centery < ball.centery and enemy_paddle.bottom < HEIGHT:
        enemy_paddle.y += paddle_speed - 1  
    if enemy_paddle.centery > ball.centery and enemy_paddle.top > 0:
        enemy_paddle.y -= paddle_speed - 1

    # Topun raketkalara dəyməsinin yoxlanılması (Collisions)
    if ball.colliderect(player_paddle) or ball.colliderect(enemy_paddle):
        ball_speed_x *= -1  

    # --- DƏYİŞİLDİ: Xal qazanma məntiqi ---
    if ball.left <= 0:
        # Top sol divardan çıxdısa, sağdakı rəqib xal qazanır
        enemy_score += 1
        # Topu sıfırlayırıq
        ball.x = WIDTH // 2 - BALL_SIZE // 2
        ball.y = HEIGHT // 2 - BALL_SIZE // 2
        ball_speed_x *= -1  

    if ball.right >= WIDTH:
        # Top sağ divardan çıxdısa, soldakı oyunçu xal qazanır
        player_score += 1
        # Topu sıfırlayırıq
        ball.x = WIDTH // 2 - BALL_SIZE // 2
        ball.y = HEIGHT // 2 - BALL_SIZE // 2
        ball_speed_x *= -1  

    # Vizual hissə
    screen.fill(BLACK)

    # Obyektləri ekrana çəkirik
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, enemy_paddle)
    pygame.draw.ellipse(screen, WHITE, ball) 
    
    # Ortadakı kəsik xətt
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # --- YENİ: Xalları ekranda render edib çəkirik ---
    # render() funksiyası mətni şəkilə (Surface) çevirir. True - hamarlaşdırma (anti-aliasing) üçündür.
    player_text = game_font.render(str(player_score), True, WHITE)
    enemy_text = game_font.render(str(enemy_score), True, WHITE)
    
    # blit() funksiyası bu mətn şəkillərini təyin etdiyimiz koordinatlara yapışdırır
    screen.blit(player_text, (WIDTH // 4, 20))         # Ekranın sol dörddə birində
    screen.blit(enemy_text, (3 * WIDTH // 4 - 20, 20)) # Ekranın sağ dörddə birində

    pygame.display.flip()
    clock.tick(60)