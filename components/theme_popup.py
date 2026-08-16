from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivy.metrics import dp


class ThemePopup:


    def __init__(self, callback):

        self.callback = callback



    def open(self):


        box = BoxLayout(

            orientation="vertical",

            spacing=dp(10),

            padding=dp(15)

        )


        themes = [

            "Ocean",

            "Dark",

            "Coffee",

            "Light"

        ]


        for theme in themes:


            btn = Button(

                text=theme,

                size_hint_y=None,

                height=dp(50)

            )


            btn.bind(

                on_press=lambda x, t=theme:
                self.select(t)

            )


            box.add_widget(btn)



        self.popup = Popup(

            title="Choose Theme",

            content=box,

            size_hint=(0.8,0.5)

        )


        self.popup.open()



    def select(self, theme):

        self.callback(theme)

        self.popup.dismiss()