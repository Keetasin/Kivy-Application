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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image



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
            Color(0, 1 - (max(0.25,self.score/30)), 0)
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


class Container(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Container, self).__init__(*args, **kwargs)

        # Create GridLayout with a 5x5 grid
        grid_layout = GridLayout(cols=5, spacing=5)

        image_paths = [
            'King_cobra.jpg', 'Banded_Krait.jpg', 'Daboia_siamensis.jpg', 'Indochinese_spitting_cobra.jpg', 'Micrurus_fulvius.jpg',
            'Calloselasma_rhodostoma.jpg', 'purpureomaculatus.jpg', 'Malayopython_reticulatus.jpg', 'Python_bivittatus.jpg', 'Boiga_cyanea.jpg',
            'Xenopeltis_unicolor.jpg', 'Lycodon_aulicus.jpg', 'Pantherophis_alleghaniensis.jpg', 'Rhabdophis_subminiatus.jpg', 'Trimeresurus_purpureomaculatus.jpg',
            'Trimeresurus_macrops.jpg', 'Trimeresurus_albolabris.jpg', 'Oligodon_fasciolatus.jpg', 'Ptyas_korros.jpg', 'Fowlea_Piscator.jpg',
            'Flying_snakes.jpg', 'Coelognathus_radiatus.jpg', 'Malayan_Pit_viper.jpg', 'Boiga_siamensis.jpg', 'Russell’s_Viper.jpg'
        ]

        # Add buttons to the GridLayout with CustomButton
        for path in image_paths:
            image = Image(source=path, size=(50, 50))  # Adjust size as needed
            image.bind(on_touch_down=self.on_image_click)
            grid_layout.add_widget(image)

        # Add the GridLayout to the Container
        self.add_widget(grid_layout)
        self.data_popup = Popup(
            title="Data Snake",
            size_hint=(None, None),
            size=(400, 400),)

    def on_image_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if instance.source == 'King_cobra.jpg':
                self.data_popup.content=Label(text="King cobra")
            if instance.source == 'Banded_Krait.jpg':
                self.data_popup.content=Label(text="Banded Krait")
            if instance.source == 'Daboia_siamensis.jpg':
                self.data_popup.content=Label(text="Daboia siamensis")
            if instance.source == 'Indochinese_spitting_cobra.jpg':
                self.data_popup.content=Label(text="Indochinese spitting cobra")
            if instance.source == 'Micrurus_fulvius.jpg':
                self.data_popup.content=Label(text="Micrurus fulvius")
            if instance.source == 'Calloselasma_rhodostoma.jpg':
                self.data_popup.content=Label(text="Calloselasma rhodostoma")
            if instance.source == 'purpureomaculatus.jpg':
                self.data_popup.content=Label(text="purpureomaculatus")
            if instance.source == 'Malayopython_reticulatus.jpg':
                self.data_popup.content=Label(text="Malayopython reticulatus")
            if instance.source == 'Python_bivittatus.jpg':
                self.data_popup.content=Label(text="Python bivittatus")
            if instance.source == 'Boiga_cyanea.jpg':
                self.data_popup.content=Label(text="Boiga cyanea")
            if instance.source == 'Xenopeltis_unicolor.jpg':
                self.data_popup.content=Label(text="Xenopeltis unicolor")
            if instance.source == 'Lycodon_aulicus.jpg':
                self.data_popup.content=Label(text="Lycodon aulicus")
            if instance.source == 'Pantherophis_alleghaniensis.jpg':
                self.data_popup.content=Label(text="Pantherophis alleghaniensis")
            if instance.source == 'Rhabdophis_subminiatus.jpg':
                self.data_popup.content=Label(text="Rhabdophis subminiatus")
            if instance.source == 'Trimeresurus_purpureomaculatus.jpg':
                self.data_popup.content=Label(text="Trimeresurus purpureomaculatus")
            if instance.source == 'Trimeresurus_macrops.jpg':
                self.data_popup.content=Label(text="Trimeresurus macrops")
            if instance.source == 'Trimeresurus_albolabris.jpg':
                self.data_popup.content=Label(text="Trimeresurus albolabris")
            if instance.source == 'Oligodon_fasciolatus.jpg':
                self.data_popup.content=Label(text="Oligodon_fasciolatus")
            if instance.source == 'Ptyas_korros.jpg':
                self.data_popup.content=Label(text="Ptyas korros")
            if instance.source == 'Fowlea_Piscator.jpg':
                self.data_popup.content=Label(text="Fowlea Piscator")
            if instance.source == 'Flying_snakes.jpg':
                self.data_popup.content=Label(text="Flying snakes")
            if instance.source == 'Coelognathus_radiatus.jpg':
                self.data_popup.content=Label(text="Coelognathus radiatus")
            if instance.source == 'Malayan_Pit_viper.jpg':
                self.data_popup.content=Label(text="Malayan Pit viper")
            if instance.source == 'Boiga_siamensis.jpg':
                self.data_popup.content=Label(text="Boiga siamensis")
            if instance.source == 'Russell’s_Viper.jpg':
                self.data_popup.content=Label(text="Russell’s Viper")

        self.data_popup.open()

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
        data_screen = Screen(name="Data Snake")

        sm = ScreenManager()

        menu_screen.add_widget(Menu(manager=sm))
        super_screen.add_widget(SnakeGame(snake_speed=100))
        Adult_screen.add_widget(SnakeGame(snake_speed=25))
        Teenager_screen.add_widget(SnakeGame(snake_speed=18))
        Child_screen.add_widget(SnakeGame(snake_speed=10))
        Baby_screen.add_widget(SnakeGame(snake_speed=5))
        data_screen.add_widget(Container())
        

        sm.add_widget(menu_screen)
        sm.add_widget(name_screen)
        sm.add_widget(super_screen)
        sm.add_widget(Adult_screen)
        sm.add_widget(Teenager_screen)
        sm.add_widget(Child_screen)
        sm.add_widget(Baby_screen)
        sm.add_widget(data_screen)

        sm.current = "Menu Game"

        self.sound_open = SoundLoader.load('open.mp3')
        self.sound_open.play()

        Window.size = (400, 380)
        Window.resizable = False

        return sm

if __name__ == '__main__':
    My_SnakeApp().run()
