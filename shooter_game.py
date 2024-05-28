import pygame
import random
import sys

# Inicialización de PyGame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Reloj para controlar la velocidad de fotogramas
clock = pygame.time.Clock()

# Clases
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 8
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Limitar al jugador dentro de la pantalla
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH - 50), 0))
        self.speed = random.randint(2, 4)
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.top = 0
            self.rect.centerx = random.randint(50, WIDTH - 50)

        self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect(midtop=(x, y))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Funciones
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def show_menu():
    screen.fill(BLACK)
    draw_text("Shooter Game", 64, WHITE, WIDTH // 2, HEIGHT // 4)
    draw_text("Seleccione la dificultad:", 36, WHITE, WIDTH // 2, HEIGHT // 2)
    draw_text("Fácil (F)", 30, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
    draw_text("Medio (M)", 30, WHITE, WIDTH // 2, HEIGHT // 2 + 100)
    draw_text("Difícil (D)", 30, WHITE, WIDTH // 2, HEIGHT // 2 + 150)
    pygame.display.flip()

def show_game_over(score):
    screen.fill(BLACK)
    draw_text("GAME OVER", 64, WHITE, WIDTH // 2, HEIGHT // 4)
    draw_text(f"Puntuación: {score}", 36, WHITE, WIDTH // 2, HEIGHT // 2)
    draw_text("Presione R para jugar de nuevo", 30, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
    pygame.display.flip()

def main(difficulty):
    global all_sprites, enemies, bullets, enemy_bullets, player
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    
    running = True
    game_over = False
    score = 0
    while running:
        clock.tick(60)
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                elif event.key == pygame.K_r and game_over:
                    main(difficulty)
        
        if not game_over:
            all_sprites.update()
        
            # Generar nuevos enemigos
            if random.randint(0, 100) < 2:
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)
        
            # Colisiones - Jugador vs Enemigos
            hits = pygame.sprite.spritecollide(player, enemies, False)
            if hits:
                player.lives -= 1
                if player.lives == 0:
                    game_over = True
                else:
                    for enemy in enemies:
                        enemy.kill()
        
            # Colisiones - Jugador vs Balas Enemigas
            hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
            if hits:
                player.lives -= 1
                if player.lives == 0:
                    game_over = True
        
            # Colisiones - Balas vs Enemigos
            hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
            for hit in hits:
                score += 1
        
            all_sprites.draw(screen)
        
        if game_over:
            show_game_over(score)
        
        pygame.display.flip()

# Mostrar el menú inicial
show_menu()

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                main("easy")
            elif event.key == pygame.K_m:
                main("medium")
            elif event.key == pygame.K_d:
                main("hard")
        
