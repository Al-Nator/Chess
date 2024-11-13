import numpy as np
from logic import *
import copy

# Класс (и модуль), отвечающий за изменения доски при ходе (за сам процесс)

class Game(object):
    def __init__(self):
        super().__init__()
        self.take = np.array([
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ])   # начальная доска
        self.moves = 0   # подсчёт ходов
        self.boards = [copy.deepcopy(self.take)]   # запоминание всех позицый
        self.notation = []   # нотация
        self.en_passant = ()   # возможность взятия на проходе

    def back(self):   # функция возврата хода
        self.boards[0] = np.array([
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ])
        if len(self.boards) > 1:   # откат кол-ва ходов, нотации, и присваивание текущей доске предыдущей позиции
            self.boards.pop()
            self.moves -= 1
            self.notation.pop()
            self.take = self.boards[-1]
        print(self.boards)

    def get_piece(self, s1, s2):   # определение фигуры по букве
        d = {'P': 'Pawn', 'R': 'Rook', 'N': 'Knight', 'B': 'Bishop', 'Q': 'Queen', 'K': 'King'}
        return d.get(self.take[s1, s2][-1])

    def move(self, s1, s2, g1, g2):   # функция для изменения доски при ходе
        turn = {0: 'white', 1: 'black'}
        letters = 'abcdefgh'
        piece = self.get_piece(s1, s2)
        if piece and turn[self.moves % 2][0] == self.take[s1, s2][0]:
            p = globals()[piece]()   # создания класса из модуля logic по названию фигуры
            p.check(s1, s2, self.take, self.en_passant)   # создание списка возможеых ходов для фигуры
            p.edit(s1, s2, self.take, self.en_passant)   # редактирование возможных ходов, учитывая шахи и маты
            if piece == 'King' and abs(g2 - s2) > 1 and (g1, g2) in p.possible:   # реализация рокировки
                self.take[g1, g2] = self.take[s1, s2]
                self.take[s1, s2] = '  '
                if (g1, g2) == (7, 6):
                    self.take[7, 5] = self.take[7, 7]
                    self.take[7, 7] = '  '
                elif (g1, g2) == (7, 2):
                    self.take[7, 3] = self.take[7, 0]
                    self.take[7, 0] = '  '
                elif (g1, g2) == (0, 2):
                    self.take[0, 3] = self.take[0, 0]
                    self.take[0, 0] = '  '
                elif (g1, g2) == (0, 6):
                    self.take[0, 5] = self.take[0, 7]
                    self.take[0, 7] = '  '
                self.boards.append(copy.deepcopy(self.take))
                self.moves += 1
                self.notation += [f'{self.moves}: {letters[s2]}{8 - s1}-{letters[g2]}{8 - g1}']
            elif piece == 'Pawn' and (g1, g2) in p.possible and g2 != s2 and not self.take[g1, g2].strip():
                # реализация взятия на проходе
                if (g1, g2) == (s1-1, s2+1):
                    self.take[g1, g2] = self.take[s1, s2]
                    self.take[s1, s2 + 1] = '  '
                    self.take[s1, s2] = '  '
                elif (g1, g2) == (s1-1, s2-1):
                    self.take[g1, g2] = self.take[s1, s2]
                    self.take[s1, s2 - 1] = '  '
                    self.take[s1, s2] = '  '
                elif (g1, g2) == (s1+1, s2+1):
                    self.take[g1, g2] = self.take[s1, s2]
                    self.take[s1, s2 + 1] = '  '
                    self.take[s1, s2] = '  '
                else:
                    self.take[g1, g2] = self.take[s1, s2]
                    self.take[s1, s2 - 1] = '  '
                    self.take[s1, s2] = '  '
                self.boards.append(copy.deepcopy(self.take))
                self.moves += 1
                self.notation += [f'{self.moves}: {letters[s2]}{8 - s1}-{letters[g2]}{8 - g1}']
            elif (g1, g2) in p.possible:   # изменения возможности взятия на проходе
                if piece == 'Pawn' and abs(g1 - s1) == 2:
                    self.en_passant = (g1, g2)
                else:
                    self.en_passant = ()
                if piece == 'Pawn' and (g1 == 7 or g1 == 0):   # превращение пешки
                    if self.moves % 2 == 0:
                        self.take[g1, g2] = 'wQ'
                        self.take[s1, s2] = '  '
                    else:
                        self.take[g1, g2] = 'bQ'
                        self.take[s1, s2] = '  '
                else:
                    self.take[g1, g2] = self.take[s1, s2]
                    self.take[s1, s2] = '  '
                self.boards.append(copy.deepcopy(self.take))   # добавление текущей доски в список
                self.moves += 1   # увеличение количества ходов
                self.notation += [f'{self.moves}: {letters[s2]}{8 - s1}-{letters[g2]}{8 - g1}']   # добавление хода в
                # нотацию





