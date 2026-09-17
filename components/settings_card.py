from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior

from kivy.metrics import dp
from kivy.resources import resource_find
from kivy.graphics import Color, RoundedRectangle, Line

from theme import (
    CARD,
    PRIMARY,
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
        self.padding = 0
        self.spacing = 0
        self.size_hint_y = None
        self.height = dp(105)

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

        # AnchorLayout is used because SettingsCard is a horizontal
        # BoxLayout. That makes the complete icon + text group truly
        # centered on the card instead of relying on center_x in the
        # BoxLayout's main axis.
        center = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint=(1, 1)
        )

        content = BoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint=(None, 1),
            width=dp(325)
        )

        icon_holder = AnchorLayout(
            size_hint_x=None,
            width=dp(58),
            size_hint_y=1,
            anchor_x="center",
            anchor_y="center"
        )

        icon_path = resource_find(icon) or icon

        icon_img = Image(
            source=icon_path,
            size_hint=(None, None),
            width=dp(58),
            height=dp(58),
            allow_stretch=True,
            keep_ratio=True,
            opacity=1
        )
        icon_holder.add_widget(icon_img)

        text_box = BoxLayout(
            orientation="vertical",
            spacing=0,
            size_hint_x=None,
            width=dp(255)
        )

        title_label = Label(
            text=title,
            color=PRIMARY,
            font_size=40,
            bold=True,
            halign="left",
            valign="middle",
            size_hint_y=0.58,
            text_size=(dp(255), None)
        )

        subtitle_label = Label(
            text=subtitle,
            color=TEXT_SECONDARY,
            font_size=34,
            halign="left",
            valign="middle",
            size_hint_y=0.42,
            text_size=(dp(255), None)
        )

        text_box.add_widget(title_label)
        text_box.add_widget(subtitle_label)

        content.add_widget(icon_holder)
        content.add_widget(text_box)
        center.add_widget(content)
        self.add_widget(center)

    def on_press(self):
        if self.callback:
            self.callback(self)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

        self.border.rounded_rectangle = (
            self.x,
            self.y,
            self.width,
            self.height,
            22
        )
