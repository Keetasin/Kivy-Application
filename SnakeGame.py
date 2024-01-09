from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
import random
from kivy.properties import NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

class SnakeGame(Widget):
    score = NumericProperty(0)
 
    def __init__(self, **kwargs):
        self.snake_speed = kwargs.pop("snake_speed")
        self.speed_start = self.snake_speed 
        
        super(SnakeGame, self).__init__(**kwargs)

        self.snake_size = 20
        self.snake_pos = [(100, 100), (100, 80), (100, 60)]
        self.food_pos = (Window.width // 2, Window.height // 2)

        self.direction = 'up'
        self.sound1 = SoundLoader.load('gameover.mp3')
        Clock.schedule_interval(self.update, 1.0 / self.snake_speed)
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

        self.popup = Popup (
            title="Game Over",
            size_hint=(None, None),
            size=(400, 400)
        )

        self.spawn_food() 

    def on_key_up(self, instance,x,y):
        print('up')

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if text == 'w':
            if self.direction == 'down':
                self.direction = 'down'
            else:
                self.direction = 'up'
        elif text == 's':
            if self.direction == 'up':
                self.direction = 'up'
            else:
                self.direction = 'down'
        elif text == 'a':
            if self.direction == 'right':
                self.direction = 'right'
            else:
                self.direction = 'left'
        elif text == 'd':
            if self.direction == 'left':
                self.direction = 'left'
            else:
                self.direction = 'right'


    def update(self, dt):
        # Update snake position
        x, y = self.snake_pos[0]
        if self.direction == 'up':
            y += self.snake_size
        elif self.direction == 'down':
            y -= self.snake_size
        elif self.direction == 'left':
            x -= self.snake_size
        elif self.direction == 'right':
            x += self.snake_size

        x %= 480
        y %= 480

        self.snake_pos.insert(0, (x, y))

        if self.check_collision_with_food(x, y):
            self.score += 1
            self.snake_grow()
            self.spawn_food()  

            if self.score > 5 and self.score <=20:
                self.snake_speed += (0.02*self.score)
            elif self.score > 20 and self.score < 26:
                self.snake_speed += (0.06*self.score)
            else :
                self.snake_speed =self.snake_speed

            Clock.unschedule(self.update)
            Clock.schedule_interval(self.update, 1.0 / self.snake_speed)

        else:
            self.snake_pos.pop()
        
        if self.check_collision(x, y, self.snake_pos[1:]):
            self.popup.content = Label(text=f"Score: {self.score}")
            self.popup.open()
            self.sound1.play()
            self.reset_game()

        self.canvas.clear()
        self.draw_snake()
        self.draw_food()


    def draw_snake(self):
        with self.canvas:
            Color(0, 1, 0)
            for pos in self.snake_pos:
                Rectangle(pos=(pos[0], pos[1]), size=(self.snake_size, self.snake_size))


    def draw_food(self):
        with self.canvas:
            Color(1, 0, 0)
            Rectangle(pos=(self.food_pos[0], self.food_pos[1]), size=(self.snake_size, self.snake_size))


    def spawn_food(self):
        x = random.randint(0, 19) * self.snake_size
        y = random.randint(0, 19) * self.snake_size

        while (x, y) in self.snake_pos:
            x = random.randint(0, 19) * self.snake_size
            y = random.randint(0, 19) * self.snake_size
        
        self.food_pos = (x, y)

    def check_collision(self, x, y, positions):
        for pos in positions:
            if pos == (x, y):
                return True

        return False

    def check_collision_with_food(self, x, y):
        return (x, y) == self.food_pos
    
    def snake_grow(self):
        x, y = self.snake_pos[-1]
        if self.direction == 'up':
            y -= self.snake_size
        elif self.direction == 'down':
            y += self.snake_size
        elif self.direction == 'left':
            x += self.snake_size
        elif self.direction == 'right':
            x -= self.snake_size

        self.snake_pos.append((x, y))


    def reset_game(self):
        self.snake_pos = [(100, 100), (100, 80), (100, 60)]
        self.direction = 'up'

        self.snake_speed = self.speed_start
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.update, 1.0 / self.snake_speed)

        self.score = 0

class Menu(BoxLayout):
    def __init__(self, *args, **kwargs):
        self.manager = kwargs.pop("manager")
        super().__init__(*args, **kwargs)
    


class My_SnakeApp(App):
    def build(self):
        menu_screen = Screen(name="Menu Game")
        name_screen = Screen(name="SnakeGame")
        Baby_screen = Screen(name="Baby Snake")
        Child_screen = Screen(name="Child Snake")
        Teenager_screen = Screen(name="Teenager Snake")
        Adult_screen = Screen(name="Adult Snake")
        super_screen = Screen(name="Super Snake")

        sm = ScreenManager()

        menu_screen.add_widget(Menu(manager=sm))
        Baby_screen.add_widget(SnakeGame(snake_speed=5))
        Child_screen.add_widget(SnakeGame(snake_speed=10))
        Teenager_screen.add_widget(SnakeGame(snake_speed=18))
        Adult_screen.add_widget(SnakeGame(snake_speed=25))
        super_screen.add_widget(SnakeGame(snake_speed=100))

        sm.add_widget(menu_screen)
        sm.add_widget(name_screen)
        sm.add_widget(Baby_screen)
        sm.add_widget(Child_screen)
        sm.add_widget(Teenager_screen)
        sm.add_widget(Adult_screen)
        sm.add_widget(super_screen)

        sm.current = "Menu Game"

        self.sound_open = SoundLoader.load('open.mp3')
        self.sound_open.play()

        Window.size = (400, 380)
        Window.resizable = False

        return sm

if __name__ == '__main__':
    My_SnakeApp().run()
