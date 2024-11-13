import itertools as it
import numpy as np

# модуль создания списков возможных ходов фигурами

class All(object):
    def __init__(self):
        self.white = []
        self.black = []

    @staticmethod
    def get_piece(s1, s2, m):   # определение фигуры
        d = {'P': 'Pawn', 'R': 'Rook', 'N': 'Knight', 'B': 'Bishop', 'Q': 'Queen', 'K': 'King'}
        return d.get(m[s1, s2][-1])

    def col(self, m, ep):   # воздание списков всех возможных ходов белых и чёрных для шаха и мата
        for i in range(8):
            for j in range(8):
                piece = self.get_piece(i, j, m)
                if piece:
                    p = globals()[piece]()
                    p.check(i, j, m, ep)
                    if piece == 'Pawn':
                        p.possible = [(n, k) for n, k in p.possible if k != j]
                    if 'w' in m[i, j]:
                        self.white += p.possible
                    else:
                        self.black += p.possible


class Pieces(All):
    def __init__(self):
        super().__init__()
        self.possible = []
        self.all_b = []
        self.all_w = []
        self.wK = ()
        self.bK = ()

    def find_kings(self, m):   # нахождение позиции королей
        for i in range(8):
            for j in range(8):
                if m[i, j] == 'wK':
                    self.wK = i, j
                elif m[i, j] == 'bK':
                    self.bK = i, j

    def edit(self, s1, s2, m, ep):   # редактирование возможных ходов, учитывая шахи и маты
        c = m[s1, s2][0]
        for i in list(self.possible):
            a = np.copy(m)
            a[i] = a[s1, s2]
            a[s1, s2] = '  '
            self.find_kings(a)
            self.col(a, ep)
            if (c == 'b' and self.bK in self.white) or (c == 'w' and self.wK in self.black):
                self.possible.remove(i)



# у всех классов ниже одинаковая структура: функция check созда1т список возможных ходов из данной позиции
class Pawn(Pieces):
    def __init__(self):
        super().__init__()

    def check(self, s1, s2, m, ep):
        if 'w' in m[s1, s2] and s1 > 0:
            if not m[s1 - 1, s2].strip():
                self.possible.append((s1 - 1, s2))
            if s1 == 6 and not m[s1 - 2, s2].strip():
                self.possible.append((s1 - 2, s2))
            if s2 > 0 and 'b' in m[s1 - 1, s2 - 1]:
                self.possible.append((s1 - 1, s2 - 1))
            if s2 < 7 and 'b' in m[s1 - 1, s2 + 1]:
                self.possible.append((s1 - 1, s2 + 1))
            if (s1, s2+1) == ep:
                self.possible.append((s1 - 1, s2 + 1))
            if (s1, s2-1) == ep:
                self.possible.append((s1 - 1, s2 - 1))
        if 'b' in m[s1, s2] and s1 < 7:
            if not m[s1 + 1, s2].strip():
                self.possible.append((s1 + 1, s2))
            if s1 == 1 and not m[s1 + 2, s2].strip():
                self.possible.append((s1 + 2, s2))
            if s2 < 7 and 'w' in m[s1 + 1, s2 + 1]:
                self.possible.append((s1 + 1, s2 + 1))
            if s2 > 0 and 'w' in m[s1 + 1, s2 - 1]:
                self.possible.append((s1 + 1, s2 - 1))
            if (s1, s2+1) == ep:
                self.possible.append((s1 + 1, s2 + 1))
            if (s1, s2-1) == ep:
                self.possible.append((s1 + 1, s2 - 1))


class Rook(Pieces):
    def __init__(self):
        super().__init__()

    def check(self, s1, s2, m, ep):
        n1, n2 = s1, s2
        while n1 < 7 and not m[n1 + 1, n2].strip():
            self.possible.append((n1 + 1, n2))
            n1 += 1
        if n1 < 7 and 'w' in m[s1, s2] and 'b' in m[n1 + 1, n2]:
            self.possible.append((n1 + 1, n2))
        elif n1 < 7 and 'b' in m[s1, s2] and 'w' in m[n1 + 1, n2]:
            self.possible.append((n1 + 1, n2))
        n1 = s1

        while n1 > 0 and not m[n1 - 1, n2].strip():
            self.possible.append((n1 - 1, n2))
            n1 -= 1
        if n1 > 0 and 'w' in m[s1, s2] and 'b' in m[n1 - 1, n2]:
            self.possible.append((n1 - 1, n2))
        elif n1 > 0 and 'b' in m[s1, s2] and 'w' in m[n1 - 1, n2]:
            self.possible.append((n1 - 1, n2))
        n1 = s1

        while n2 < 7 and not m[n1, n2 + 1].strip():
            self.possible.append((n1, n2 + 1))
            n2 += 1
        if n2 < 7 and 'w' in m[s1, s2] and 'b' in m[n1, n2 + 1]:
            self.possible.append((n1, n2 + 1))
        elif n2 < 7 and 'b' in m[s1, s2] and 'w' in m[n1, n2 + 1]:
            self.possible.append((n1, n2 + 1))
        n2 = s2

        while n2 > 0 and not m[n1, n2 - 1].strip():
            self.possible.append((n1, n2 - 1))
            n2 -= 1
        if n2 > 0 and 'w' in m[s1, s2] and 'b' in m[n1, n2 - 1]:
            self.possible.append((n1, n2 - 1))
        elif n2 > 0 and 'b' in m[s1, s2] and 'w' in m[n1, n2 - 1]:
            self.possible.append((n1, n2 - 1))


class Bishop(Pieces):
    def __init__(self):
        super().__init__()

    def check(self, s1, s2, m, ep):
        n1, n2 = s1, s2
        while n1 < 7 and n2 < 7 and not m[n1 + 1, n2 + 1].strip():
            self.possible.append((n1 + 1, n2 + 1))
            n1 += 1
            n2 += 1
        if n1 < 7 and n2 < 7 and 'w' in m[s1, s2] and 'b' in m[n1 + 1, n2 + 1]:
            self.possible.append((n1 + 1, n2 + 1))
        elif n1 < 7 and n2 < 7 and 'b' in m[s1, s2] and 'w' in m[n1 + 1, n2 + 1]:
            self.possible.append((n1 + 1, n2 + 1))
        n1 = s1
        n2 = s2

        while n1 > 0 and n2 > 0 and not m[n1 - 1, n2 - 1].strip():
            self.possible.append((n1 - 1, n2 - 1))
            n1 -= 1
            n2 -= 1
        if n1 > 0 and n2 > 0 and 'w' in m[s1, s2] and 'b' in m[n1 - 1, n2 - 1]:
            self.possible.append((n1 - 1, n2 - 1))
        elif n1 > 0 and n2 > 0 and 'b' in m[s1, s2] and 'w' in m[n1 - 1, n2 - 1]:
            self.possible.append((n1 - 1, n2 - 1))
        n1 = s1
        n2 = s2

        while n1 < 7 and n2 > 0 and not m[n1 + 1, n2 - 1].strip():
            self.possible.append((n1 + 1, n2 - 1))
            n1 += 1
            n2 -= 1
        if n1 < 7 and n2 > 0 and 'w' in m[s1, s2] and 'b' in m[n1 + 1, n2 - 1]:
            self.possible.append((n1 + 1, n2 - 1))
        elif n1 < 7 and n2 > 0 and 'b' in m[s1, s2] and 'w' in m[n1 + 1, n2 - 1]:
            self.possible.append((n1 + 1, n2 - 1))
        n1 = s1
        n2 = s2

        while n1 > 0 and n2 < 7 and not m[n1 - 1, n2 + 1].strip():
            self.possible.append((n1 - 1, n2 + 1))
            n1 -= 1
            n2 += 1
        if n1 > 0 and n2 < 7 and 'w' in m[s1, s2] and 'b' in m[n1 - 1, n2 + 1]:
            self.possible.append((n1 - 1, n2 + 1))
        elif n1 > 0 and n2 < 7 and 'b' in m[s1, s2] and 'w' in m[n1 - 1, n2 + 1]:
            self.possible.append((n1 - 1, n2 + 1))


class Queen(Pieces):
    def __init__(self):
        super().__init__()

    def check(self, s1, s2, m, ep):
        r = Rook()
        r.check(s1, s2, m, ep)
        b = Bishop()
        b.check(s1, s2, m, ep)
        self.possible += r.possible + b.possible


class Knight(Pieces):
    def __init__(self):
        super().__init__()

    def check(self, s1, s2, m, ep):
        for i, j in filter(lambda x: abs(x[0]) != abs(x[1]), it.permutations([1, 2, -1, -2], 2)):
            if 0 <= (s1+i) <= 7 and 0 <= (s2+j) <= 7:
                if not m[s1+i, s2+j].strip():
                    self.possible.append((s1+i, s2+j))
                if 'w' in m[s1, s2] + m[s1+i, s2+j] and 'b' in m[s1, s2] + m[s1+i, s2+j]:
                    self.possible.append((s1 + i, s2 + j))


class King(Pieces):
    def __init__(self):
        super().__init__()

    @staticmethod
    def near(s1, s2, m):
        ind = [(s1 + i, s2 + j) for i, j in it.product([1, 0, -1], repeat=2)
               if all([0 <= s1 + i <= 7, 0 <= s2 + j <= 7])]
        return [m[i, j] for i, j in ind]

    def check(self, s1, s2, m, ep):
        color = m[s1, s2][0]
        for i, j in it.product([1, 0, -1], repeat=2):
            if 0 <= (s1+i) <= 7 and 0 <= (s2+j) <= 7:
                if not (i == 0 and j == 0):
                    a = np.copy(m)
                    a[s1 + i, s2 + j] = f'{color}K'
                    a[s1, s2] = '  '
                    if color == 'w' and 'bK' not in self.near(s1+i, s2+j, m):
                        if not m[s1 + i, s2 + j].strip() or 'b' in m[s1 + i, s2 + j]:
                            self.possible.append((s1 + i, s2 + j))
                    elif color == 'b' and 'wK' not in self.near(s1+i, s2+j, m):
                        if not m[s1 + i, s2 + j].strip() or 'w' in m[s1 + i, s2 + j]:
                            self.possible.append((s1 + i, s2 + j))
                    if s1 == 7 and s2 == 4:
                        if not ''.join(m[s1, s2+1:s2+3]).strip() and m[7, 7] == 'wR':
                            self.possible.append((7, 6))
                        if not ''.join(m[s1, s2-1:s2-4]).strip() and m[7, 0] == 'wR':
                            self.possible.append((7, 2))
                    elif s1 == 0 and s2 == 4:
                        if not ''.join(m[s1, s2+1:s2+3]).strip() and m[0, 7] == 'bR':
                            self.possible.append((0, 6))
                        if not ''.join(m[s1, s2-1:s2-4]).strip() and m[0, 0] == 'bR':
                            self.possible.append((0, 2))

