from tile import Tile

PROMOTIONS = {-1: 0, 1: 7}

class Checker:
    '''
    Визначає шашку за її місцем положення

    Аргументи:
    tile: клітинка, на якій перебуває шашка
    '''
    def __init__(self, x: int, y: int):
        self.tile = Tile(x, y)

    def __repr__(self):
        return f'Checker {self.tile}'
    

class Queen(Checker):
    '''
    Визначає дамку за її місцем перебування

    Батьківський клас: Checker

    Аргументи:
    tile: клітинка, на якій перебуває дамка
    '''
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def __repr__(self):
        return f'Queen {self.tile}'


def default_board()->dict:
    '''
    Метод для створення звичайної початкової дошки

    Повертає
    dict: початковий список всіх шашок
    '''
    return {-1: [Checker(0, 5), Checker(2, 5), Checker(4, 5), Checker(6, 5), \
                 Checker(1, 6), Checker(3, 6), Checker(5, 6), Checker(7, 6), \
                 Checker(0, 7), Checker(2, 7), Checker(4, 7), Checker(6, 7)], \
            +1: [Checker(1, 2), Checker(3, 2), Checker(5, 2), Checker(7, 2), \
                 Checker(0, 1), Checker(2, 1), Checker(4, 1), Checker(6, 1), \
                 Checker(1, 0), Checker(3, 0), Checker(5, 0), Checker(7, 0)]}

class Board:
    '''
    Визначає ігрову дошку, а також виконує на ній всі ходи та перевірки
    Гравці визначаються числами:
    білий  = -1
    чорний = +1

    Аргументи:
    board: визначає початкове розташування усіх шашок.
           Створюється у вигляді наступного dict: {-1: [білі шашки], 1: [чорні шашки]} 
    player_to_move: визначає гравця, котрий ходить першим. По замовчуванню білі (-1)
    possible_attacker: визначає шашку, котра може робити хід.
                       Використовується лише для атак де забирається більше 1 шашки
    winner: визначає переможця гри.
    '''
    def __init__(self, board: dict = None, player_to_move: int = -1):
        if board == None:
            self.board = default_board()
        else:
            self.board = board
        self.player_to_move = player_to_move
        self.possible_attacker = None
        self.winner = 0

    def checker_on_tile(self, tile: Tile)->list:
        '''
        Перевіряє наявність шашки на заданій клітинці

        Параметри:
        tile: клітинка, на якій перевіряється наявність шашки.

        Повертає:
        list: список [0], якщо шашки на клітинці немає, або список у вигляді [власник_шашки, шашка]
        '''
        for checker_to_check in self.board[1]:
            if checker_to_check.tile.equals(tile):
                return [1, checker_to_check]
        for checker_to_check in self.board[-1]:
            if checker_to_check.tile.equals(tile):
                return [-1, checker_to_check]
        return [0]

    def promote(self, checker_to_promote: Checker)->Queen:
        '''
        Виконує переведення шашки в дамку

        Параметри:
        checker_to_promote: шашка, яку переводимо в дамку

        Повертає:
        queen: дамка, в яку перетворилась ця шашка
        '''
        queen = Queen(checker_to_promote.tile.x, checker_to_promote.tile.y)
        self.board[self.player_to_move].remove(checker_to_promote)
        self.board[self.player_to_move].append(queen)
        return queen

    def premove(self):
        '''
        Виконує необхідні умови перед початком ходу:
        1) Передає хід наступному гравцеві
        2) Визначає чи цей гравець може походити
        '''
        self.possible_attacker = None
        self.player_to_move = -self.player_to_move
        if not self.move_is_possible():
            self.winner = -self.player_to_move

    def queens_take_possible(self, queens_tile: Tile, empty_tile: Tile = Tile(-2, -2))->bool:
        '''
        Визначає чи може дамка здійснити бій з клітинки queens_tile, ігноруючи фігуру на empty_tile

        Параметри:
        queens_tile: клітинка, для якої здійснюємо перевірку
        empty_tile: клітинка, фігуру на якій треба ігнорувати

        Повертає:
        bool: True, якщо бій можливий
              False, інакше
        '''
        for diag in [(-1,  -1), (-1, 1), (1, -1), (1, 1)]:
            tile_ = queens_tile + diag
            while (self.checker_on_tile(tile_) == [0] or tile_ == empty_tile) and tile_.is_valid():
                tile_ += diag
            if self.checker_on_tile(tile_)[0] == -self.player_to_move and tile_.is_valid():
                tile_ += diag
                if self.checker_on_tile(tile_) == [0] and tile_.is_valid():
                    return True
        return False

    def take_possible(self)->bool:
        '''
        Перевіряє чи є можливим бій для поточної дошки.

        Повертає:
        True:  якщо хоча б один бій можливий
        False: інакше
        '''
        if self.possible_attacker == None:
            attackers = self.board[self.player_to_move]
        else:
            attackers = [self.possible_attacker]
        for checker_to_check in attackers:
            if isinstance(checker_to_check, Queen):
                if self.queens_take_possible(checker_to_check.tile):
                    return True
            else:
                for tile_ in checker_to_check.tile.all_adjacent():
                    if self.checker_on_tile(tile_)[0] == -self.player_to_move:
                        x = tile_ * 2 - checker_to_check.tile
                        if self.checker_on_tile(x) == [0] and x.is_valid():
                            return True
        return False

    def take(self, toctm: Tile, tile_to_move: Tile)->bool:
        '''
        Виконує бій шашкою, що знаходиться на toctm (Tile Of Checker To Move) і поміщає її на tile_to_move.

        Параметри:
        toctm: клітинка, на якій знаходиться шашка, яка повинна виконувати бій
        tile_to_move: клітинка, на яку ця шашка має стати

        Повертає:
        True:  бій виконано успішно і можливий ще один бій
        False: бій виконано успішно і ще один бій неможливий
        None:  бій не виконано (неправильно обрана клітинка, нема кого бити і т.п.)
        '''
        if self.take_possible():
            if self.checker_on_tile(tile_to_move) != [0]:
                return None
            checker_to_move = self.checker_on_tile(toctm)[1]
            if isinstance(checker_to_move, Queen):
                if toctm.on_same_diagonal(tile_to_move):
                    diag = tile_to_move.diagonal_unit(toctm)
                    victim_tile = None
                    test_tile = toctm + diag
                    while not test_tile.equals(tile_to_move):
                        if self.checker_on_tile(test_tile)[0] == self.player_to_move:
                            return None
                        if self.checker_on_tile(test_tile)[0] == -self.player_to_move:
                            if victim_tile != None:
                                return None
                            else:
                                victim_tile = test_tile
                        test_tile += diag
                    if victim_tile == None:
                        return None
                    if not self.queens_take_possible(tile_to_move, victim_tile):
                        tile_to_test = victim_tile + diag
                        while self.checker_on_tile(tile_to_test) == [0] and tile_to_test.is_valid():
                            if self.queens_take_possible(tile_to_test, victim_tile):
                                return None
                            tile_to_test += diag
                    checker_to_move.tile = tile_to_move
                    self.board[-self.player_to_move].remove(self.checker_on_tile(victim_tile)[1])
                    self.possible_attacker = checker_to_move
                    if not self.take_possible():
                        self.premove()
                        return False
                    return True
            else:
                if not self.possible_attacker == None:
                    if not checker_to_move.tile.equals(self.possible_attacker.tile):
                        return None
                if not toctm.on_same_diagonal(tile_to_move):
                    return None
                diag = tile_to_move.diagonal_unit(toctm)
                if not (toctm + diag * 2).equals(tile_to_move):
                    return None
                if self.checker_on_tile(toctm + diag)[0] == -self.player_to_move:
                    checker_to_move.tile = tile_to_move
                    if checker_to_move.tile.y == PROMOTIONS[self.player_to_move]:
                        checker_to_move = self.promote(checker_to_move)
                    self.board[-self.player_to_move].remove(self.checker_on_tile(toctm + diag)[1])
                    self.possible_attacker = checker_to_move
                    if not self.take_possible():
                        self.premove()
                        return False
                    return True

    def move_is_possible(self)->bool:
        '''
        Перевіряє можливість ходу гравця (включно з боєм)

        Повертає:
        True:  хід можливий
        False: хід неможливий, у цьому випадку гравець програє гру
        '''
        if self.take_possible():
            return True
        if len(self.board[self.player_to_move]) != 0:
            for checker_to_check in self.board[self.player_to_move]:
                if isinstance(checker_to_check, Queen):
                    for diag in [(-1,  -1), (-1, 1), (1, -1), (1, 1)]:
                        tile_to_check = checker_to_check.tile + diag
                        if tile_to_check.is_valid() and self.checker_on_tile(tile_to_check) == [0]:
                            return True
                else:
                    for adj in checker_to_check.tile.all_adjacent(self.player_to_move):
                        if self.checker_on_tile(adj) == [0]:
                            return True
        self.winner = -self.player_to_move
        return False

    def move(self, toctm: Tile, tile_to_move: Tile)->bool:
        '''
        Виконує хід (не бій) шашкою, що знаходиться на toctm (Tile Of Checker To Move) і поміщає її на tile_to_move.

        Параметри:
        toctm: клітинка, на якій знаходиться шашка, яка повинна виконувати хід
        tile_to_move: клітинка, на яку ця шашка має стати

        Повертає:
        True: хід виконано
        None: хід не виконано (нелегітимний)
        '''
        checker_to_move = self.checker_on_tile(toctm)[1]
        if isinstance(checker_to_move, Queen):
            if toctm.on_same_diagonal(tile_to_move):
                diag = tile_to_move.diagonal_unit(toctm)
                tile_to_check = toctm + diag
                while (not tile_to_check.equals(tile_to_move)) and self.checker_on_tile(tile_to_check) == [0]:
                    tile_to_check += diag
                if tile_to_check.equals(tile_to_move):
                    checker_to_move.tile = tile_to_move
                    self.premove()
                    return True
        else:
            pos = False
            for tile_ in toctm.all_adjacent(self.player_to_move):
                if tile_.equals(tile_to_move):
                    pos = True
                    break
            if not pos:
                return None 
            if self.checker_on_tile(tile_to_move) == [0]:
                checker_to_move.tile = tile_to_move
                if checker_to_move.tile.y == PROMOTIONS[self.player_to_move]:
                        checker_to_move = self.promote(checker_to_move)
                self.premove()
                return True
