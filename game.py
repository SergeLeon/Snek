from random import randint

import pygame

pygame.init()

# размер окна
size = [1280, 720]
window = pygame.display.set_mode(size)

pygame.display.set_caption("Snek game")

screen = pygame.Surface(size)

font = pygame.font.Font("AtariClassic-Regular.ttf", 36)

cell_size = 40


class Snake():
    def __init__(self):
        self.moves = {"hold": [0, 0],
                      "up": [0, -1],
                      "down": [0, 1],
                      "left": [-1, 0],
                      "right": [1, 0]}
        self.score = 0
        self.head = [16, 8]
        self.snake = [[16, 10], [16, 9], self.head]
        self.move_round = "up"

    def render(self):
        for block in self.snake:
            pygame.draw.rect(screen, [0, 255, 0], (block[0] * cell_size, block[1] * cell_size, cell_size, cell_size))

    def move(self, apple_list):
        pushed_keys = pygame.key.get_pressed()

        if pushed_keys[pygame.K_w] and self.move_round != "down":
            self.move_round = "up"
        if pushed_keys[pygame.K_s] and self.move_round != "up":
            self.move_round = "down"
        if pushed_keys[pygame.K_d] and self.move_round != "left":
            self.move_round = "right"
        if pushed_keys[pygame.K_a] and self.move_round != "right":
            self.move_round = "left"

        self.head = [self.head[0] + self.moves[self.move_round][0], self.head[1] + self.moves[self.move_round][1]]
        self.snake.append(self.head)

        apple_eaten = False
        for apple in apple_list:
            if self.check_apple_contact(apple):
                apple.repose()
                self.score += 1
                apple_eaten = True

        if not apple_eaten:
            self.snake.pop(0)


    def check_apple_contact(self, apple):
        if self.head == apple.get_cords():
            return True
        return False

    def check_death(self):
        if self.head in self.snake[0:-1]:
            return True
        if self.head[0] <= -1 or self.head[0] >= 32 or self.head[1] <= -1 or self.head[1] >= 18:
            return True
        return False


class Apple():
    def __init__(self):
        self.x = randint(1, 31)
        self.y = randint(1, 17)
        self.color = [255, 0, 0]

    def render(self, cell_size):
        pygame.draw.circle(screen, self.color,
                           (self.x * cell_size + cell_size // 2 + 1, self.y * cell_size + cell_size // 2 + 1),
                           cell_size // 2 - 1)

    def get_cords(self):
        return [self.x, self.y]

    def repose(self):
        self.x = randint(1, 31)
        self.y = randint(1, 17)


def render_field(window_size, cell_size):
    depth = 2
    for x in range(-1, round(window_size[0] / cell_size) + 1):
        pygame.draw.line(screen, [0, 0, 0], [x * cell_size, 0], [x * cell_size, window_size[1]], depth)
    for y in range(-1, round(window_size[1] / cell_size) + 1):
        pygame.draw.line(screen, [0, 0, 0], [0, y * cell_size], [window_size[0], y * cell_size], depth)


def show_score(score):
    text = font.render(f"score: {score}", 1, (0, 0, 0))
    text_pos = (442, 20)

    screen.blit(text, text_pos)


def start_game():
    apple_list = [Apple()]
    snek = Snake()

    running_game = True
    while running_game:
        # обработка событий
        for e in pygame.event.get():
            if e.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running_game = False

        screen.fill([144, 238, 144])

        if not snek.check_death():
            for apple in apple_list:
                apple.render(cell_size)

            snek.move(apple_list)

            snek.render()

            render_field(size, cell_size)
            # отображение окна
            window.blit(screen, [0, 0])
        else:
            text = font.render("You Lose", 1, (0, 0, 0))
            screen.blit(text, (445, 300))

        window.blit(screen, [0, 0])
        pygame.display.flip()
        pygame.time.delay(100)

    pygame.display.set_caption("SneK menu")


if __name__ == "__main__":
    start_game()
