from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.app import App
from kivy.clock import Clock
from database import Database
import theme
from components.item_card import ItemCard
from components.header import Header

from components.icons import get_icon, ADD, EMPTY


class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = App.get_running_app()
        self.db = Database()

        with self.canvas.before:
            Color(*theme.BACKGROUND)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg, size=self.update_bg)

        root = BoxLayout(
            orientation="vertical",
            spacing=dp(18),
            padding=dp(18)
        )

        self.header = Header()
        root.add_widget(self.header)

        self.scroll = ScrollView(do_scroll_x=False)
        self.list_container = BoxLayout(
            orientation="vertical",
            spacing=dp(15),
            size_hint_y=None
        )
        self.list_container.bind(
            minimum_height=self.list_container.setter("height")
        )
        self.scroll.add_widget(self.list_container)
        root.add_widget(self.scroll)

        self.add_button = Button(
            size_hint_y=None,
            height=dp(64),
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        with self.add_button.canvas.before:
            Color(*theme.PRIMARY)
            self.add_button_bg = RoundedRectangle(
                pos=self.add_button.pos,
                size=self.add_button.size,
                radius=[dp(22)]
            )

        self.add_button.bind(
            pos=self.update_add_button,
            size=self.update_add_button
        )

        button_box = BoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            padding=[dp(20), 0, dp(20), 0]
        )

        icon = Image(
            source=get_icon(ADD),
            size_hint_x=None,
            width=dp(32)
        )

        text = Label(
            text=app.tr("add_item"),
            color=theme.TEXT,
            font_size=30,
            bold=True
        )

        button_box.add_widget(icon)
        button_box.add_widget(text)
        self.add_button.add_widget(button_box)
        self.add_button.bind(on_press=self.open_add_item)
        root.add_widget(self.add_button)

        self.add_widget(root)
        self.load_items()

    def load_items(self):
        self.show_items(self.db.get_all_items())

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
            empty_box.add_widget(Image(
                source=get_icon(EMPTY),
                size_hint_y=None,
                height=dp(70)
            ))
            empty_box.add_widget(Label(
                text=app.tr("no_items"),
                color=theme.TEXT_SECONDARY,
                font_size=24,
                bold=True
            ))
            self.list_container.add_widget(empty_box)
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

            self.list_container.add_widget(ItemCard(
                item_id=item_id,
                name=name,
                category=category or app.tr("other"),
                icon=icon,
                location=location or app.tr("unknown"),
                description=description or "",
                image_path=image_path or ""
            ))

    def open_add_item(self, instance):
        self.manager.current = "add_item"

    def refresh(self):
        self.load_items()

    def refresh_theme(self):
        self.clear_widgets()
        self.__init__(name=self.name)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def update_add_button(self, *args):
        self.add_button_bg.pos = self.add_button.pos
        self.add_button_bg.size = self.add_button.size

    def on_pre_enter(self):
        self.load_items()
