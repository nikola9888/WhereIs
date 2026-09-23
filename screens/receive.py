from kivy.app import App
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.storage.jsonstore import JsonStore
from kivy.graphics import Color, RoundedRectangle, Line

import theme
import os
from components.icons import get_icon, EMPTY
from database import Database
from supabase_client import SupabaseClient


class ReceiveScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.supabase = SupabaseClient()
        self.build_ui()

    def get_profile_id(self):
        store = JsonStore("profile.json")
        if store.exists("profile"):
            return store.get("profile").get("id", "")
        return ""

    def sync_cloud_transfers(self):
        profile_id = self.get_profile_id()
        if not profile_id:
            return

        try:
            transfers = self.supabase.get_pending_transfers(profile_id)
        except Exception as e:
            print("SUPABASE RECEIVE FETCH ERROR:", repr(e))
            return

        for transfer in transfers:
            transfer_id = transfer.get("transfer_id", "")
            if not transfer_id:
                continue

            if self.db.get_transfer(transfer_id):
                try:
                    self.supabase.mark_transfer_received(transfer_id)
                except Exception as e:
                    print("SUPABASE RECEIVE MARK ERROR:", repr(e))
                continue

            name = transfer.get("name", "")
            category = transfer.get("category", "Other")
            location = transfer.get("location", "")
            description = transfer.get("description", "")
            remote_path = transfer.get("image_path", "") or ""
            local_image = ""

            try:
                if remote_path:
                    extension = os.path.splitext(remote_path)[1] or ".jpg"
                    local_image = os.path.join(
                        App.get_running_app().user_data_dir,
                        "received_" + transfer_id + extension
                    )
                    self.supabase.download_file(
                        remote_path,
                        local_image
                    )

                category_id = self.db.get_or_create_category(category)
                item_id = self.db.add_item(
                    name,
                    category_id,
                    location,
                    description,
                    local_image
                )

                self.db.create_item_transfer(
                    transfer_id,
                    None,
                    transfer.get("sender_profile_id", ""),
                    profile_id,
                    name,
                    category_id,
                    location,
                    description,
                    local_image
                )
                self.db.mark_transfer_received(transfer_id)

                self.supabase.mark_transfer_received(transfer_id)

            except Exception as e:
                print("SUPABASE RECEIVE PROCESS ERROR:", repr(e))

    def on_enter(self):
        self.sync_cloud_transfers()
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        app = App.get_running_app()

        with self.canvas.before:
            Color(*theme.BACKGROUND)
            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size
            )

        self.bind(pos=self.update_bg, size=self.update_bg)

        root = BoxLayout(
            orientation="vertical",
            spacing=dp(15),
            padding=dp(18)
        )

        title = Label(
            text="Receive",
            color=theme.PRIMARY,
            font_size=48,
            bold=True,
            size_hint_y=None,
            height=dp(60)
        )
        root.add_widget(title)

        received = self.db.get_received_transfers()

        if not received:
            empty_card = BoxLayout(
                orientation="vertical",
                spacing=dp(10),
                padding=dp(18),
                size_hint_y=None,
                height=dp(230)
            )

            with empty_card.canvas.before:
                Color(*theme.CARD)
                empty_card.bg = RoundedRectangle(
                    pos=empty_card.pos,
                    size=empty_card.size,
                    radius=[dp(22)]
                )

            with empty_card.canvas.after:
                Color(*theme.ITEM_BORDER)
                empty_card.border = Line(
                    rounded_rectangle=(
                        empty_card.x,
                        empty_card.y,
                        empty_card.width,
                        empty_card.height,
                        dp(22)
                    ),
                    width=1.2
                )

            empty_card.bind(
                pos=self.update_card,
                size=self.update_card
            )

            empty_card.add_widget(Image(
                source=get_icon(EMPTY),
                size_hint_y=None,
                height=dp(90),
                allow_stretch=True,
                keep_ratio=True
            ))

            empty_card.add_widget(Label(
                text="Trenutno nema primljenih itema.",
                color=theme.TEXT_SECONDARY,
                font_size=30,
                bold=True,
                halign="center",
                valign="middle"
            ))

            root.add_widget(empty_card)

        else:
            scroll = ScrollView(
                do_scroll_x=False
            )

            items_box = BoxLayout(
                orientation="vertical",
                spacing=dp(12),
                size_hint_y=None
            )
            items_box.bind(
                minimum_height=items_box.setter("height")
            )

            for transfer in received:
                (
                    transfer_db_id,
                    transfer_id,
                    item_id,
                    sender_profile_id,
                    recipient_profile_id,
                    name,
                    category_id,
                    location,
                    description,
                    image_path,
                    status,
                    created_at,
                    received_at
                ) = transfer

                card = BoxLayout(
                    orientation="vertical",
                    spacing=dp(8),
                    padding=dp(15),
                    size_hint_y=None,
                    height=dp(220)
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
                        rounded_rectangle=(
                            card.x,
                            card.y,
                            card.width,
                            card.height,
                            dp(22)
                        ),
                        width=1.2
                    )

                card.bind(
                    pos=self.update_card,
                    size=self.update_card
                )

                if image_path:
                    import os
                    if os.path.exists(image_path):
                        card.add_widget(Image(
                            source=image_path,
                            size_hint_y=None,
                            height=dp(90),
                            allow_stretch=True,
                            keep_ratio=True
                        ))

                card.add_widget(Label(
                    text=name,
                    color=theme.PRIMARY,
                    font_size=38,
                    bold=True,
                    size_hint_y=None,
                    height=dp(48)
                ))

                card.add_widget(Label(
                    text=(
                        "From: " + sender_profile_id +
                        "\nLocation: " + (location or "-") +
                        "\n" + (description or "-")
                    ),
                    color=theme.TEXT,
                    font_size=28,
                    halign="left",
                    valign="middle"
                ))

                items_box.add_widget(card)

            scroll.add_widget(items_box)
            root.add_widget(scroll)

        root.add_widget(BoxLayout())

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
