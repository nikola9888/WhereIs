import os
import time

import theme

from camera import Camera
from database import Database
from image_manager import ImageManager

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image


class AddItemScreen(Screen):

    CAMERA_REQUEST_CODE = 200
    GALLERY_REQUEST_CODE = 201

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.db = Database()
        self.image_manager = ImageManager()
        self.image_path = ""
        self.edit_mode = False
        self.edit_id = None

        self.camera = Camera(
            request_code=self.CAMERA_REQUEST_CODE,
            on_image=self.on_camera_image
        )

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

        scroll = ScrollView(do_scroll_x=False)

        self.root_box = BoxLayout(
            orientation="vertical",
            spacing=dp(18),
            padding=dp(20),
            size_hint_y=None
        )

        self.root_box.bind(
            minimum_height=self.root_box.setter("height")
        )

        scroll.add_widget(self.root_box)
        self.add_widget(scroll)

        app = App.get_running_app()

        self.title = Label(
            text=app.tr("add_item"),
            color=theme.PRIMARY,
            font_size=42,
            bold=True,
            size_hint_y=None,
            height=dp(90)
        )
        self.root_box.add_widget(self.title)

        self.name_input = self.create_input(
            app.tr("item_name"), False, 65
        )
        self.root_box.add_widget(self.name_input)

        self.location_input = self.create_input(
            app.tr("location"), False, 65
        )
        self.root_box.add_widget(self.location_input)

        self.description_input = self.create_input(
            app.tr("description"), True, 140
        )
        self.root_box.add_widget(self.description_input)

        self.category_spinner = Spinner(
            text=app.tr("choose_category"),
            size_hint_y=None,
            height=95,
            background_normal="",
            background_color=theme.CARD,
            color=theme.PRIMARY,
            font_size=40
        )
        self.root_box.add_widget(self.category_spinner)
        self.load_categories()

        self.preview = Image(
            source="",
            size_hint=(1, None),
            height=dp(200),
            fit_mode="contain"
        )
        self.root_box.add_widget(self.preview)

        self.image_button = Button(
            text=app.tr("add_photo"),
            size_hint_y=None,
            height=90,
            background_normal="",
            background_color=theme.CARD,
            color=theme.TEXT,
            font_size=40
        )
        self.image_button.bind(on_press=self.choose_image)
        self.root_box.add_widget(self.image_button)

        self.save_button = Button(
            text=app.tr("save_item"),
            size_hint_y=None,
            height=95,
            background_normal="",
            background_color=theme.PRIMARY,
            color=theme.TEXT,
            font_size=42,
            bold=True
        )
        self.save_button.bind(on_press=self.save_item)
        self.root_box.add_widget(self.save_button)

        back = Button(
            text=app.tr("back"),
            size_hint_y=None,
            height=90,
            background_normal="",
            background_color=theme.CARD,
            color=theme.TEXT,
            font_size=45,
            bold=True
        )
        back.bind(on_press=self.go_back)
        self.root_box.add_widget(back)

    def on_activity_result(self, request_code, result_code, intent):
        if request_code == self.CAMERA_REQUEST_CODE:
            try:
                self.camera.handle_result(
                    request_code,
                    result_code,
                    intent
                )
            except Exception as e:
                print("CAMERA RESULT ERROR:", repr(e))
            return

        if request_code == self.GALLERY_REQUEST_CODE:
            self.handle_gallery_result(result_code, intent)

    def create_input(self, hint, multiline, height):
        box = TextInput(
            hint_text=hint,
            multiline=multiline,
            size_hint_y=None,
            height=dp(height),
            background_normal="",
            background_active="",
            background_color=theme.CARD,
            foreground_color=theme.TEXT,
            hint_text_color=theme.TEXT_SECONDARY,
            font_size=62,
            padding=[dp(3), dp(3)]
        )

        with box.canvas.after:
            Color(*theme.INPUT_BORDER)
            box.border_line = Line(
                rounded_rectangle=(
                    box.x,
                    box.y,
                    box.width,
                    box.height,
                    18
                ),
                width=1
            )

        box.bind(
            pos=self.update_input_border,
            size=self.update_input_border
        )
        return box

    def update_input_border(self, widget, *args):
        if hasattr(widget, "border_line"):
            widget.border_line.rounded_rectangle = (
                widget.x,
                widget.y,
                widget.width,
                widget.height,
                18
            )

    def load_categories(self):
        app = App.get_running_app()
        values = []

        for cat in self.db.get_categories():
            values.append(app.tr(cat[1].lower()))

        self.category_spinner.values = values

    def get_selected_category_id(self):
        app = App.get_running_app()
        selected = self.category_spinner.text

        for cat in self.db.get_categories():
            if app.tr(cat[1].lower()) == selected:
                return cat[0]

        return None

    def choose_image(self, instance):
        from kivy.uix.popup import Popup

        box = BoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=dp(20)
        )

        camera = Button(
            text=App.get_running_app().tr("camera"),
            size_hint_y=None,
            height=80
        )

        gallery = Button(
            text=App.get_running_app().tr("gallery"),
            size_hint_y=None,
            height=80
        )

        popup = Popup(
            title=App.get_running_app().tr("select_image"),
            content=box,
            size_hint=(0.8, 0.4)
        )

        camera.bind(
            on_press=lambda btn: self._select_camera(popup)
        )
        gallery.bind(
            on_press=lambda btn: self._select_gallery(popup)
        )

        box.add_widget(camera)
        box.add_widget(gallery)
        popup.open()

    def _select_camera(self, popup):
        popup.dismiss()
        Clock.schedule_once(lambda dt: self.open_camera(), 0.15)

    def _select_gallery(self, popup):
        popup.dismiss()
        Clock.schedule_once(lambda dt: self.open_gallery(), 0.15)

    def open_camera(self):
        try:
            from android.permissions import (
                request_permissions,
                check_permission,
                Permission
            )

            def launch_camera(*args):
                def attempt_open(dt):
                    try:
                        if check_permission(Permission.CAMERA):
                            print("CAMERA: PERMISSION CONFIRMED")
                            self.camera.open()
                        else:
                            print("CAMERA: PERMISSION STILL NOT GRANTED")
                    except Exception as e:
                        print("CAMERA LAUNCH AFTER PERMISSION ERROR:", repr(e))

                Clock.schedule_once(attempt_open, 0.5)

            # Important: if permission was already granted, do not request it
            # again. Launch the camera directly. This avoids Android returning
            # from the permission flow without starting the camera intent.
            if check_permission(Permission.CAMERA):
                print("CAMERA: PERMISSION ALREADY GRANTED")
                Clock.schedule_once(
                    lambda dt: self.camera.open(),
                    0.1
                )
                return

            print("CAMERA: REQUESTING PERMISSION")
            request_permissions(
                [Permission.CAMERA],
                launch_camera
            )

        except Exception as e:
            print("CAMERA PERMISSION ERROR:", repr(e))
            try:
                self.camera.open()
            except Exception as camera_error:
                print("OPEN CAMERA ERROR:", repr(camera_error))

    def on_camera_image(self, path):
        if not path or not os.path.isfile(path):
            print("CAMERA FILE INVALID:", path)
            return

        try:
            if os.path.getsize(path) <= 0:
                print("CAMERA FILE EMPTY")
                return
        except Exception:
            return

        converted = self.image_manager.copy_and_resize(
            path,
            max_size=1600,
            quality=92
        )

        if converted:
            self.image_path = converted
            self.set_preview(converted)
        else:
            self.image_path = path
            self.set_preview(path)

    def open_gallery(self):
        try:
            from jnius import autoclass

            Intent = autoclass("android.content.Intent")
            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            activity = PythonActivity.mActivity

            intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
            intent.addCategory(Intent.CATEGORY_OPENABLE)
            intent.setType("image/*")
            intent.addFlags(
                Intent.FLAG_GRANT_READ_URI_PERMISSION
                | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION
            )

            activity.startActivityForResult(
                intent,
                self.GALLERY_REQUEST_CODE
            )

        except Exception as e:
            print("OPEN GALLERY ERROR:", repr(e))

    def handle_gallery_result(self, result_code, intent):
        try:
            from jnius import autoclass

            Activity = autoclass("android.app.Activity")

            if result_code != Activity.RESULT_OK or intent is None:
                return

            uri = intent.getData()
            if uri is None:
                return

            self.copy_android_uri(uri)

        except Exception as e:
            print("GALLERY RESULT ERROR:", repr(e))

    def copy_android_uri(self, uri):
        try:
            from jnius import autoclass

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )
            FileOutputStream = autoclass(
                "java.io.FileOutputStream"
            )

            activity = PythonActivity.mActivity
            resolver = activity.getContentResolver()
            stream = resolver.openInputStream(uri)

            if stream is None:
                print("GALLERY: INPUT STREAM NONE")
                return

            app = App.get_running_app()
            image_dir = os.path.join(app.user_data_dir, "images")
            os.makedirs(image_dir, exist_ok=True)

            raw_path = os.path.join(
                image_dir,
                "gallery_raw_" + str(int(time.time() * 1000))
            )

            output = FileOutputStream(raw_path)

            try:
                buffer = bytearray(64 * 1024)
                while True:
                    count = stream.read(buffer)
                    if count <= 0:
                        break
                    output.write(buffer, 0, count)
            finally:
                try:
                    stream.close()
                except Exception:
                    pass
                try:
                    output.close()
                except Exception:
                    pass

            if not os.path.isfile(raw_path) or os.path.getsize(raw_path) <= 0:
                print("GALLERY: COPY FAILED")
                return

            converted = self.image_manager.copy_and_resize(
                raw_path,
                max_size=1600,
                quality=92
            )

            if not converted:
                print("GALLERY: IMAGE CONVERSION FAILED")
                return

            try:
                os.remove(raw_path)
            except Exception:
                pass

            self.image_path = converted
            self.set_preview(converted)
            print("GALLERY IMAGE:", converted)

        except Exception as e:
            print("COPY GALLERY IMAGE ERROR:", repr(e))

    def set_preview(self, path):
        """Load a newly-created local image after the file is fully ready.

        Android/Kivy can otherwise start loading the file while the previous
        texture is still attached to the Image widget. The result can be a
        black preview until the app is restarted. The short scheduled reloads
        force Kivy to read the finished JPEG again without changing the saved
        file path in the database.
        """
        if not path or not os.path.isfile(path):
            print("PREVIEW FILE INVALID:", path)
            return

        try:
            if os.path.getsize(path) <= 0:
                print("PREVIEW FILE EMPTY:", path)
                return
        except Exception as e:
            print("PREVIEW FILE CHECK ERROR:", repr(e))
            return

        def reload_preview(*args):
            try:
                if not os.path.isfile(path):
                    return

                if os.path.getsize(path) <= 0:
                    return

                self.preview.texture = None
                self.preview.source = ""
                self.preview.source = path
                self.preview.reload()

                print("PREVIEW RELOADED:", path)

            except Exception as e:
                print("PREVIEW RELOAD ERROR:", repr(e))

        try:
            self.preview.texture = None
            self.preview.source = ""
        except Exception:
            pass

        # First load on the next Kivy frame, then repeat after the file and
        # Android/Kivy texture pipeline have had time to settle.
        Clock.schedule_once(reload_preview, 0.05)
        Clock.schedule_once(reload_preview, 0.25)
        Clock.schedule_once(reload_preview, 0.60)

    def save_item(self, instance):
        app = App.get_running_app()

        name = self.name_input.text.strip()
        if not name:
            print("NAME REQUIRED")
            return

        location = self.location_input.text.strip()
        description = self.description_input.text.strip()
        category_id = self.get_selected_category_id()
        image_path = self.image_path or ""

        if image_path and (
            not os.path.isfile(image_path)
            or os.path.getsize(image_path) <= 0
        ):
            image_path = ""

        try:
            if self.edit_mode:
                self.db.update_item(
                    self.edit_id,
                    name,
                    category_id,
                    location,
                    description,
                    image_path
                )
                self.db.add_history(
                    self.edit_id,
                    "Updated",
                    location
                )
            else:
                item_id = self.db.add_item(
                    name,
                    category_id,
                    location,
                    description,
                    image_path
                )
                self.db.add_history(
                    item_id,
                    "Created",
                    location
                )
        except Exception as e:
            print("SAVE ITEM ERROR:", repr(e))
            return

        self.clear_form()
        self.manager.current = "home"

        try:
            self.manager.get_screen("home").load_items()
        except Exception as e:
            print("HOME REFRESH ERROR:", repr(e))

    def load_edit_item(self, item_id):
        self.edit_mode = True
        self.edit_id = item_id

        item = self.db.get_item(item_id)
        if not item:
            return

        (
            _,
            name,
            category_id,
            location,
            description,
            image_path,
            _,
            _
        ) = item

        app = App.get_running_app()
        self.title.text = app.tr("edit_item")
        self.save_button.text = app.tr("update_item")
        self.name_input.text = name or ""
        self.location_input.text = location or ""
        self.description_input.text = description or ""
        self.image_path = image_path or ""

        if self.image_path and os.path.isfile(self.image_path):
            self.set_preview(self.image_path)

        for cat in self.db.get_categories():
            if cat[0] == category_id:
                self.category_spinner.text = app.tr(cat[1].lower())
                break

    def clear_form(self):
        self.edit_mode = False
        self.edit_id = None

        app = App.get_running_app()
        self.title.text = app.tr("add_item")
        self.save_button.text = app.tr("save_item")
        self.name_input.text = ""
        self.location_input.text = ""
        self.description_input.text = ""
        self.category_spinner.text = app.tr("choose_category")
        self.image_path = ""
        self.preview.source = ""

    def go_back(self, instance):
        self.manager.current = "home"

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def refresh_theme(self):
        self.clear_widgets()
        self.__init__(name=self.name)