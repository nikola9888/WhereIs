from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

from database import Database

from theme import (
    BACKGROUND,
    CARD,
    PRIMARY,
    TEXT,
    TEXT_SECONDARY,
    DANGER
)



class CategoriesScreen(Screen):


    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        self.db = Database()


        with self.canvas.before:

            Color(*BACKGROUND)

            self.bg = RoundedRectangle(

                pos=self.pos,

                size=self.size

            )


        self.bind(

            pos=self.update_bg,

            size=self.update_bg

        )



        self.root_box = BoxLayout(

            orientation="vertical",

            spacing=dp(12),

            padding=dp(20)

        )


        self.add_widget(
            self.root_box
        )



        self.title = Label(

            text="Categories",

            color=PRIMARY,

            font_size=34,

            bold=True,

            size_hint_y=None,

            height=dp(60)

        )


        self.root_box.add_widget(
            self.title
        )



        self.name_input = TextInput(

            hint_text="New category name",

            size_hint_y=None,

            height=dp(50),

            background_normal="",

            background_color=CARD,

            foreground_color=TEXT,

            hint_text_color=TEXT_SECONDARY

        )


        self.root_box.add_widget(
            self.name_input
        )



        add = Button(

            text="＋ Add Category",

            size_hint_y=None,

            height=dp(55),

            background_normal="",

            background_color=PRIMARY,

            color=TEXT

        )


        add.bind(
            on_press=self.add_category
        )


        self.root_box.add_widget(
            add
        )



        self.list_box = BoxLayout(

            orientation="vertical",

            spacing=dp(10)

        )


        self.root_box.add_widget(
            self.list_box
        )



        back = Button(

            text="← Back",

            size_hint_y=None,

            height=dp(55),

            background_normal="",

            background_color=CARD,

            color=TEXT

        )


        back.bind(

            on_press=self.go_back

        )


        self.root_box.add_widget(
            back
        )



    def on_enter(self):

        self.load_categories()



    def load_categories(self):

        self.list_box.clear_widgets()


        for cat in self.db.get_categories():

            cid = cat[0]

            name = cat[1]

            icon = cat[2]


            row = BoxLayout(

                spacing=dp(10),

                size_hint_y=None,

                height=dp(55)

            )


            label = Label(

                text=f"{icon}  {name}",

                color=TEXT,

                font_size=18

            )


            delete = Button(

                text="🗑",

                size_hint_x=None,

                width=dp(55),

                background_normal="",

                background_color=DANGER,

                color=TEXT

            )


            delete.bind(

                on_press=lambda x, i=cid:
                self.delete_category(i)

            )


            row.add_widget(label)

            row.add_widget(delete)


            self.list_box.add_widget(row)



    def add_category(self, instance):

        name = self.name_input.text.strip()


        if not name:

            return


        try:

            self.db.add_category(

                name,

                "📦"

            )

        except:

            pass


        self.name_input.text = ""


        self.load_categories()



    def delete_category(self, category_id):

        self.db.delete_category(

            category_id

        )


        self.load_categories()



    def go_back(self, instance):

        self.manager.current = "settings"



    def update_bg(self, *args):

        self.bg.pos = self.pos

        self.bg.size = self.size