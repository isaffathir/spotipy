from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.slider.slider import MDSlider
from kivymd.app import MDApp
from kvdroid.tools import change_statusbar_color, navbar_color
from kvdroid.tools.audio import Player
from kvdroid.tools.network import network_status, wifi_status, mobile_status
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivymd.uix.label import MDLabel
import datetime
import time

class Tema(MDApp):
    pass

class SpotipyButton(MDFloatingActionButton):
    pass

class SpotipySlider(MDSlider):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        else:
            return False

class Home(MDScreen):
    music_pos = NumericProperty(0)
    maxduration = NumericProperty(0)

    def __init__(self, **kw):
        Builder.load_file("kv/home.kv")
        a = Tema()
        a.theme_cls.material_style = "M3"
        change_statusbar_color('#4C6E81', 'white')
        navbar_color('#4C6E81')
        super().__init__(**kw)

        # Temp Data
        self.like = 0
        self.shuffle = 0
        self.repeat = 0
        self.seek = 0
        self.player = Player()
        self.add_music()
        time.sleep(0.5)
        self.player.pause()
        self.maxduration_music()
        self.slider = self.ids.spoti_slider
        self.slider.bind(on_touch_down = self.get_slider_value,on_touch_up = self.seek_music)
        Clock.schedule_interval(self.check_connection, 0)

    def check_connection(self,*args):
        player = self.player
        max = player.get_duration() / 1000
        if network_status() == True:
            self.ids.no_inet.text = ""
            if self.ids.spoti_slider.max == 0:
                self.add_music()
                self.ids.spoti_slider.max = max

            elif self.ids.spoti_slider.max != max:
                self.add_music()
                self.ids.spoti_slider.max = max
            else:
                "added"
        else:
            print("no connection")
            self.ids.no_inet.text = "No Internet"

    def detikmenit(self, sec):
        val = str(datetime.timedelta(seconds = sec)).split(':')
        return f'{val[1]}:{val[2].split(".")[0]}'

    def add_music(self):
        player = self.player
        player.mPlayer
        player.stream("https://raw.githubusercontent.com/isaffathir/PyMusic/master/Light%20Switch.mp3")
        time.sleep(0.5)
        player.pause()

    def play_music(self):
        player = self.player
        play_button = self.ids.play_button
        Clock.schedule_interval(self.current_pos_music, 0)

        if self.ids.left_time.text == self.ids.right_time.text:
            player.seek(0)
            player.resume()
            play_button.icon = "pause"
            if self.repeat == 2:
                player.do_loop(True)

        elif play_button.icon == "play":
            player.resume()
            play_button.icon = "pause"
            
        elif play_button.icon == "pause":
            player.pause()
            play_button.icon = "play"


    def like_music(self):
        player = self.player
        like_button = self.ids.like_button
        print(self.music_pos)
        print(self.maxduration)
        print(network_status())
        print(wifi_status())
        if self.like == 0:
            like_button.icon_color = "#a60d3e"
            self.like += 1
            print(self.like)
        elif self.like != 0:
            like_button.icon_color = "#ded7db"
            self.like -= 1
            print(self.like)

    def shuffle_music(self):
        shuffle_button = self.ids.shuffle_button
        print(self.ids.shuffle_button.icon_color)
        if self.shuffle == 0:
            shuffle_button.icon_color = "#00ff00"
            self.shuffle += 1
            print(self.like)
        elif self.shuffle != 0:
            shuffle_button.icon_color = "#e0e0da"
            self.shuffle -= 1
            print(self.like)

    def repeat_music(self):
        repeat_button = self.ids.repeat_button
        if self.repeat == 0:
            repeat_button.icon = "repeat"
            repeat_button.icon_color = "#00ff00"
            self.repeat += 1
        elif self.repeat == 1:
            repeat_button.icon = "repeat-once"
            repeat_button.icon_color = "#00ff00"
            self.repeat += 1
        elif self.repeat == 2:
            repeat_button.icon = "repeat-off"
            repeat_button.icon_color = "#e0e0da"
            self.repeat -= 2

    def get_slider_value(self,slider,touch):
        if slider.collide_point(*touch.pos):
            Clock.unschedule(self.current_pos_music)
            self.seek += 1

    def seek_music(self,slider,touch):
        player = self.player
        if self.seek == 1:
            Clock.schedule_interval(self.current_pos_music, 0)
            player.seek(slider.value)
            self.seek -= 1

    def current_pos_music(self,*args):
        player = self.player
        stats_repeat = self.repeat
        self.music_pos = player.current_position() / 1000
        if player.is_playing() == False:
            self.ids.spoti_slider.max = player.get_duration() / 1000
            if self.ids.left_time.text > self.ids.right_time.text:
                self.ids.left_time.text = self.ids.right_time.text
            player.pause()
            self.ids.play_button.icon = "play"
        elif player.is_playing() == True:
            self.ids.spoti_slider.max = player.get_duration() / 1000
            if self.ids.left_time.text > self.ids.right_time.text:
                self.ids.left_time.text = self.ids.right_time.text
            if stats_repeat == 2:
                player.do_loop(True)
            else:
                print("bukan")
                player.do_loop(False)

    def maxduration_music(self):
        player = self.player
        self.maxduration = player.get_duration() / 1000