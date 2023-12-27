from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout


class SnakeGame(Widget):
    pass


class SnakeApp(App):
    def build(self):
        box = GridLayout()
        game = SnakeGame()

        box.add_widget(game)

        return box

if __name__ == '__main__':
    SnakeApp().run()
