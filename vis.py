import pygame as pg
import game

# модуль визуализации с помощью библиотеки pygame

class Board(object):
    def __init__(self, light, dark):
        pg.init()
        pg.font.init()
        self.light = light
        self.dark = dark
        self.sc = pg.display.set_mode((700, 700))
        self.font = pg.font.SysFont('serif', 15)
        self.coord = {}
        self.squares = {}

    def field(self):
        self.sc.fill('black')
        pg.draw.rect(self.sc, self.light, (23, 123, 454, 454))
        pg.draw.rect(self.sc, self.dark, (25, 125, 450, 450))
        pg.draw.rect(self.sc, self.light, (48, 148, 404, 404))
        pg.draw.rect(self.sc, self.light, (120, 50, 260, 55), 3)
        for x in range(1, 9):
            for y in range(3, 11):
                color = self.light if (x + y) % 2 == 0 else self.dark
                pg.draw.rect(self.sc, color, (x * 50, y * 50, 50, 50))
                self.coord[y-3, x-1] = (x * 50, y * 50)
                self.squares[x * 50, y * 50] = (y - 3, x - 1)

    def f(self, s):
        return self.font.render(s, True, self.light)

    def ticks(self):
        self.sc.blit(pg.font.SysFont('serif', 30).render('Вернуть ход', True, self.light), (100 + 70, 60))
        for i, j in zip(range(1, 9), 'ABCDEFGH'):
            self.sc.blit(self.f(j), (i * 50 + 20, 127))
            self.sc.blit(self.f(j), (i * 50 + 20, 553))
        for i, j in zip(range(3, 11), '87654321'):
            self.sc.blit(self.f(j), (32, i * 50 + 20))
            self.sc.blit(self.f(j), (460, i * 50 + 20))


g = game.Game()


class Pieces(Board):
    def __init__(self, light, dark):
        super().__init__(light, dark)
        self.boards = g.boards
        self.possible = []

    def fill(self):
        p = {'bP', 'bR', 'bN', 'bB', 'bK', 'bQ', 'wP', 'wR', 'wN', 'wB', 'wK', 'wQ'}
        images = {i: pg.transform.smoothscale(pg.image.load(f'pieces//{i}.png'), (50, 50)).convert_alpha() for i in p}
        for line in range(8):
            for square in range(8):
                if self.boards[-1][line, square].strip():
                    rect = images[self.boards[-1][line, square]].get_rect()
                    rect = rect.move(self.coord[line, square])
                    self.sc.blit(images[self.boards[-1][line, square]], rect)
        y = 100
        x = 500
        for i, j in zip(range(len(g.notation)), g.notation):
            y += 20
            if y <= 600:
                self.sc.blit(self.f(j), (x, y))
            else:
                x += 80
                y = 120
                self.sc.blit(self.f(j), (x, y))


screen = Pieces('white', 'black')
squares = {x: y for y, x in screen.coord.items()}
move = []
choose = False
while True:
    screen.field()
    screen.ticks()
    screen.fill()
    pg.display.update()
    if len(move) > 4:
        move = move[4:]
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if all(i < j < (k + 50) for i, j, k in zip(screen.coord[0, 0], event.pos, screen.coord[7, 7])):
                move += (screen.squares[tuple(map(lambda x: x // 50 * 50, event.pos))])
            elif 120 < event.pos[0] < 380 and 50 < event.pos[1] < 115:
                g.back()
                move = []
            else:
                move = []
    if len(move) == 4:
        g.move(*move)
        move = []
