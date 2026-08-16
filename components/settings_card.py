from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line


from theme import (
    CARD,
    PRIMARY,
    TEXT,
    TEXT_SECONDARY,
    ITEM_BORDER
)



class SettingsCard(ButtonBehavior, BoxLayout):


    def __init__(
        self,
        icon,
        title,
        subtitle,
        callback,
        **kwargs
    ):

        super().__init__(**kwargs)


        self.callback = callback


        self.orientation = "horizontal"

        self.spacing = dp(15)

        self.padding = dp(15)

        self.size_hint_y = None

        self.height = dp(80)



        # =========================
        # CARD BACKGROUND
        # =========================


        with self.canvas.before:


            Color(*CARD)


            self.bg = RoundedRectangle(

                pos=self.pos,

                size=self.size,

                radius=[22]

            )


        with self.canvas.after:


            Color(*ITEM_BORDER)


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
        # ICON
        # =========================


        icon_img = Image(

            source=icon,

            size_hint_x=None,

            width=dp(45),

            size_hint_y=None,

            height=dp(45),

            allow_stretch=True,

            keep_ratio=True

        )


        self.add_widget(

            icon_img

        )



        # =========================
        # TEXT
        # =========================


        text_box = BoxLayout(

            orientation="vertical",

            spacing=dp(2)

        )


        title_label = Label(

            text=title,

            color=PRIMARY,

            font_size=40,

            bold=True,

            halign="left",

            valign="middle"

        )


        title_label.bind(

            size=title_label.setter(
                "text_size"
            )

        )



        subtitle_label = Label(

            text=subtitle,

            color=TEXT_SECONDARY,

            font_size=34,

            halign="left",

            valign="middle"

        )


        subtitle_label.bind(

            size=subtitle_label.setter(
                "text_size"
            )

        )



        text_box.add_widget(

            title_label

        )


        text_box.add_widget(

            subtitle_label

        )


        self.add_widget(

            text_box

        )



    # =========================
    # CLICK
    # =========================


    def on_press(self):

        if self.callback:

            self.callback(self)



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