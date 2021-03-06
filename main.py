import engine.Sprite
import engine.active_wall
import minigames.finishedgame
import engine.minimap
from engine.network import Network
from engine.texture import Planning
from minigames.main_menu import Load_cicle, Settings
from settings import *

pygame.init()
screen = pygame.display.set_mode((width_screen, height_screen))
sc = Planning(screen)
# Инициализация загрузчика.
Loader = Load_cicle(screen)


def Menu_func(All, Mistake):
    """
    Запускает окно загрузки игры.
    Потом открывает главное меню.
    :return: Окно.
    """
    pygame.display.set_caption("DefusePro")
    Loader.main_menu_init()
    # Отрисовка меню.
    finished = False
    while not finished:

        screen.blit(Loader.LK, (0, -100))
        Loader.menu.draw()
        pygame.time.delay(60)
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                finished = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                is_one_of_buttons_on = Loader.menu.is_one_of_buttons_on()
                if is_one_of_buttons_on != -1:
                    Loader.audio.sound_play(Loader.audio.sound_if_button_down,
                                            sound_if_button_down_duration,
                                            Loader.audio.sound_if_button_down_start_time)
                    Loader.audio.sound_if_button_down_start_time \
                        = Loader.audio.check_sound(sound_if_button_down_duration,
                                                   Loader.audio.sound_if_button_down_start_time)
                    num_in_massive_of_buttoms_from_main_menu = is_one_of_buttons_on
                    indificate_func(num_in_massive_of_buttoms_from_main_menu, All, Mistake)
                    finished = True


def indificate_func(num_in_massive_of_buttoms, All, Mistake):
    """
    Проверяет, какая из кнопок была нажата и запускает команду соответствующую этой кнопке.
    :param num_in_massive_of_buttoms: Номер нажатой кнопки в массиве.
    :return: None
    """
    if num_in_massive_of_buttoms == 0:
        Main_game(All, Mistake)
    elif num_in_massive_of_buttoms == 1:
        Menu_of_settings(All, Mistake)


def Menu_of_settings(All, Mistake):
    """
    Рисует окно настроек.
    """
    finnish1 = False
    while not finnish1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                finnish1 = True
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE:
                    finnish1 = True
            elif i.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                Loader.audio.is_sounds_on = (Loader.set_win.points[0].is_point_down(mouse_position, 0))
                Loader.set_win.fractional_points[0].is_slider_down(mouse_position, 1)
        Loader.set_win.draw_set_win()
        pygame.time.delay(60)
        pygame.display.update()

    Menu_func(All, Mistake)


def redrawWindow(win, player, player2, ModelPlayer, text):
    '''
    :param win: экран
    :param player: основной игрок
    :param player2: второй игрок
    :param ModelPlayer: модель второго игрока
    :param text: объект текста с оставшимся временем в таймер
    :return: обновление экрана
    '''
    pressed_keys = pygame.key.get_pressed()
    sc.sky(player.angle)
    sprite_surf, sprite_rect = ModelPlayer.draw()
    sprites = (ModelPlayer.distance_to_player(), sprite_surf, sprite_rect)
    sc.plan(player.pos, player.angle, sprites)
    ModelPlayer.move(player2.x_player, player2.y_player)

    if pressed_keys[pygame.K_m]:
        engine.minimap.draw_minimap(player, screen)

    if pressed_keys[pygame.K_t]:
        surf1 = pygame.Surface((300, 120))
        surf1.fill(White)
        text_rect = text.get_rect(center=surf1.get_rect().center)
        surf1.fill(White)
        surf1.blit(text, text_rect)
        screen.blit(surf1, (0, 0))
    pygame.display.flip()


def wait(p, p2, n):
    '''
    :param p: Текущий игрок
    :param p2: Второй игрок
    :param n: сеть
    :return: Зал ожидания
    '''
    surf = pygame.Surface((width_screen, height_screen))
    surf.fill(White)
    f = pygame.font.SysFont('serif', 48)

    if p.status[2] == 1:
        text01 = 'Вы охранник.'
        text02 = '   Ваша задача найти методички.'
        text03 = '           И объяснить напарнику, что делать.'
        text04 = 'Запомните серийный номер, который вам сообщили:'
        text05 = str(sn)
        text3 = f.render(text04, False, Black)
        text4 = f.render(text05, False, Black)
        surf.blit(text3, (80, 370))
        surf.blit(text4, (450, 420))

    if p.status[2] == 2:
        text01 = 'Вы электрик.'
        text02 = 'Ваша задача найти модули бомбы.'
        text03 = 'И обезвредить их, следуя указаниям напарника.'

    text = f.render(text01, False, Black)
    text0 = f.render(text02, False, Black)
    text1 = f.render(text03, False, Black)
    text2 = f.render('Нажмите любую кнопку по готовности.', False, Black)
    surf.blit(text, (450, 200))
    surf.blit(text0, (270, 250))
    surf.blit(text1, (120, 300))
    surf.blit(text2, (190, 620))
    screen.blit(surf, (0, 0))
    pygame.display.update()

    while (p2.starts == False) or (p.starts == False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Menu_func(All, Mistake)
            if event.type == pygame.KEYDOWN:
                p.start = True
        p = n.getP()
        p2 = n.send(p)


def change_mod(p1, p2, event):
    """Меняет настроение охраннику (меняет спрайт).
    :param p1: текущий игрок
    :param p2: модель второго игрока
    :param event: событые
    """
    if ((p1.x_player - p2.x_pos) ** 2 + (p2.y_pos - p1.y_player) ** 2) ** (0.5) < distance_interaction \
            and event.type == pygame.KEYDOWN and event.key == pygame.K_g:
        p2.change_mood()


def Main_game(All, Mistake):
    pygame.display.set_caption("DefusePro")
    font = pygame.font.SysFont(None, 100)
    n = Network()
    p = n.getP()
    TimeAll = 0

    if type(p) == type(None):
        minigames.finishedgame.Fingame(3, TimeAll).manager()
        return 0

    p.sensitivity = Loader.set_win.fractional_points[0].parametr
    p2 = n.send(p)
    wait(p, p2, n)
    TimeAll = time.time()
    ModelPlayer = engine.Sprite.Guard(1, p2.x_player, p2.y_player, screen, p)

    while not All:
        pygame.time.Clock().tick(FPS)

        for event in pygame.event.get():
            change_mod(p, ModelPlayer, event)
            if event.type == pygame.QUIT:
                All = True
                p.change(True, 1)

        text = font.render(str(Time - round(time.time() - TimeAll)) + ' сек', True, Black)
        p.move()

        if p.is_player_move():
            Loader.audio.sound_play(Loader.audio.steps, steps_duration, Loader.audio.steps_start_time)
            Loader.audio.steps_start_time = Loader.audio.check_sound(steps_duration, Loader.audio.steps_start_time)

        redrawWindow(sc, p, p2, ModelPlayer, text)
        ro = engine.active_wall.active(minigames_set, p, Mistake, TimeAll)

        if type(ro) != type(None):
            minigames_set[int(ro[0]) - 1], Mistake = ro[1]

        if (Time - round(time.time() - TimeAll)) <= 0 or (Mistake > 3):
            All = True
            p.change(True, 1)
            p2 = n.send(p)
            minigames.finishedgame.Fingame(1, TimeAll).manager()

        try:
            minigames_set.index(0)
        except:
            All = True
            p.change(True, 2)
            p2 = n.send(p)
            minigames.finishedgame.Fingame(2, TimeAll).manager()

        if p2.status[0]:
            All = True
            minigames.finishedgame.Fingame(p2.status[1], TimeAll).manager()

        p2 = n.send(p)
    pygame.quit()


if __name__ == '__main__':
    Menu_func(All, Mistake)
