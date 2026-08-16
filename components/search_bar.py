import theme
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.app import App
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line



from components.icons import (
    get_icon,
    SEARCH
)



class SearchBar(BoxLayout):


    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        self.orientation = "horizontal"

        self.spacing = dp(8)

        self.padding = [
            dp(10),
            dp(8)
        ]


        self.size_hint_y = None

        self.height = dp(60)



        # =========================
        # BACKGROUND
        # =========================


        with self.canvas.before:


            Color(*theme.CARD)


            self.bg = RoundedRectangle(

                pos=self.pos,

                size=self.size,

                radius=[22]

            )


        with self.canvas.after:


            Color(*theme.ITEM_BORDER)


            self.border = Line(

                rounded_rectangle=(

                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    22

                ),

                width=1

            )


        self.bind(

            pos=self.update_bg,

            size=self.update_bg

        )



        # =========================
        # SEARCH ICON
        # =========================


        search_box = BoxLayout(

            size_hint_x=None,

            width=dp(40),

            padding=dp(5)

        )


        search_icon = Image(

            source=get_icon(SEARCH),

            size_hint=(None,None),

            size=(dp(28),dp(28)),

            allow_stretch=True,

            keep_ratio=True

        )


        search_box.add_widget(

            search_icon

        )


        self.add_widget(

            search_box

        )



        # =========================
        # INPUT
        # =========================


        self.input = TextInput(

            hint_text=App.get_running_app().tr("search_hint"),

            multiline=False,

            background_normal="",

            background_active="",

            background_color=(0,0,0,0),

            foreground_color=theme.TEXT,

            hint_text_color=theme.TEXT_SECONDARY,

            cursor_color=theme.PRIMARY,

            font_size=38,

            padding=[

                dp(10),
                dp(12)

            ]

        )


        self.add_widget(

            self.input

        )


    # =========================
    # UPDATE
    # =========================


    def update_bg(self,*args):


        self.bg.pos = self.pos

        self.bg.size = self.size


        self.border.rounded_rectangle = (

            self.x,
            self.y,
            self.width,
            self.height,
            22

        )