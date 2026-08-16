from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.app import App
from kivy.clock import Clock
from database import Database
import theme
from components.item_card import ItemCard
from components.header import Header

from components.icons import (
    get_icon,
    ADD,
    EMPTY
)





class HomeScreen(Screen):


    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        
        app = App.get_running_app()

        self.db = Database()



        # =========================
        # BACKGROUND
        # =========================


        with self.canvas.before:


            Color(*theme.BACKGROUND)


            self.bg = RoundedRectangle(

                pos=self.pos,

                size=self.size

            )


        self.bind(

            pos=self.update_bg,

            size=self.update_bg

        )



        # =========================
        # ROOT
        # =========================


        root = BoxLayout(

            orientation="vertical",

            spacing=dp(18),

            padding=dp(18)

        )



        # =========================
        # HEADER
        # =========================


        self.header = Header()

        root.add_widget(

            self.header

        )



        # =========================
        # LIST
        # =========================


        self.scroll = ScrollView(

            do_scroll_x=False

        )


        self.list_container = BoxLayout(

            orientation="vertical",

            spacing=dp(15),

            size_hint_y=None

        )


        self.list_container.bind(

            minimum_height=
            self.list_container.setter(
                "height"
            )

        )


        self.scroll.add_widget(

            self.list_container

        )


        root.add_widget(

            self.scroll

        )



        # =========================
        # ADD BUTTON
        # =========================


        self.add_button = Button(

            size_hint_y=None,

            height=dp(50),

            background_normal="",

            background_down="",

            background_color=theme.PRIMARY,

        )


        button_box = BoxLayout(

            orientation="horizontal",

            spacing=dp(90),

            padding=[dp(80), dp(-50), dp(55), dp(0)]

        )


        icon = Image(

            source=get_icon(ADD),

            size_hint_x=None,

            width=dp(38)

        )


        text = Label(

            text=app.tr("add_item"),

            color=theme.TEXT,

            font_size=50,

            bold=True

        )


        button_box.add_widget(icon)

        button_box.add_widget(text)


        self.add_button.add_widget(

            button_box

        )


        self.add_button.bind(

            on_press=self.open_add_item

        )


        root.add_widget(

            self.add_button

        )


        # BORDER BUTTON


        with self.add_button.canvas.after:


            Color(*theme.ITEM_BORDER)


            self.button_border = Line(

                rounded_rectangle=(

                    self.add_button.x,
                    self.add_button.y,
                    self.add_button.width,
                    self.add_button.height,
                    22

                ),

                width=1

            )


        self.add_button.bind(

            pos=self.update_button_border,

            size=self.update_button_border

        )



        self.add_widget(root)


        self.load_items()




    # =========================
    # LOAD
    # =========================


    def load_items(self):


        rows = self.db.get_all_items()

        self.show_items(rows)




    # =========================
    # SHOW
    # =========================


    def show_items(self, rows):
        
        app = App.get_running_app()

        self.list_container.clear_widgets()



        if not rows:


            empty_box = BoxLayout(

                orientation="vertical",

                size_hint_y=None,

                height=dp(180),

                spacing=dp(10)

            )


            empty_icon = Image(

                source=get_icon(EMPTY),

                size_hint_y=None,

                height=dp(70)

            )


            app = App.get_running_app()

            empty_text = Label(

                text=app.tr("no_items"),

                color=theme.TEXT_SECONDARY,

                font_size=24,

                bold=True

            )


            empty_box.add_widget(

                empty_icon

            )


            empty_box.add_widget(

                empty_text

            )


            self.list_container.add_widget(

                empty_box

            )


            return




        for item in rows:


            (
                item_id,
                name,
                category,
                icon,
                location,
                description,
                image_path

            ) = item



            card = ItemCard(

                item_id=item_id,

                name=name,

                category=category or app.tr("other"),

                icon=icon,

                location=location or app.tr("unknown"),

                description=description or "",

                image_path=image_path or ""

            )


            self.list_container.add_widget(

                card

            )



    def refresh_theme(self):

        self.clear_widgets()

        self.__init__(name=self.name)
    # =========================
    # ADD ITEM
    # =========================


    def open_add_item(self, instance):

        self.manager.current = "add_item"




    # =========================
    # REFRESH
    # =========================


    def refresh(self):

        self.load_items()




    # =========================
    # UPDATE
    # =========================


    def update_bg(self,*args):

        self.bg.pos = self.pos

        self.bg.size = self.size



    def update_button_border(self,*args):

        self.button_border.rounded_rectangle = (

            self.add_button.x,
            self.add_button.y,
            self.add_button.width,
            self.add_button.height,
            22

        )
        
    def on_pre_enter(self):

        self.load_items()
