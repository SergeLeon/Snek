from random import randint

import pygame

pygame.init()

# размер окна
win_width = 1280
win_height = 720
win_size = [win_width, win_height]
cell_size = 40

size_mult = 1


def resize(obj):
    if type(obj) == int:
        return round(obj * size_mult)
    return [round(x * size_mult) for x in obj]


win_width = resize(win_width)
win_height = resize(win_height)
win_size = resize(win_size)
cell_size = resize(cell_size)

x_cells = int(win_width / cell_size)
y_cells = int(win_height / cell_size)

window = pygame.display.set_mode(win_size)

pygame.display.set_caption("Snek game")

screen = pygame.Surface(win_size)

font = pygame.font.Font("AtariClassic-Regular.ttf", 36)


class Snake:
    def __init__(self):
        self.moves = {"hold": [0, 0],
                      "up": [0, -1],
                      "down": [0, 1],
                      "left": [-1, 0],
                      "right": [1, 0]}
        self.score = 0
        self.head = [x_cells // 2, y_cells // 2]
        self.snake = [[x_cells // 2, y_cells // 2 + 2], [x_cells // 2, y_cells // 2 + 1], self.head]
        self.move_round = "up"

    def get_score(self):
        return self.score

    def score_events(self, apple_list):
        if self.score % 20 == 0:
            apple_list.append(Apple())

    def render(self):
        """Отрисовка змеи"""
        for num, block in enumerate(self.snake):
            # Головы
            if block == self.head:
                pygame.draw.rect(screen, [0, 160, 0],
                                 (*[cord * cell_size for cord in block], cell_size, cell_size))
            # Тела
            elif (num % 5) == 0:
                pygame.draw.rect(screen, [153, 255, 71],
                                 (*[cord * cell_size for cord in block], cell_size, cell_size))
            else:
                pygame.draw.rect(screen, [86, 230, 15],
                                 (*[cord * cell_size for cord in block], cell_size, cell_size))

    def move(self, apple_list):
        pushed_keys = pygame.key.get_pressed()

        if (pushed_keys[pygame.K_w] or pushed_keys[pygame.K_UP]) and self.move_round != "down":
            self.move_round = "up"
        elif (pushed_keys[pygame.K_s] or pushed_keys[pygame.K_DOWN]) and self.move_round != "up":
            self.move_round = "down"
        elif (pushed_keys[pygame.K_d] or pushed_keys[pygame.K_RIGHT]) and self.move_round != "left":
            self.move_round = "right"
        elif (pushed_keys[pygame.K_a] or pushed_keys[pygame.K_LEFT]) and self.move_round != "right":
            self.move_round = "left"

        self.head = [self.head[0] + self.moves[self.move_round][0], self.head[1] + self.moves[self.move_round][1]]
        self.snake.append(self.head)

        apple_eaten = False
        for apple in apple_list:
            if self.check_apple_contact(apple):
                apple.repose(self.snake)
                self.score += 1
                apple_eaten = True

        if apple_eaten:
            self.score_events(apple_list)
        else:
            self.snake.pop(0)

    def check_apple_contact(self, apple):
        if self.head == apple.get_cords():
            return True
        return False

    def check_death(self):
        if self.head in self.snake[0:-1]:
            return True
        if self.head[0] <= -1 or self.head[0] >= x_cells or self.head[1] <= -1 or self.head[1] >= y_cells:
            return True
        return False

    def check_win(self):
        if self.score >= (x_cells * y_cells) - 3:
            return True
        return False

class Apple:
    def __init__(self):
        self.x = randint(0, x_cells - 1)
        self.y = randint(0, y_cells - 1)
        self.color = [255, 0, 0]

    def render(self):
        pygame.draw.circle(screen, self.color,
                           (self.x * cell_size + cell_size // 2 + 1, self.y * cell_size + cell_size // 2 + 1),
                           cell_size // 2 - 3)
        pygame.draw.circle(screen, [180, 10, 10],
                           (self.x * cell_size + cell_size // 2 + 1, self.y * cell_size + cell_size // 2 + 1),
                           cell_size // 2 - 2, 2)

    def get_cords(self):
        return [self.x, self.y]

    def repose(self, snake):
        while [self.x, self.y] in snake:
            self.x = randint(1, x_cells - 1)
            self.y = randint(1, y_cells - 1)


def render_field():
    depth = 2
    for x in range(0, x_cells + 1):
        pygame.draw.line(screen, [0, 0, 0], [x * cell_size, 0], [x * cell_size, win_height], depth)
    for y in range(0, y_cells + 1):
        pygame.draw.line(screen, [0, 0, 0], [0, y * cell_size], [win_width, y * cell_size], depth)


def show_score(score):
    text = font.render(f"Score:{str(score).zfill(2)}", 1, (0, 0, 0), [144, 238, 144])
    text_pos = (text.get_rect(center=(win_width//2, win_height // 2 - 33)))

    screen.blit(text, text_pos)


def start_game():
    snek = Snake()
    apple_list = [Apple()]

    running_game = True
    while running_game:
        # обработка событий
        for e in pygame.event.get():
            if e.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running_game = False

        if pygame.key.get_pressed()[pygame.K_r]:
            snek = Snake()
            apple_list = [Apple()]

        if not snek.check_death() and not snek.check_win():
            screen.fill([153, 255, 153])

            for apple in apple_list:
                apple.render()

            snek.move(apple_list)
            snek.render()

            render_field()

            window.blit(screen, [0, 0])
        else:
            if snek.check_death():
                text = font.render("You Lose", 1, (0, 0, 0), [144, 238, 144])
            elif snek.check_win():
                text = font.render("You WIN!", 1, (0, 0, 0), [144, 238, 144])
            screen.blit(text, text.get_rect(center=(win_width//2, win_height // 2 - 70)))

            show_score(snek.get_score())

        window.blit(screen, [0, 0])
        pygame.display.flip()
        pygame.time.delay(100)

    pygame.display.set_caption("SneK menu")


if __name__ == "__main__":
    start_game()
