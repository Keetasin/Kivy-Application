from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window


class SnakeGame(Widget):
    def __init__(self, *args, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
    pass


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
