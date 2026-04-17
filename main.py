import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
GRAY = (100, 100, 100)
DARK_RED = (139, 0, 0)
LIGHT_GREEN = (144, 238, 144)


class Chicken(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(YELLOW)
        pygame.draw.circle(self.image, BLACK, (10, 15), 3)
        pygame.draw.circle(self.image, BLACK, (30, 15), 3)
        pygame.draw.polygon(self.image, RED, [(15, 0), (20, -10), (25, 0)])
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction):
        super().__init__()
        self.image = pygame.Surface((60, 35))

        colors = [RED, (255, 100, 0), (0, 100, 255), (128, 0, 128)]
        color = random.choice(colors)
        self.image.fill(color)

        pygame.draw.rect(self.image, (100, 100, 100), (10, 5, 15, 15))
        pygame.draw.rect(self.image, (100, 100, 100), (35, 5, 15, 15))
        pygame.draw.circle(self.image, BLACK, (10, 30), 8)
        pygame.draw.circle(self.image, BLACK, (50, 30), 8)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = direction

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Курочка перебеги дорогу!")
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.chicken = Chicken()
        self.all_sprites.add(self.chicken)

        self.score = 0
        self.lives = 3
        self.level = 1
        self.car_spawn_timer = 0
        self.level_timer = 0

        self.road_y_positions = [150, 200, 250, 300, 350, 400]
        self.car_speeds = [3, 4, 5, 4, 6, 5]
        self.car_directions = [1, -1, 1, -1, 1, -1]

    def spawn_car(self):
        lane = random.randint(0, len(self.road_y_positions) - 1)
        y = self.road_y_positions[lane]
        speed = self.car_speeds[lane] + (self.level - 1) // 2
        direction = self.car_directions[lane]

        if direction == 1:
            x = -60
        else:
            x = SCREEN_WIDTH + 60

        car = Car(x, y, speed, direction)
        self.cars.add(car)
        self.all_sprites.add(car)

    def draw_heart(self, x, y, size=20):
        heart_points = [
            (x, y + size // 4),
            (x - size // 2, y - size // 4),
            (x - size // 4, y - size // 2),
            (x, y - size // 4),
            (x + size // 4, y - size // 2),
            (x + size // 2, y - size // 4)
        ]
        pygame.draw.polygon(self.screen, RED, heart_points)
        pygame.draw.circle(self.screen, RED, (x - size // 4, y - size // 4), size // 3)
        pygame.draw.circle(self.screen, RED, (x + size // 4, y - size // 4), size // 3)

    def draw_star(self, x, y, size=15):
        points = []
        for i in range(5):
            angle = i * 144 - 90
            rad = size
            x1 = x + rad * pygame.math.Vector2(1, 0).rotate(angle).x
            y1 = y + rad * pygame.math.Vector2(1, 0).rotate(angle).y
            points.append((x1, y1))

            rad = size // 2
            x2 = x + rad * pygame.math.Vector2(1, 0).rotate(angle + 36).x
            y2 = y + rad * pygame.math.Vector2(1, 0).rotate(angle + 36).y
            points.append((x2, y2))

        pygame.draw.polygon(self.screen, YELLOW, points)

    def draw_road(self):
        pygame.draw.rect(self.screen, GRAY, (0, 120, SCREEN_WIDTH, 340))

        for i, y in enumerate(self.road_y_positions):
            pygame.draw.line(self.screen, WHITE, (0, y + 17), (SCREEN_WIDTH, y + 17), 2)
            if i < len(self.road_y_positions) - 1:
                for x in range(0, SCREEN_WIDTH, 40):
                    pygame.draw.line(self.screen, YELLOW, (x, y + 35), (x + 20, y + 35), 3)

        pygame.draw.rect(self.screen, GREEN, (0, 0, SCREEN_WIDTH, 120))
        pygame.draw.rect(self.screen, GREEN, (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80))

        pygame.draw.rect(self.screen, BROWN, (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 10))

        for i in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, 100)
            pygame.draw.circle(self.screen, (255, 200, 200), (x, y), 3)
            pygame.draw.circle(self.screen, (255, 255, 0), (x, y), 1)

        pygame.draw.rect(self.screen, BROWN, (SCREEN_WIDTH - 80, 50, 60, 70))
        pygame.draw.polygon(self.screen, RED,
                            [(SCREEN_WIDTH - 80, 50), (SCREEN_WIDTH - 50, 20), (SCREEN_WIDTH - 20, 50)])
        pygame.draw.rect(self.screen, YELLOW, (SCREEN_WIDTH - 55, 85, 10, 35))

    def draw_ui(self):
        for i in range(self.lives):
            self.draw_heart(40 + i * 35, 30)

        stars_count = self.score // 100
        for i in range(min(stars_count, 10)):
            self.draw_star(SCREEN_WIDTH - 40 - i * 30, 30, 12)

        level_width = (self.level % 10) * 20
        pygame.draw.rect(self.screen, DARK_RED, (SCREEN_WIDTH // 2 - 100, 15, 200, 20))
        pygame.draw.rect(self.screen, LIGHT_GREEN, (SCREEN_WIDTH // 2 - 100, 15, level_width, 20))

        pygame.draw.circle(self.screen, YELLOW, (SCREEN_WIDTH // 2 - 110, 25), 10)

    def show_effect(self, effect_type, x, y):
        if effect_type == "death":
            for i in range(10):
                pygame.draw.circle(self.screen, RED, (x + random.randint(-20, 20),
                                                      y + random.randint(-20, 20)),
                                   random.randint(2, 8))
        elif effect_type == "level_up":
            for i in range(30):
                pygame.draw.circle(self.screen, YELLOW, (x + random.randint(-50, 50),
                                                         y + random.randint(-30, 30)),
                                   random.randint(3, 10))

    def reset_chicken_position(self):
        self.show_effect("death", self.chicken.rect.centerx, self.chicken.rect.centery)

        self.chicken.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.lives -= 1

        if self.lives <= 0:
            self.game_over()
        else:
            for i in range(5):
                self.screen.fill(BLACK)
                self.draw_road()
                self.all_sprites.draw(self.screen)
                self.draw_ui()
                pygame.display.flip()
                pygame.time.wait(100)

    def next_level(self):
        self.level += 1
        self.score += 100

        self.show_effect("level_up", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        for car in self.cars:
            car.kill()

        for i in range(3):
            self.screen.fill(BLACK)
            self.draw_road()
            self.all_sprites.draw(self.screen)
            self.draw_ui()

            if i % 2 == 0:
                pygame.draw.rect(self.screen, YELLOW, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 50)

            pygame.display.flip()
            pygame.time.wait(300)

        if self.level % 3 == 0:
            self.car_speeds = [min(s + 0.5, 10) for s in self.car_speeds]

        self.chicken.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

    def game_over(self):
        for i in range(10):
            self.screen.fill(BLACK)
            self.draw_road()
            self.all_sprites.draw(self.screen)
            self.draw_ui()

            offset = i * 10
            pygame.draw.line(self.screen, RED, (SCREEN_WIDTH // 2 - 50 - offset, SCREEN_HEIGHT // 2 - 50 - offset),
                             (SCREEN_WIDTH // 2 + 50 + offset, SCREEN_HEIGHT // 2 + 50 + offset), 5)
            pygame.draw.line(self.screen, RED, (SCREEN_WIDTH // 2 + 50 + offset, SCREEN_HEIGHT // 2 - 50 - offset),
                             (SCREEN_WIDTH // 2 - 50 - offset, SCREEN_HEIGHT // 2 + 50 + offset), 5)

            pygame.display.flip()
            pygame.time.wait(100)

        pygame.time.wait(2000)
        self.running = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r and self.lives <= 0:
                        return True

            self.chicken.update()
            self.cars.update()

            self.car_spawn_timer += 1
            spawn_delay = random.randint(2, 7)
            if self.car_spawn_timer > spawn_delay:
                self.car_spawn_timer = 0
                if random.random() < 0.7 + self.level * 0.02:
                    self.spawn_car()

            collisions = pygame.sprite.spritecollide(self.chicken, self.cars, False)
            if collisions:
                self.reset_chicken_position()
                pygame.time.wait(500)

            if self.chicken.rect.top < 120:
                self.next_level()

            self.level_timer += 10
            if self.level_timer > 1800:
                self.level_timer = 0
                if self.level < 50:
                    self.level += 0.5

            self.screen.fill(BLACK)
            self.draw_road()
            self.all_sprites.draw(self.screen)
            self.draw_ui()

            pygame.display.flip()
            self.clock.tick(FPS)

        return False


def main():

    while True:
        game = Game()
        restart = game.run()
        if not restart:
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()