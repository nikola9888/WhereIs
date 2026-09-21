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

            background_down="",

            background_color=(0, 0, 0, 0),

            color=theme.TEXT,

            font_size=48

        )

        with back.canvas.before:
            Color(*theme.PRIMARY)
            back.bg_rect = RoundedRectangle(
                pos=back.pos,
                size=back.size,
                radius=[dp(22)]
            )

        def update_back(widget, *args):
            widget.bg_rect.pos = widget.pos
            widget.bg_rect.size = widget.size

        back.bind(pos=update_back, size=update_back)
        update_back(back)


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

        try:

            if not os.path.exists(source):
                raise FileNotFoundError(source)

            # Android 10+ blocks direct filesystem writes to shared
            # storage. Use MediaStore so the backup is saved normally
            # into the public Downloads folder without storage permission.
            from jnius import autoclass, cast

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            MediaStore = autoclass("android.provider.MediaStore")
            MediaColumns = autoclass("android.provider.MediaStore$MediaColumns")
            Downloads = autoclass("android.provider.MediaStore$Downloads")
            Files = autoclass("android.provider.MediaStore$Files")
            ContentValues = autoclass("android.content.ContentValues")
            JavaInteger = autoclass("java.lang.Integer")
            BuildVersion = autoclass("android.os.Build$VERSION")

            activity = PythonActivity.mActivity
            resolver = activity.getContentResolver()

            values = ContentValues()
            values.put(MediaColumns.DISPLAY_NAME, "whereis_backup.db")
            values.put(MediaColumns.MIME_TYPE, "application/octet-stream")

            if BuildVersion.SDK_INT >= 29:
                values.put(MediaColumns.RELATIVE_PATH, "Download/")
                values.put(MediaColumns.IS_PENDING, JavaInteger(1))
                collection = Downloads.EXTERNAL_CONTENT_URI
            else:
                collection = Files.getContentUri("external")

            uri = resolver.insert(collection, values)

            if uri is None:
                raise IOError("Could not create backup file")

            try:
                output_stream = resolver.openOutputStream(uri)
                with open(source, "rb") as input_file:
                    data = input_file.read()
                output_stream.write(data)
                output_stream.close()

                if BuildVersion.SDK_INT >= 29:
                    values = ContentValues()
                    values.put(MediaColumns.IS_PENDING, JavaInteger(0))
                    resolver.update(uri, values, None, None)

                # Keep the exact MediaStore URI that Android created.
                # Restore can then reopen this file directly instead of
                # trying to find it again by filename/path.
                app.store.put(
                    "backup",
                    uri=str(uri),
                    name="whereis_backup.db"
                )

            except Exception:
                resolver.delete(uri, None, None)
                raise

            self.show_message(
                app.tr("backup_title"),
                app.tr("backup_saved") + "\nDownload/whereis_backup.db"
            )

        except Exception as e:

            self.show_message(
                app.tr("error"),
                str(e)
            )
            
    def restore(self, instance):

        app = App.get_running_app()

        database_file = os.path.join(
            app.user_data_dir,
            "whereis.db"
        )

        try:

            # First try the exact MediaStore URI saved when the backup
            # was created. This is the most reliable method because Android
            # may expose Downloads differently between devices/versions.
            saved_uri = None
            if app.store.exists("backup"):
                try:
                    saved_uri = app.store.get("backup").get("uri")
                except Exception:
                    saved_uri = None

            if saved_uri:
                try:
                    from jnius import autoclass
                    PythonActivity = autoclass(
                        "org.kivy.android.PythonActivity"
                    )
                    Uri = autoclass("android.net.Uri")

                    activity = PythonActivity.mActivity
                    resolver = activity.getContentResolver()
                    uri = Uri.parse(saved_uri)
                    input_stream = resolver.openInputStream(uri)

                    if input_stream is not None:
                        with open(database_file, "wb") as output_file:
                            buffer = bytearray(8192)
                            while True:
                                count = input_stream.read(buffer)
                                if count <= 0:
                                    break
                                output_file.write(buffer[:count])

                        input_stream.close()

                        self.show_message(
                            app.tr("restore_title"),
                            app.tr("restore_success")
                        )

                        home = app.root.get_screen("home")
                        home.load_items()
                        return
                except Exception:
                    # If the saved URI is no longer valid, continue with the
                    # existing MediaStore/file fallback below.
                    pass

            # Android 10+ shared storage must be read through MediaStore.
            from jnius import autoclass

            MediaStore = autoclass("android.provider.MediaStore")
            MediaColumns = autoclass(
                "android.provider.MediaStore$MediaColumns"
            )
            Downloads = autoclass(
                "android.provider.MediaStore$Downloads"
            )
            BuildVersion = autoclass("android.os.Build$VERSION")
            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            if BuildVersion.SDK_INT >= 29:

                activity = PythonActivity.mActivity
                resolver = activity.getContentResolver()

                # The backup is created in MediaStore Downloads, so restore
                # must query the same Downloads collection. Querying the
                # generic Files collection can miss files inserted through
                # MediaStore.Downloads on Android 10+.
                collection = Downloads.EXTERNAL_CONTENT_URI

                projection = [MediaColumns._ID]

                # Match both the filename and the exact Downloads folder.
                # RELATIVE_PATH is stored by Android with a trailing slash.
                selection = (
                    MediaColumns.DISPLAY_NAME + "=? AND " +
                    MediaColumns.RELATIVE_PATH + "=?"
                )
                selection_args = [
                    "whereis_backup.db",
                    "Download/"
                ]

                cursor = resolver.query(
                    collection,
                    projection,
                    selection,
                    selection_args,
                    None
                )

                # Some Android versions expose Downloads through the
                # generic external-files collection. If the Downloads
                # collection returns nothing, try that collection too.
                if cursor is None or not cursor.moveToFirst():

                    if cursor is not None:
                        cursor.close()

                    Files = autoclass(
                        "android.provider.MediaStore$Files"
                    )
                    collection = Files.getContentUri("external")

                    cursor = resolver.query(
                        collection,
                        projection,
                        selection,
                        selection_args,
                        None
                    )

                if cursor is None or not cursor.moveToFirst():

                    if cursor is not None:
                        cursor.close()

                    self.open_restore_file_picker()
                    return

                column_index = cursor.getColumnIndexOrThrow(
                    MediaColumns._ID
                )
                file_id = cursor.getLong(column_index)
                cursor.close()

                from android.net import Uri

                uri = Uri.withAppendedPath(
                    collection,
                    str(file_id)
                )

                input_stream = resolver.openInputStream(uri)

                if input_stream is None:
                    raise IOError(
                        "Could not open backup file"
                    )

                with open(database_file, "wb") as output_file:

                    buffer = bytearray(8192)

                    while True:

                        count = input_stream.read(buffer)

                        if count <= 0:
                            break

                        output_file.write(buffer[:count])

                input_stream.close()

            else:

                backup_file = (
                    "/storage/emulated/0/Download/"
                    "whereis_backup.db"
                )

                if not os.path.exists(backup_file):

                    self.open_restore_file_picker()
                    return

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


    RESTORE_REQUEST_CODE = 301

    def open_restore_file_picker(self):
        try:
            from jnius import autoclass

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )
            Intent = autoclass(
                "android.content.Intent"
            )

            intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
            intent.addCategory(Intent.CATEGORY_OPENABLE)
            intent.setType("*/*")

            PythonActivity.mActivity.startActivityForResult(
                intent,
                self.RESTORE_REQUEST_CODE
            )

        except Exception as e:
            self.show_message(
                App.get_running_app().tr("restore_error"),
                str(e)
            )

    def on_restore_result(
        self,
        request_code,
        result_code,
        intent
    ):
        if request_code != self.RESTORE_REQUEST_CODE:
            return

        if result_code != -1 or intent is None:
            return

        try:
            app = App.get_running_app()
            uri = intent.getData()

            if uri is None:
                raise IOError("No backup file selected")

            PythonActivity = __import__(
                "jnius"
            ).autoclass(
                "org.kivy.android.PythonActivity"
            )

            activity = PythonActivity.mActivity
            resolver = activity.getContentResolver()
            input_stream = resolver.openInputStream(uri)

            if input_stream is None:
                raise IOError("Could not open selected backup file")

            database_file = os.path.join(
                app.user_data_dir,
                "whereis.db"
            )

            home = app.root.get_screen("home")

            try:
                home.db.close()
            except Exception:
                pass

            with open(database_file, "wb") as output_file:
                buffer = bytearray(8192)

                while True:
                    count = input_stream.read(buffer)

                    if count <= 0:
                        break

                    output_file.write(buffer[:count])

            input_stream.close()

            # Reopen the database connection after replacing the file.
            home.db = Database()

            app.store.put(
                "backup",
                uri=str(uri),
                name="whereis_backup.db"
            )

            self.show_message(
                app.tr("restore_title"),
                app.tr("restore_success")
            )

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
            text=text,
            color=theme.TEXT,
            halign="center",
            valign="middle"
        )
        label.bind(
            size=label.setter("text_size")
        )

        button = Button(
            text=App.get_running_app().tr("ok"),
            size_hint_y=None,
            height=dp(50)
        )

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.45)
        )

        button.bind(
            on_press=popup.dismiss
        )

        content.add_widget(label)
        content.add_widget(button)

        popup.open()