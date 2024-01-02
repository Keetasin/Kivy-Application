from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color





class SnakeGame(Widget):
    def __init__(self, *args, **kwargs):

        super(SnakeGame, self).__init__(**kwargs)
        self.snake_size = 20
        self.snake_pos = [(100, 100), (100, 80), (100, 60)]
        self.food_pos = (Window.width // 2, Window.height // 2)

        self.direction = 'up'
        self.snake_speed = 12

        Window.bind(on_key_down=self.on_key_down)
        Clock.schedule_interval(self.update, 1.0 / self.snake_speed)



    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if text == 'w':
            self.direction = 'up'
        elif text == 's':
            self.direction = 'down'
        elif text == 'a':
            self.direction = 'left'
        elif text == 'd':
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
        self.draw_snake()

    def draw_snake(self):
        with self.canvas:
            Color(0, 1, 0)
            for pos in self.snake_pos:
                Rectangle(pos=(pos[0], pos[1]), size=(self.snake_size, self.snake_size))



   

class SnakeApp(App):
    def build(self):
        box = GridLayout()
        game = SnakeGame()

        box.add_widget(game)

        Window.size = (400, 380)
        Window.resizable = False

        return box

if __name__ == '__main__':
    SnakeApp().run()
