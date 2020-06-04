import os
import string
import pygame as pg

from shapes import Shapes
from config import config
from score import Score
from color import colors, ColorEffect


score = Score()
shape = Shapes()
next_shape = Shapes()
color_effect = ColorEffect(length=15)

class Button():
    # інформація про майбутні дії користувача
    def get_Button(self):
        pass

class Button_interface(Button):
    def __init__(self, key, function, draw_on):

        self.key = key

        # Положення та розміри кнопки
        self.x = config.buttons_size[self.key]['x']
        self.y = config.buttons_size[self.key]['y']
        self.w = config.buttons_size[self.key]['w']
        self.h = config.buttons_size[self.key]['h']

        self.x_center = self.x + (self.w / 2)
        self.y_center = self.y + (self.h / 2)

        self.button = pg.Rect(self.x, self.y, self.w, self.h)
        self.button_on = False
        self.function = function

        #  Додавання кнопки на цій поверхні
        self.screen = draw_on

        self.draw_params = {'button': self.button,
                            'text': self.key,
                            'x_center': self.x_center,
                            'y_center': self.y_center}


    def draw_button(self, color_active=False):

        color = color_effect.change_color()
        if color_active:
            color = color_effect.modify_color(color, l=-20)

        draw_params = self.draw_params.copy()
        if isinstance(draw_params['button'], list):#Повертає прапор, який вказує на те, чи є зазначений об'єкт екземпляром зазначеного класу
            pg.draw.polygon(self.screen, color, draw_params['button'])
        else:
            pg.draw.rect(self.screen, color, draw_params['button'], 5)

        draw_params.pop('button')
        surface, rect = config.text_objects(**draw_params, color=color)#для прийняття тільки іменованих аргументів
        self.screen.blit(surface, rect)#метод blit () застосовується до батьківської Surface, в той час як дочірня приймає в якості аргументу.


    def status(self):# Статус нажимання на кнопки

        pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()

        if self.button.collidepoint(pos):
            self.draw_button(color_active=True)
            if click[0] == 1:
                self.button_on = True
        else:
            self.draw_button()

        return self.button_on


    def __call__(self):
        # Запустити функцію кнопки, якщо кнопку увімкнено
        if self.button_on:
            self.button_on = False
            self.function()


class Spinner(Button_interface):

    def __init__(self, key, function, draw_on):

        Button.__init__(self, key, function, draw_on)

        # Цінності, які слід поставити на spinner
        self.text = f'{self.key} {self.current_val}'# рядки покращують читабельність коду, а також працюють швидше ніж інші способи форматування

        surface, rect = config.text_objects(self.text,
                                            left=self.x,
                                            top=self.y,
                                            font_size=config.medium_text)
        self.button_x, self.button_y = rect.bottomright
        self.button = pg.Rect(self.button_x, self.button_y, self.w, self.h)

        self.triangle = [[self.button_x, self.button_y],
                         [self.button_x + self.w, self.button_y],
                         [self.button_x + self.w / 2, self.button_y + self.h]]

        self.draw_params = {'button': self.triangle,
                            'text': self.text,
                            'left': self.x,
                            'top': self.y,
                            'font_size': config.medium_text}

    # / ----------------------------------------------------------------------- \

    def __call__(self):

        # Відображення значення spinner при включенні кнопки
        if self.button_on:
            pg.time.wait(250)#модуль pygame для управління часом і частотою кадрів

            color_text = colors['berry']
            color_text_act = color_effect.modify_color(colors['purple'], l=-50)

            rect_spinner = pg.Rect(self.button_x, self.button_y, self.w, self.h * len(self.vals))# Цінність класу полягає у властивостях і методах, що дозволяють управляти розміщенням поверхонь, виконувати перевірку їх перекриття
            cx = self.button_x + self.w / 2
            cy = self.button_y

            running = True
            while running:

                pg.event.pump()#дозволити pygame обробляти внутрішні дії
                pos = pg.mouse.get_pos()#отримати позицію курсора миші
                click = pg.mouse.get_pressed()#отримати стан кнопок миші

                color_rect = color_effect.change_color()
                pg.draw.rect(self.screen, color_rect, rect_spinner)#намалювати прямокутну форму

                for i in range(len(self.vals)):
                    surface, rect = config.text_objects(f'{self.vals[i]}',
                                                        x_center=cx,
                                                        y_center=cy + self.h / 2 + i * self.h,
                                                        color=color_text,
                                                        font_size=self.vals_font_size)
                    rect_button = rect.copy()
                    rect_button.left = self.button_x
                    rect_button.width = self.w
                    if rect_button.collidepoint(pos):#Метод collidepoint () об'єкта Rect перевіряє, чи знаходиться точка,
                    #координати якої були передані в якості аргументу, в межах прямокутника, до якого застосовується метод
                        if click[0] == 1:
                            self.function(self.vals[i])
                            self.current_val = f'{self.vals[i]}'
                            self.text = f'{self.key} {self.current_val}'
                            self.draw_params['text'] = self.text
                            running = False
                        surface, rect = config.text_objects(f'{self.vals[i]}',# Представлення значень на поверхності, її розміщення і колір
                                                            x_center=cx,
                                                            y_center=cy + self.h / 2 + i * self.h,
                                                            color=color_text_act,
                                                            font_size=self.vals_font_size * 2)
                        self.screen.blit(surface, rect)#метод blit () застосовується до батьківської Surface, в той час як дочірня приймає в якості аргументу.

                    else:
                        self.screen.blit(surface, rect)

                pg.display.update()#модуль pygame для оновлення

                if not rect_spinner.collidepoint(pos):#Метод collidepoint () об'єкта Rect перевіряє, чи знаходиться точка,
                    #координати якої були передані в якості аргументу, в межах прямокутника, до якого застосовується метод
                    running = False

            self.button_on = False
            pg.time.wait(250)#модуль pygame для управління часом і частотою кадрів



class Tetris:

    def __init__(self):

        self.screen = pg.display.set_mode((config.window_w, config.window_h))
        pg.display.set_caption('TETRIS') # Доступ до дисплея


        self.functions = {pg.K_LEFT: shape.move_left, # управління
                          pg.K_RIGHT: shape.move_right,
                          pg.K_DOWN: shape.move_down,
                          pg.K_r: shape.rotate,
                          pg.K_q: self.exit,
                          pg.K_m: self.menu,
                          pg.K_SPACE: self.pause,
                          'START': self.play,
                          'RANKING': self.ranking,
                          'BACK': self.menu,
                          'HOME': self.home,
                          'RESTART GAME': self.restart_game,
                          'EXIT': self.exit,
                          }

        self.running = False


    # Функції малювання
    def draw_score(self, color): #Вивід рахунку
        text = f'Score : {score.score}'
        # Представлення рахунку на поверхності, її розміщення і колір
        surface, rect = config.text_objects(text,
                                            x_center=config.texts['score']['x'],
                                            y_center=config.texts['score']['y'],
                                            color=color)
        self.screen.blit(surface, rect)#метод blit () застосовується до батьківської Surface, в той час як дочірня приймає в якості аргументу.



    def draw_next_shape(self, color):#Вивід наступної фігури на екран
        if config.see_next_shape:
            cx, cy = config.rects['next_shape'].center
            next_shape.draw_next_shape(cx, cy, self.screen)

            pg.draw.rect(self.screen, color, config.rects['next_shape'], 5)
            # Представлення фігури на поверхності, її розміщення і колір
            surface, rect = config.text_objects('Next Shape',
                                                x_center=config.texts['next_shape']['x'],
                                                y_center=config.texts['next_shape']['y'],
                                                color=color)
            self.screen.blit(surface, rect)#метод blit () застосовується до батьківської Surface, в той час як дочірня приймає в якості аргументу.


    def draw_background(self): #Малювання фону

        color = color_effect.change_color()

        # Фон
        self.screen.blit(config.images['GAME BACKGROUND'], (0, 0))#метод blit () застосовується до батьківської Surface, в той час як дочірня приймає в якості аргументу.

        # Межі гри
        pg.draw.rect(self.screen, color, config.rects['game_boundaries'], 5)

        # Інші об'єкти
        self.draw_next_shape(color)
        self.draw_score(color)


    def draw_records(self, names, records, color):

        text = 'TOP FIVE'
        x = config.texts['top five']['x']
        y = config.texts['top five']['y']
        # Представлення тексту на поверхності, її розміщення і колір
        surface, rect = config.text_objects(text, left=x, top=y, color=color)
        self.screen.blit(surface, rect)

        for i in range(len(records)):
            text = f'{names[i]} ......... {records[i]:2}'
            x = config.texts['records']['x']
            y = config.texts['records']['y'] + i * config.texts['records']['y_space']
            surface, rect = config.text_objects(text, left=x, top=y, color=color)# Представлення тексту на поверхності, її розміщення і колір
            self.screen.blit(surface, rect)#метод blit () застосовується до батьківської Surface, в той час як дочірня приймає в якості аргументу.


    def draw_game_over(self):

        text = 'GAME OVER'
        # Представлення тексту на поверхності, її розміщення і колір
        surface, rect = config.text_objects(text,
                                            x_center=config.texts['game_over']['x'],
                                            y_center=config.texts['game_over']['y'],
                                            rotation_angle=45,
                                            font_size=config.huge_text,
                                            color=colors['berry'])
        self.screen.blit(surface, rect)#метод blit () застосовується до батьківської Surface, в той час як дочірня приймає в якості аргументу.
        pg.display.update()#модуль pygame для оновлення
        pg.time.wait(1000)#модуль pygame для управління часом і частотою кадрів


    def start_count(self):

        texts = ['3', '2', '1', 'GO!']

        for text in texts:
            color = color_effect.change_color()
            surface, rect = config.text_objects(text,# Представлення рахунку на поверхності, її розміщення і колір
                                                x_center=config.texts['start']['x'],
                                                y_center=config.texts['start']['y'],
                                                font_size=config.huge_text,
                                                color=color)
            self.draw_background()
            self.screen.blit(surface, rect)#метод blit () застосовується до батьківської Surface, в той час як дочірня приймає в якості аргументу.
            pg.display.update()
            pg.time.wait(1000)#модуль pygame для управління часом і частотою кадрів

    # Функції
    def exit(self):
        pg.quit()
        quit()

    def pause(self):
        pause = True
        while pause:
            event = pg.event.wait()

            if event.type == pg.QUIT:
                self.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pause = False

    def _continue(self):
        shape.restart()
        score.restart(level=True)
        self.play()


    def restart_game(self):
        config.speed = 3
        shape.restart()
        score.restart()
        self.play()

    def home(self):
        config.speed = 3
        shape.restart()
        score.restart()
        self.menu()

    def is_losser(self):
        loss = False
        if any(rect.bottom <= config.game_boundaries[1] for rect in shape.dropped):
            loss = True
        return loss

    # Інтерактивні функції
    def menu(self):#функція для головного меню

        key_buttons = ['START', 'RANKING', 'EXIT']
        buttons = [Button_interface(key, self.functions[key], self.screen) for key in key_buttons]


        self.running = True
        while self.running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit()

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_F1:

                        buttons.append(button)
                        self.running = False

            self.screen.blit(config.images['MENU BACKGROUND'], (0, 0))#метод blit () застосовується до батьківської Surface, в той час як дочірня приймає в якості аргументу.

            for button in buttons:
                if isinstance(button, Button):#Повертає прапор, який вказує на те, чи є зазначений об'єкт екземпляром зазначеного класу
                    button.status()
                    if button.button_on:
                        self.running = False

            pg.display.update()#модуль pygame для оновлення
            config.clock.tick(config.fps)#частота картинок за хвилину

        pg.time.wait(250)#модуль pygame для управління часом і частотою кадрів

        for button in buttons:
            button()


    def ranking(self):#функція по перегляду топ 5 рейтингу

        names, records = score.load_records()

        key_button = 'BACK'
        button = Button_interface(key_button, self.functions[key_button], self.screen)

        self.running = True
        while self.running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit()

            self.screen.blit(config.images['RECORDS BACKGROUND'], (0, 0))#метод blit () застосовується до батьківської Surface, в той час як дочірня приймає в якості аргументу.

            button.status()
            if button.button_on:
                self.running = False

            color = color_effect.change_color()
            self.draw_records(names, records, color)

            pg.display.update()#модуль pygame для оновлення
            config.clock.tick(config.fps)#частота картинок за хвилину

        button()

    def restart_continue(self):#функція меню після закінчення гри

        key_buttons = ['HOME', 'RESTART GAME']
        buttons = [Button_interface(key, self.functions[key], self.screen) for key in key_buttons]

        self.running = True
        while self.running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit()

            self.screen.blit(config.images['MENU BACKGROUND'], (0, 0))#метод blit () застосовується до батьківської Surface, в той час як дочірня приймає в якості аргументу.

            for button in buttons:
                button.status()
                if button.button_on:
                    self.running = False

            pg.display.update()
            config.clock.tick(config.fps)

        for button in buttons:
            if button.button_on:
                return button

    def write_record(self):#функція для запису рахунку

        chars = string.ascii_uppercase
        name = list(f'{chars[-1]}    ')

        chars_index = 0
        name_index = 0
        count = 0

        self.running = True
        while self.running:

            for event in pg.event.get():

                if event.type == pg.QUIT:
                    self.exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        count += 1
                        if count < 4:
                            name_index += 1
                            chars_index = 0

                    if event.key == pg.K_BACKSPACE:
                        if name_index > 0:
                            chars_index = -1
                            name_index -= 2
                            count -= 1

                    else:
                        if event.key == pg.K_DOWN:
                            chars_index -= 1
                            if chars_index < ~(len(chars) - 1):
                                chars_index = -1

                        elif event.key == pg.K_UP:
                            chars_index += 1
                            if chars_index > len(chars) - 1:
                                chars_index = 0

                if event.type == pg.KEYUP:
                    if event.key == pg.K_DOWN or event.key == pg.K_UP:
                        chars_index += 0

            name[name_index] = chars[chars_index]

            text = ''.join(name)
            color = color_effect.change_color()
            # розміщення тексту на поверхні
            surface, rect = config.text_objects(text,
                                                x_center=config.texts['write_record']['x'],
                                                y_center=config.texts['write_record']['y'],
                                                color=color)
            # Малювання фону
            pg.draw.rect(self.screen, colors['gray'], rect)
            self.screen.blit(surface, rect)#метод blit () застосовується до батьківської Surface, в той час як дочірня приймає в якості аргументу.

            pg.display.update()#модуль pygame для оновлення
            config.clock.tick(config.fps)#частота картинок за хвилину

            if count == 4:
                self.running = False

        name = ''.join(name)
        name = name.replace(' ', '')
        score.save_record(name)

        pg.time.wait(1000)#модуль pygame для управління часом і частотою кадрів

    def play(self):#функція гри

        shape.next_shape()
        next_shape.next_shape()

        # Позначення, чи користувач тримає ліву чи праву клавіші
        left_on = False
        right_on = False

        self.start_count()

        self.running = True
        while self.running:

            for event in pg.event.get():

                if event.type == pg.QUIT:
                    self.exit()

                elif event.type == pg.KEYDOWN:
                    if event.key in self.functions:
                        if event.key == pg.K_DOWN:
                            self.functions[event.key](pressed_y=True)
                        else:
                            self.functions[event.key]()

                        if event.key == pg.K_LEFT:
                            left_on = True

                        elif event.key == pg.K_RIGHT:
                            right_on = True

                elif event.type == pg.KEYUP:
                    if event.key == pg.K_DOWN:
                        self.functions[event.key](pressed_y=False)

                    if event.key == pg.K_LEFT:
                        left_on = False

                    if event.key == pg.K_RIGHT:
                        right_on = False

            self.draw_background()
            shape.move_down()

            if not shape.move:

                # Якщо форма не може рухатися вниз, але користувач є
                # утримування лівої або правої клавіші
                if left_on:
                    shape.move_left()
                    left_on = False

                if right_on:
                    shape.move_right()
                    right_on = False

                # Якщо переміщена форма може перейти вниз
                if shape.move_down():
                    shape.move = True

                else:
                    # Додавання форми до скинутих фігур
                    shape.update_filled_spaces()

            shape.draw_filled(self.screen)
            shape.draw_shape(self.screen)

            pg.display.update()
            config.clock.tick(config.fps)

            n_eresed = shape.erese_blocks()
            if n_eresed > 0:
                score.update_score(n_eresed)
                shape.draw_eresed(self.screen)

            if not shape.move:
                shape.next_shape(shape=next_shape)
                next_shape.next_shape()

            if self.is_losser():
                self.draw_game_over()
                self.write_record()
                button = self.restart_continue()


        pg.time.wait(250)#модуль pygame для управління часом і частотою кадрів
        button()


if __name__ == '__main__':
    tetris = Tetris()
    tetris.menu()