class Tile:
    '''
    Визначає клітинку ігрової дошки

    Аргументи:
    x: індекс стовпця клітинки
    y: індекс рядка клітинки
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        # return f"{chr(97 + self.x)}{8 - self.y}" - офіційна нотація, з нею багато мороки і складний дебаг
        return f'<{self.x}, {self.y}>'

    def __add__(self, other: Tile)->Tile:
        '''
        __add__(self, other: tuple)->Tile

        Додає дві клітинки шляхом додавання відповідних координат
        '''
        if isinstance(other, Tile):
            return Tile(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple):
            return Tile(self.x + other[0], self.y + other[1])

    def __sub__(self, other: Tile)->Tile:
        '''
        __sub__(self, other: tuple)->Tile

        Віднімає одну клітинку від іншої шляхом віднімання відповідних координат
        '''
        if isinstance(other, Tile):
            return Tile(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple):
            return Tile(self.x - other[0], self.y - other[1])

    def __mul__(self, number: int)->Tile:
        '''Множить усі координати клітинки на число number'''
        return Tile(int(self.x * number), int(self.y * number))

    def equals(self, other: Tile)->bool:
        '''
        Перевіряє чи є дві задані клітинки рівні між собою (по координатам)

        Повертає:
        True: у разі рівності відповідних координат
        False: інакшу
        '''
        return self.x == other.x and self.y == other.y

    def is_valid(self: Tile)->bool:
        '''
        Перевіряє чи знаходиться задана клітинка в межах дошки

        Повертає:
        True:  клітинка знаходиться в межах дошки
        False: інакше
        '''
        return self.x >= 0 and self.x <= 7 and self.y >= 0 and self.y <= 7

    def all_adjacent(self, direction: int = 0)->list:
        '''
        Створює список з усіх клітинок в межах дошки, сусідних по діагоналі до заданої
        
        Параметри:
        direction: визначає напрям, в якому шукаємо необхідні нам клітинки.
                   Можливі значення:
                    0:  Будь-який напрямок
                    1:  Напрямок, в якому друга координата шуканих клітинок більша від другої координати заданої
                    -1: Напрямок, в якому друга координата шуканих клітинок менша від другої координати заданої
                   Будь-яке інше значення direction спричинить помилку
        Повертає:
        list: список усіх клітинок, що задовільняють критерії сусідства і напрямку
        '''
        if direction not in [-1, 0, 1]:
            raise ValueError(f"Impossible value of 'direction' ({direction}), has to be either -1, 0, or 1.")
        y_increase = [-1, 1] if direction == 0 else [direction]
        return [self + (i, j) for i in [-1, 1] for j in y_increase if (self + (i, j)).is_valid()]

    def on_same_diagonal(self, other: Tile)->bool:
        '''
        Перевіряє чи є дві задані клітинки на одній і тій самій діагоналі

        Повертає:
        True:  якщо self і other знаходяться на одній діагоналі
        False: інакше
        '''
        return abs(self.x - other.x) == abs(self.y - other.y)

    def diagonal_unit(self, other: Tile)->Tile:
        '''
        Створює Tile з одиничними координатами в напрямку від other до self

        Повертає:
        Tile: клітинку з координатами ((-)1, (-)1) в напрямку від other до self
        '''
        if not self.on_same_diagonal(other):
            raise ValueError("Tiles have to be on same diagonal")
        a = abs(self.x - other.x)
        return Tile((self.x - other.x) // a, (self.y - other.y) // a)

    # В коді не використовується
    def same_diagonal(self, right: int = 1, down: int = 1)->list:
        '''Створює список усіх клітинок по діагоналі у вказаному напрямку відносно вказаної клітинки'''
        if right not in [-1, 1]:
            raise ValueError(f"Impossible value of 'right' ({right}), has to be either -1 or 1")
        if down not in [-1, 1]:
            raise ValueError(f"Impossible value of 'down' ({down}), has to be either -1 or 1")
        result = []
        tile_ = self + (right, down)
        while tile_.is_valid():
            result.append(tile_)
            tile_ += (right, down)
        return result
