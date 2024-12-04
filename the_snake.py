import pygame
import random

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        """Инициализирует базовые атрибуты объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, screen):
        """Отрисовывает объект на экране."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self):
        """Инициализирует яблоко."""
        super().__init__((0, 0), (255, 0, 0))
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self, screen):
        """Отрисовывает яблоко на экране."""
        pygame.draw.rect(
            screen,
            self.body_color,
            (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE),
        )


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self):
        """Инициализирует змейку."""
        super().__init__(
            ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)), (0, 255, 0)
        )
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        if (
            (self.direction == UP and new_direction == DOWN)
            or (self.direction == DOWN and new_direction == UP)
            or (self.direction == LEFT and new_direction == RIGHT)
            or (self.direction == RIGHT and new_direction == LEFT)
        ):
            return
        self.next_direction = new_direction

    def move(self):
        """Обновляет позицию змейки."""
        head_position = self.get_head_position()
        new_head_position = (
            (head_position[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_position[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )
        if new_head_position in self.positions[1:]:
            self.reset()
            return

        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None
        self.direction = self.next_direction or self.direction

    def draw(self, screen):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            pygame.draw.rect(
                screen,
                self.body_color,
                (position[0], position[1], GRID_SIZE, GRID_SIZE),
            )
        if self.last:
            pygame.draw.rect(
                screen,
                BOARD_BACKGROUND_COLOR,
                (self.last[0], self.last[1], GRID_SIZE, GRID_SIZE),
            )

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Основной игровой цикл."""
    pygame.init()
    pygame.display.set_caption("Змейка")

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(15)


if __name__ == "__main__":
    main()
