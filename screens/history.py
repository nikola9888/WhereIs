from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.metrics import dp

from database import Database
from theme import TEXT, PRIMARY, CARD


class HistoryScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.db = Database()


        root = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(15)
        )


        # TITLE

        title = Label(
            text="📜 History",
            font_size=32,
            color=PRIMARY,
            size_hint_y=None,
            height=dp(55)
        )

        root.add_widget(title)



        # LIST

        scroll = ScrollView()


        self.list_container = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None
        )


        self.list_container.bind(
            minimum_height=
            self.list_container.setter("height")
        )


        scroll.add_widget(
            self.list_container
        )


        root.add_widget(scroll)



        # BACK

        back = Button(
            text="← Back",
            size_hint_y=None,
            height=dp(50),
            background_normal="",
            background_down="",
            background_color=PRIMARY,
            color=TEXT
        )


        back.bind(
            on_press=self.go_home
        )


        root.add_widget(back)


        self.add_widget(root)


        self.load_history()



    def load_history(self):

        self.list_container.clear_widgets()


        rows = self.db.get_history()


        for row in rows:

            (
                item_name,
                action,
                location,
                time

            ) = row


            card = BoxLayout(

                orientation="vertical",

                padding=dp(12),

                spacing=dp(5),

                size_hint_y=None,

                height=dp(90)

            )


            card.canvas.before.add(
                # kasnije ubacujemo RoundedRectangle
            )


            label = Label(

                text=
                f"{item_name}\n"
                f"{action}\n"
                f"📍 {location}\n"
                f"{time}",

                color=TEXT,

                halign="left"

            )


            card.add_widget(label)


            self.list_container.add_widget(card)



    def go_home(self, instance):

        self.manager.current = "home"