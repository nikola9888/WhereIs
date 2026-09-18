import uuid

import theme
from kivy.app import App
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Line


class ProfileScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.store = JsonStore("profile.json")
        self.profile_id = self.get_profile_id()
        self.build_ui()

    def get_profile_id(self):
        if self.store.exists("profile"):
            value = self.store.get("profile")
            return value.get("id") or self.create_profile_id()
        return self.create_profile_id()

    def create_profile_id(self):
        profile_id = str(uuid.uuid4()).replace("-", "")[:12].upper()
        self.store.put("profile", id=profile_id, name="")
        return profile_id

    def build_ui(self):
        self.clear_widgets()
        app = App.get_running_app()

        with self.canvas.before:
            Color(*theme.BACKGROUND)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg, size=self.update_bg)

        root = BoxLayout(
            orientation="vertical",
            spacing=dp(15),
            padding=dp(18)
        )

        title = Label(
            text="Profile",
            color=theme.PRIMARY,
            font_size=48,
            bold=True,
            size_hint_y=None,
            height=dp(60)
        )
        root.add_widget(title)

        card = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(18),
            size_hint_y=None,
            height=dp(230)
        )

        with card.canvas.before:
            Color(*theme.CARD)
            card.bg = RoundedRectangle(
                pos=card.pos,
                size=card.size,
                radius=[dp(22)]
            )

        with card.canvas.after:
            Color(*theme.ITEM_BORDER)
            card.border = Line(
                rounded_rectangle=(card.x, card.y, card.width, card.height, dp(22)),
                width=1.2
            )

        card.bind(pos=self.update_card, size=self.update_card)

        card.add_widget(Label(
            text="Profile ID",
            color=theme.TEXT_SECONDARY,
            font_size=48,
            size_hint_y=None,
            height=dp(55)
        ))

        card.add_widget(Label(
            text=self.profile_id,
            color=theme.PRIMARY,
            font_size=68,
            bold=True,
            size_hint_y=None,
            height=dp(75)
        ))

        self.name_input = self.create_input(
            "Profile name"
        )
        card.add_widget(self.name_input)
        self.add_input_background(
            card,
            self.name_input,
            theme.BACKGROUND_DARK
        )

        save = self.create_round_button(
            "Save profile",
            theme.PRIMARY,
            theme.TEXT,
            52,
            22,
            91.8,
            True
        )
        save.bind(on_press=self.save_profile)
        card.add_widget(save)

        root.add_widget(card)

        root.add_widget(Label(
            text="Connections",
            color=theme.PRIMARY,
            font_size=68,
            bold=True,
            size_hint_y=None,
            height=dp(80)
        ))

        self.connection_input = self.create_input(
            "Enter another Profile ID"
        )
        root.add_widget(self.connection_input)
        self.add_input_background(
            root,
            self.connection_input,
            theme.CARD
        )

        connect = self.create_round_button(
            "Add connection",
            theme.PRIMARY,
            theme.TEXT,
            52,
            22,
            91.8,
            True
        )
        connect.bind(on_press=self.add_connection)
        root.add_widget(connect)

        self.connections_label = Label(
            text=self.connections_text(),
            color=theme.TEXT_SECONDARY,
            font_size=63.36,
            halign="left",
            valign="top",
            size_hint_y=None,
            height=dp(100)
        )
        self.connections_label.bind(
            size=self.connections_label.setter("text_size")
        )
        root.add_widget(self.connections_label)

        back = self.create_round_button(
            app.tr("back"),
            theme.CARD,
            theme.TEXT,
            55,
            22,
            107.1,
            True
        )
        back.bind(on_press=self.go_back)
        root.add_widget(back)

        self.add_widget(root)

    def create_round_button(
        self,
        text,
        background,
        color,
        height,
        radius,
        font_size,
        bold=False
    ):
        button = Button(
            text=text,
            size_hint_y=None,
            height=dp(height),
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0),
            color=color,
            font_size=font_size,
            bold=bold
        )

        with button.canvas.before:
            Color(*background)
            button.bg_rect = RoundedRectangle(
                pos=button.pos,
                size=button.size,
                radius=[dp(radius)]
            )

        with button.canvas.after:
            Color(*theme.ITEM_BORDER)
            button.border_line = Line(
                rounded_rectangle=(
                    button.x,
                    button.y,
                    button.width,
                    button.height,
                    dp(radius)
                ),
                width=1
            )

        def update(widget, *args):
            widget.bg_rect.pos = widget.pos
            widget.bg_rect.size = widget.size
            widget.border_line.rounded_rectangle = (
                widget.x,
                widget.y,
                widget.width,
                widget.height,
                dp(radius)
            )

        button.bind(pos=update, size=update)
        return button

    def create_input(self, hint):
        box = TextInput(
            text=self.get_profile_name() if hint == "Profile name" else "",
            hint_text=hint,
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            background_normal="",
            background_active="",
            background_color=(0, 0, 0, 0),
            foreground_color=theme.WHITE,
            hint_text_color=theme.TEXT_SECONDARY,
            font_size=32,
            cursor_color=theme.PRIMARY,
            padding=[dp(12), dp(10)]
        )
        return box

    def add_input_background(self, parent, input_widget, background):
        with parent.canvas.before:
            Color(*background)
            rect = RoundedRectangle(
                pos=input_widget.pos,
                size=input_widget.size,
                radius=[dp(16)]
            )

        def update_input(widget, *args):
            rect.pos = widget.pos
            rect.size = widget.size

        input_widget.bind(pos=update_input, size=update_input)
        update_input(input_widget)

    def get_profile_name(self):
        if self.store.exists("profile"):
            return self.store.get("profile").get("name", "")
        return ""

    def get_connections(self):
        if self.store.exists("connections"):
            return self.store.get("connections").get("ids", [])
        return []

    def connections_text(self):
        connections = self.get_connections()
        if not connections:
            return "No connected profiles yet."
        return "\n".join("• " + value for value in connections)

    def save_profile(self, instance):
        self.store.put(
            "profile",
            id=self.profile_id,
            name=self.name_input.text.strip()
        )

    def add_connection(self, instance):
        value = self.connection_input.text.strip().upper()

        if not value or value == self.profile_id:
            return

        connections = self.get_connections()

        if value not in connections:
            connections.append(value)
            self.store.put("connections", ids=connections)

        self.connection_input.text = ""
        self.connections_label.text = self.connections_text()

    def go_back(self, instance):
        self.manager.current = "home"

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def update_card(self, card, *args):
        card.bg.pos = card.pos
        card.bg.size = card.size
        card.border.rounded_rectangle = (
            card.x,
            card.y,
            card.width,
            card.height,
            dp(22)
        )

    def refresh_theme(self):
        self.build_ui()
