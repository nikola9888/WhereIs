import theme
import os
import shutil
import sqlite3
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.app import App
from database import Database
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.image import Image
from components.settings_card import SettingsCard




class SettingsScreen(Screen):


    def __init__(self, **kwargs):

        super().__init__(**kwargs)



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



        root = BoxLayout(

            orientation="vertical",

            spacing=dp(15),

            padding=dp(18)

        )
        
        app = App.get_running_app()


        title_box = BoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(60)
        )


        settings_icon = Image(
            source="assets/icons/settings.png",
            size_hint_x=None,
            width=dp(45),
            allow_stretch=True,
            keep_ratio=True
        )


        title = Label(
            text=app.tr("settings"),
            color=theme.PRIMARY,
            font_size=54,
            bold=True,
            halign="left",
            valign="middle"
        )


        title.bind(
            size=title.setter("text_size")
        )


        title_box.add_widget(settings_icon)
        title_box.add_widget(title)


        root.add_widget(title_box)



        root.add_widget(
            self.create_button(

                app.tr("theme"),

                app.tr("change_theme"),

                "assets/icons/theme.png",

                self.change_theme

            )
        )


        root.add_widget(
            self.create_button(

                app.tr("language"),

                app.tr("choose_language"),

                "assets/icons/language.png",

                self.change_language

            )
        )


        root.add_widget(
            self.create_button(

                app.tr("backup"),

                app.tr("save_data"),

                "assets/icons/backup.png",

                self.backup

            )
        )


        root.add_widget(
            self.create_button(

                app.tr("restore"),

                app.tr("restore_data"),

                "assets/icons/restore.png",

                self.restore

            )
        )


        root.add_widget(
            self.create_button(

                app.tr("clear_data"),

                app.tr("delete_items"),

                "assets/icons/delete.png",

                self.clear_data

            )
        )


        root.add_widget(
            self.create_button(

                app.tr("about"),

                app.tr("whereis_info"),

                "assets/icons/about.png",

                self.about

            )
        )


        back = Button(

            text=app.tr("back"),

            size_hint_y=None,

            height=dp(55),

            background_normal="",

            background_color=theme.PRIMARY,

            color=theme.TEXT,

            font_size=48

        )


        back.bind(

            on_press=self.go_home

        )


        root.add_widget(back)



        self.add_widget(root)


     # =====================================
    # BUTTON
    # =====================================

    def create_button(
        self,
        title,
        subtitle,
        icon,
        callback
    ):

        card = SettingsCard(
            icon=icon,
            title=title,
            subtitle=subtitle,
            callback=callback
        )

        return card
    # =====================================
    # THEME
    # =====================================

    def change_theme(self, instance):

        app = App.get_running_app()

        app.change_theme()


    # =====================================
    # OTHER
    # =====================================


    def change_language(self, instance):

        app = App.get_running_app()


        box = GridLayout(

            cols=1,

            spacing=dp(10),

            padding=dp(15)

        )


        languages = [

            ("English", "en"),
            ("Srpski", "sr"),
            ("Deutsch", "de"),
            ("Français", "fr"),
            ("Español", "es"),
            ("Italiano", "it"),
            ("Русский", "ru")

        ]


        popup = Popup(

            title=app.tr("language"),

            content=box,

            size_hint=(0.8,0.7)

        )


        for name, code in languages:


            btn = Button(

                text=name,

                size_hint_y=None,

                height=dp(55),

                background_normal="",

                background_color=theme.CARD,

                color=theme.TEXT

            )


            btn.bind(

                on_press=lambda x, c=code:
                self.select_language(
                    popup,
                    c
                )

            )


            box.add_widget(btn)



        popup.open()


    def select_language(self, popup, language):


        app = App.get_running_app()


        app.language = language


        app.store.put(

            "app",

            language=language

        )


        popup.dismiss()


        app.root.get_screen(
            "home"
        ).refresh_theme()


        app.root.get_screen(
            "settings"
        ).refresh_theme()
        
        app.root.get_screen(
            "add_item"
        ).refresh_theme()
        
        app.root.get_screen(
            "detail"
        ).refresh_theme()
        
        app.root.get_screen(
            "search"
        ).refresh_theme()
        
    def backup(self, instance):

        app = App.get_running_app()

        source = os.path.join(
            app.user_data_dir,
            "whereis.db"
        )

        destination = "/storage/emulated/0/Download/whereis_backup.db"

        try:

            shutil.copy2(
                source,
                destination
            )

            self.show_message(
                app.tr("backup_title"),
                app.tr("backup_saved") + "\n" + destination
            )

        except Exception as e:

            self.show_message(
                app.tr("error"),
                str(e)
            )
            
    def restore(self, instance):

        app = App.get_running_app()

        backup_file = "/storage/emulated/0/Download/whereis_backup.db"

        database_file = os.path.join(
            app.user_data_dir,
            "whereis.db"
        )


        if not os.path.exists(backup_file):

            self.show_message(
                app.tr("restore_title"),
                app.tr("restore_not_found")
            )

            return


        try:

            shutil.copy2(
                backup_file,
                database_file
            )
 

            self.show_message(
                app.tr("restore_title"),
                app.tr("restore_success")
            )


            home = app.root.get_screen("home")

            home.load_items()


        except Exception as e:

            self.show_message(
                app.tr("restore_error"),
                str(e)
            )
 

    def clear_data(self, instance):

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(15),
            padding=dp(15)
        )

        label = Label(
            text=App.get_running_app().tr("delete_confirm")
        )

        buttons = BoxLayout(
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )

        yes = Button(
            text=App.get_running_app().tr("delete")
        )

        no = Button(
            text=App.get_running_app().tr("cancel")
        )

        buttons.add_widget(yes)
        buttons.add_widget(no)

        content.add_widget(label)
        content.add_widget(buttons)

        popup = Popup(
            title=App.get_running_app().tr("confirm"),
            content=content,
            size_hint=(0.8, 0.4)
        )

        yes.bind(
            on_press=lambda x: self.confirm_clear_data(popup)
        )

        no.bind(
            on_press=popup.dismiss
        )

        popup.open()
        
    def confirm_clear_data(self, popup):

        db = Database()

        db.cursor.execute("DELETE FROM item_history")
        db.cursor.execute("DELETE FROM items")

        db.conn.commit()

        popup.dismiss()

        app = App.get_running_app()

        self.show_message(
            app.tr("done"),
            app.tr("all_items_deleted")
        )

        app = App.get_running_app()

        home = app.root.get_screen("home")
        home.load_items()
        
    def about(self, instance):

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(15),
            padding=dp(15)
        )

        info = Label(
            text=(
                f"WhereIs\n\n"
                f"{App.get_running_app().tr('version_text')}: 1.0.0\n\n"
                f"{App.get_running_app().tr('made_by')}\n\n"
                f"{App.get_running_app().tr('store_items')}\n"
                f"{App.get_running_app().tr('find_items')}"
            ),
            halign="center",
            valign="middle"
        )
 
        info.bind(
            size=info.setter("text_size")
        )

        close = Button(
            text=App.get_running_app().tr("close"),
            size_hint_y=None,
            height=dp(50)
        )

        popup = Popup(
            title=App.get_running_app().tr("about"),
            content=content,
            size_hint=(0.85, 0.55)
        )

        close.bind(
            on_press=popup.dismiss
        )

        content.add_widget(info)
        content.add_widget(close)

        popup.open()

    # =====================================
    # POPUP
    # =====================================


    def show_popup(

        self,

        title,

        message

    ):


        content = Label(

            text=message,

            color=theme.TEXT

        )


        Popup(

            title=title,

            content=content,

            size_hint=(0.7,0.3)

        ).open()





    # =====================================
    # NAVIGATION
    # =====================================


    def go_home(self,instance):

        self.manager.current="home"





    # =====================================
    # BACKGROUND
    # =====================================


    def update_bg(self,*args):

        self.bg.pos=self.pos

        self.bg.size=self.size
        
    def refresh_theme(self):

        self.clear_widgets()

        self.__init__(
            name=self.name
        )
        
    def show_message(self, title, text):

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(15),
            padding=dp(15)
        )

        label = Label(
            text=text
        )

        button = Button(
            text=App.get_running_app().tr("ok"),
            size_hint_y=None,
            height=dp(50)
        )

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.35)
        )

        button.bind(
            on_press=popup.dismiss
        )

        content.add_widget(label)
        content.add_widget(button)

        popup.open()