import numpy as np
import engine.map
from settings import *
from engine.ray_casting import mapping


class Player:
    '''
    Класс игрока
    :param player_pos:  Координаты игрока в кортеже
    :param role:  Роль игрока
    :param angle:  Угол поворота камеры
    :param finish:  Завершена ли игра
    :param typefin:  Тип концовки
    :param start:  Статус начала игры
    :param sensitivity: Чувствительность поворота
    '''

    def __init__(self, player_pos, role):
        self.x_player, self.y_player = player_pos
        self.angle = player_angle
        self.finish = False
        self.typefin = 1
        self.role = role
        self.start = False
        self.sensitivity = 0

    def audio_init(self, audio):
        self.audio = audio

    def change(self, s, t):
        self.finish = s
        self.typefin = t

    def sound_of_steps(self):
        '''
        Включает звук ходьбы для персонажа.
        :return: звук.
        '''
        self.audio.Sound_play(self.audio.steps, steps_duration, self.audio.steps_start_time)
        self.audio.steps_start_time = self.audio.check_sound(steps_duration, self.audio.steps_start_time)

    @property
    def pos(self):
        '''
        :return: Позиция игрока
        '''
        return int(self.x_player), int(self.y_player)

    @property
    def status(self):
        '''
        :return: Состояние игрока
        '''
        return (self.finish, self.typefin, self.role)

    @property
    def starts(self):
        '''
        :return: Готов ли игрок
        '''
        return self.start

    def move(self):
        '''
        :return: Движение игрока
        '''
        pressed_keys = pygame.key.get_pressed()
        self.is_move = False
        self.Vy = player_speed * np.cos(self.angle)
        self.Vx = player_speed * np.sin(self.angle)

        if (pressed_keys[pygame.K_w] or pressed_keys[pygame.K_s]) \
                and (pressed_keys[pygame.K_a] or pressed_keys[pygame.K_d]):
            self.Vx *= 1 / (2 ** 0.5)
            self.Vy *= 1 / (2 ** 0.5)

        if pressed_keys[pygame.K_LSHIFT]:
            self.Vy *= 2
            self.Vx *= 2

        if pressed_keys[pygame.K_a]:
            self.x_player, self.y_player = self.__mover_player__(self.x_player, self.Vx,
                                                                 self.y_player, -1 * self.Vy)
        if pressed_keys[pygame.K_d]:
            self.x_player, self.y_player = self.__mover_player__(self.x_player, -1 * self.Vx,
                                                                 self.y_player, self.Vy)
        if pressed_keys[pygame.K_s]:
            self.x_player, self.y_player = self.__mover_player__(self.x_player, -1 * self.Vy,
                                                                 self.y_player, -1 * self.Vx)
        if pressed_keys[pygame.K_w]:
            self.x_player, self.y_player = self.__mover_player__(self.x_player, self.Vy,
                                                                 self.y_player, self.Vx)
        if pressed_keys[pygame.K_RIGHT]:
            self.angle += player_angle_change_speed * (1 + self.sensitivity / 100)
        if pressed_keys[pygame.K_LEFT]:
            self.angle -= player_angle_change_speed * (1 + self.sensitivity / 100)

    def is_player_in_colader(self, cord_x, Vx, cord_y, Vy):
        '''
        Проверяет, попадет ли игрок в следующем кадре в текстуры.
        :param cord_x  и cord_y:  Координаты, по которым считается перемещение.
        :param Vx и Vy: - Скорости по данным коодринатам.
        :return: Возращает скорочти по координатам cord_x и cord_yю
        '''
        Vx_m = collader_of_player * Vx / math.fabs(Vx)
        Vy_m = collader_of_player * Vy / math.fabs(Vy)
        m_x = mapping(cord_x + Vx_m, cord_y)  # Создает кортеж координат.
        m_y = mapping(cord_x, cord_y + Vy_m)  # Создает кортеж координат.
        m_d = mapping(cord_x + Vx_m // 9, cord_y + Vy_m // 9)
        map, active_map = engine.map.map_create(engine.map.text_map)
        if m_x in map:
            Vx = 0
        if m_y in map:
            Vy = 0
        if m_d in map and not (m_x in map and m_y in map):
            Vx = 0
            Vy = 0
        return Vx, Vy

    def __mover_player__(self, cord_x, Vx, cord_y, Vy):
        '''
        Меняет координаты игрока.
        Проверяет, может ли он идти дальше (проверка на текстутры).
        Меняет переменную, в которой отмечено, есть ли движение.
        :param cord_x и cord_y:  Координаты, по которым считается перемещение.
        :param Vx и Vy: - Скорости по данным коодринатам.
        :return: Новую коодринату.
        '''
        self.is_move = True
        Vx, Vy = self.is_player_in_colader(cord_x, Vx, cord_y, Vy)
        cord_x += Vx
        cord_y += Vy
        return cord_x, cord_y

    def is_player_move(self):
        """
        Проверяет движентся ли игрок.
        :return: True, если игрок движется, иаче False.
        """
        return self.is_move
