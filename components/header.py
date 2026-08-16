import theme
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line

from kivy.app import App


from components.icons import (
    get_icon,
    SEARCH,
    SETTINGS
)



class Header(BoxLayout):


    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        self.orientation = "horizontal"

        self.spacing = dp(10)

        self.padding = [
            dp(15),
            dp(8),
            dp(15),
            dp(8)
        ]

        self.size_hint_y = None

        self.height = dp(75)



        # =========================
        # BACKGROUND
        # =========================

        with self.canvas.before:

            Color(*theme.CARD)

            self.bg = RoundedRectangle(

                pos=self.pos,

                size=self.size,

                radius=[25]

            )


        with self.canvas.after:

            Color(*theme.ITEM_BORDER)

            self.border = Line(

                rounded_rectangle=(

                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    25

                ),

                width=1.2

            )


        self.bind(

            pos=self.update_bg,

            size=self.update_bg

        )



        # =========================
        # TITLE
        # =========================

        self.title = Label(

            text="Where Is:",

            color=theme.PRIMARY,

            font_size=64,

            bold=True,

            halign="left",

            valign="middle"

        )


        self.title.bind(

            size=self.title.setter(
                "text_size"
            )

        )


        self.add_widget(
            self.title
        )



        # =========================
        # SPACE
        # =========================

        self.add_widget(
            Label()
        )



        # =========================
        # SEARCH BUTTON
        # =========================

        self.search_btn = self.create_icon_button(
            SEARCH
        )


        self.search_btn.bind(
            on_press=self.open_search
        )


        self.add_widget(
            self.search_btn
        )



        # =========================
        # SETTINGS BUTTON
        # =========================

        self.settings_btn = self.create_icon_button(
            SETTINGS
        )


        self.settings_btn.bind(
            on_press=self.open_settings
        )


        self.add_widget(
            self.settings_btn
        )



    # =========================
    # ICON BUTTON
    # =========================

    def create_icon_button(self, icon):


        button = Button(

            size_hint_x=None,

            size_hint_y=None,

            width=dp(35),

            height=dp(35),
 
            background_normal=get_icon(icon),

            background_down=get_icon(icon),

            background_color=(1,1,1,1),

            border=(0,0,0,0)

        )


        return button



    # =========================
    # UPDATE BACKGROUND
    # =========================

    def update_bg(self, *args):


        self.bg.pos = self.pos

        self.bg.size = self.size


        self.border.rounded_rectangle = (

            self.x,
            self.y,
            self.width,
            self.height,
            25

        )



    # =========================
    # NAVIGATION
    # =========================

    def open_settings(self, instance):


        app = App.get_running_app()


        if app and app.root:

            app.root.current = "settings"



    def open_search(self, instance):


        app = App.get_running_app()


        if app and app.root:

            app.root.current = "search"
