import os

import theme
from camera import Camera
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.app import App
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.clock import Clock
from database import Database
from image_manager import ImageManager


class AddItemScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        app = App.get_running_app()

        self.db = Database()

        self.image_manager = ImageManager()

        self.image_path = ""

        self.camera_request_code = 200

        self.camera = Camera(
            request_code=self.camera_request_code,
            on_image=self.on_camera_image
        )

        self.edit_mode = False

        self.edit_id = None
 
        # =====================================================
        # BACKGROUND
        # =====================================================

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

        # =====================================================
        # SCROLL
        # =====================================================

        scroll = ScrollView(
            do_scroll_x=False
        )

        self.root_box = BoxLayout(
            orientation="vertical",
            spacing=dp(18),
            padding=dp(20),
            size_hint_y=None
        )

        self.root_box.bind(
            minimum_height=self.root_box.setter(
                "height"
            )
        )

        scroll.add_widget(
            self.root_box
        )

        self.add_widget(
            scroll
        )

        # =====================================================
        # TITLE
        # =====================================================

        self.title = Label(
            text=app.tr("add_item"),
            color=theme.PRIMARY,
            font_size=42,
            bold=True,
            size_hint_y=None,
            height=dp(90)
        )

        self.root_box.add_widget(
            self.title
        )

        # =====================================================
        # NAME
        # =====================================================

        self.name_input = self.create_input(
            app.tr("item_name"),
            False,
            65
        )

        self.root_box.add_widget(
            self.name_input
        )

        # =====================================================
        # LOCATION
        # =====================================================

        self.location_input = self.create_input(
            app.tr("location"),
            False,
            65
        )

        self.root_box.add_widget(
            self.location_input
        )

        # =====================================================
        # DESCRIPTION
        # =====================================================

        self.description_input = self.create_input(
            app.tr("description"),
            True,
            140
        )

        self.root_box.add_widget(
            self.description_input
        )

        # =====================================================
        # CATEGORY
        # =====================================================

        self.category_spinner = Spinner(
            text=app.tr("choose_category"),
            size_hint_y=None,
            height=95,
            background_normal="",
            background_color=theme.CARD,
            color=theme.PRIMARY,
            font_size=40
        )

        self.root_box.add_widget(
            self.category_spinner
        )

        self.load_categories()

        # =====================================================
        # IMAGE PREVIEW
        # =====================================================

        self.preview = Image(
            source="",
            size_hint=(1, None),
            height=dp(200),
            fit_mode="contain"
        )

        self.root_box.add_widget(
            self.preview
        )


        # =====================================================
        # IMAGE BUTTON
        # =====================================================

        self.image_button = Button(
            text=app.tr("add_photo"),
            size_hint_y=None,
            height=90,
            background_normal="",
            background_color=theme.CARD,
            color=theme.TEXT,
            font_size=40
        )

        self.image_button.bind(
            on_press=self.choose_image
        )

        self.root_box.add_widget(
            self.image_button
        )

        # =====================================================
        # SAVE BUTTON
        # =====================================================

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

        self.save_button.bind(
            on_press=self.save_item
        )

        self.root_box.add_widget(
            self.save_button
        )

        # =====================================================
        # BACK BUTTON
        # =====================================================

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

        back.bind(
            on_press=self.go_back
        )

        self.root_box.add_widget(
            back
        )


    # =========================================================
    # CAMERA RESULT
    # =========================================================

    def on_activity_result(
        self,
        request_code,
        result_code,
        intent
    ):

        print(
            "========================================"
        )

        print(
            "ADD ITEM: CAMERA ACTIVITY RESULT"
        )

        print(
            "REQUEST:",
            request_code
        )

        print(
            "RESULT:",
            result_code
        )

        print(
            "========================================"
        )

        if request_code != self.camera_request_code:

            return

        try:

            self.camera.handle_result(
                request_code,
                result_code,
                intent
            )

        except Exception as e:

            print(
                "ADD ITEM: CAMERA RESULT ERROR:",
                repr(e)
            )
    # =========================================================
    # INPUT
    # =========================================================

    def create_input(
        self,
        hint,
        multiline,
        height
    ):

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
            padding=[
                dp(3),
                dp(3)
            ]
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

    def update_input_border(
        self,
        widget,
        *args
    ):

        if hasattr(
            widget,
            "border_line"
        ):

            widget.border_line.rounded_rectangle = (
                widget.x,
                widget.y,
                widget.width,
                widget.height,
                18
            )

    # =========================================================
    # CATEGORY
    # =========================================================

    def load_categories(self):

        app = App.get_running_app()

        values = []

        for cat in self.db.get_categories():

            values.append(
                app.tr(
                    cat[1].lower()
                )
            )

        self.category_spinner.values = values

    # =========================================================
    # EDIT MODE
    # =========================================================

    def load_edit_item(
        self,
        item_id
    ):

        self.edit_mode = True
        self.edit_id = item_id

        item = self.db.get_item(
            item_id
        )

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

        self.title.text = app.tr(
            "edit_item"
        )

        self.save_button.text = app.tr(
            "update_item"
        )

        self.name_input.text = name or ""

        self.location_input.text = (
            location or ""
        )

        self.description_input.text = (
            description or ""
        )

        self.image_path = (
            image_path or ""
        )

        if (
            self.image_path
            and os.path.exists(
                self.image_path
            )
        ):

            self.preview.source = (
                self.image_path
            )

            self.preview.reload()

        for cat in self.db.get_categories():

            if cat[0] == category_id:

                self.category_spinner.text = (
                    app.tr(
                        cat[1].lower()
                    )
                )

                break

    # =========================================================
    # CHOOSE IMAGE
    # =========================================================

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

        # -----------------------------------------------------
        # CAMERA
        # -----------------------------------------------------

        def camera_pressed(button):

            popup.dismiss()

            Clock.schedule_once(
                lambda dt: self.open_camera(),
                0.1
            )

        # -----------------------------------------------------
        # GALLERY
        # -----------------------------------------------------

        def gallery_pressed(button):

            popup.dismiss()

            Clock.schedule_once(
                lambda dt: self.open_gallery(),
                0.1
            )

        camera.bind(
            on_press=camera_pressed
        )

        gallery.bind(
            on_press=gallery_pressed
        )

        box.add_widget(
            camera
        )

        box.add_widget(
            gallery
        )

        popup.open()
    # =========================================================
    # GALLERY
    # =========================================================

    def open_gallery(self):

        from kivy.uix.popup import Popup
        from kivy.uix.button import Button
        from kivy.uix.filechooser import FileChooserIconView

        layout = BoxLayout(
            orientation="vertical"
        )

        chooser = FileChooserIconView(
            filters=[
                "*.png",
                "*.jpg",
                "*.jpeg",
                "*.webp"
            ]
        )

        select = Button(
            text="Select",
            size_hint_y=None,
            height=80
        )

        layout.add_widget(
            chooser
        )

        layout.add_widget(
            select
        )

        popup = Popup(
            title="Choose image",
            content=layout,
            size_hint=(0.95, 0.95)
        )

        def choose(instance):

            if not chooser.selection:
                print("NEMA IZABRANE SLIKE")
                return

            path = chooser.selection[0]

            print(
                "IZABRANA SLIKA:",
                path
            )

            if not os.path.exists(path):

                print(
                    "SLIKA NE POSTOJI:",
                    path
                )

                return

            try:

                # =============================================
                # ORIGINALNA SLIKA
                # =============================================

                self.preview.source = ""
                self.preview.source = path
                self.preview.reload()

                # =============================================
                # KOPIJA U APP STORAGE
                # =============================================

                self.image_path = (
                    self.image_manager.copy_file(
                        path
                    )
                )

                if not self.image_path:

                    print(
                        "SLIKA NIJE SACUVANA"
                    )

                    return

                print(
                    "ORIGINAL ZA PREVIEW:",
                    path
                )

                print(
                    "SACUVANA SLIKA:",
                    self.image_path
                )

                popup.dismiss()

            except Exception as e:

                print(
                    "IMAGE ERROR:",
                    repr(e)
                )

        select.bind(
            on_press=choose
        )

        popup.open()
        
        # =========================================================
    # OPEN CAMERA
    # =========================================================

    def open_camera(self):

        print(
            "ADD ITEM: OPEN CAMERA"
        )
        
        try:

            app = App.get_running_app()

            output_dir = os.path.join(
                app.user_data_dir,
                "images"
            )

            os.makedirs(
                output_dir,
                exist_ok=True
            )

            print(
                "ADD ITEM CAMERA DIRECTORY:",
                output_dir
            )
    
            result = self.camera.open(
                output_dir
            )

            print(
                "ADD ITEM CAMERA RESULT:",
                result
            )

        except Exception as e:

            print(
                "ADD ITEM OPEN CAMERA ERROR:",
                repr(e)
            )
            # =========================================================
        # CAMERA
        # =========================================================

    def on_camera_image(self, path):

        print("========================================")
        print("ADD ITEM: CAMERA IMAGE RECEIVED")
        print("PATH:", path)
        print("========================================")

        if not path:

            print(
                "CAMERA: PATH EMPTY"
            )

            return

        if not os.path.exists(path):

            print(
                "CAMERA: FILE DOES NOT EXIST:",
                path
            )

            return

        try:

            size = os.path.getsize(path)

        except Exception as e:

            print(
                "CAMERA: SIZE ERROR:",
                repr(e)
            )

            return

        if size <= 0:

            print(
                "CAMERA: FILE EMPTY"
            )

            return

        self.image_path = path

        print(
            "ADD ITEM: FINAL IMAGE:",
            self.image_path
        )

        Clock.schedule_once(
            lambda dt: self.set_camera_preview(path),
            0
        )
        
    def set_camera_preview(self, path):

        try:

            self.preview.source = ""
            self.preview.source = path
            self.preview.reload()

            print(
                "ADD ITEM: PREVIEW OK:",
                path
            )

        except Exception as e:

            print(
                "ADD ITEM: PREVIEW ERROR:",
                repr(e)
            )
    # =========================================================
    # SAVE / UPDATE
    # =========================================================
    def save_item(self, instance):

        app = App.get_running_app()

    # =====================================================
    # PODACI
    # =====================================================

        name = self.name_input.text.strip()

        if not name:
            print("Name required")
            return

        location = self.location_input.text.strip()

        description = self.description_input.text.strip()

    # =====================================================
    # CATEGORY
    # =====================================================

        category_id = None

        for cat in self.db.get_categories():
    
            translated_name = app.tr(
                cat[1].lower()
            )

            if translated_name == self.category_spinner.text:

                category_id = cat[0]
                break

    # =====================================================
    # SLIKA
    # =====================================================

        final_image_path = self.image_path or ""
    
        if final_image_path:

            if not os.path.exists(final_image_path):

                print(
                    "IMAGE PATH DOES NOT EXIST:",
                    final_image_path
                )
    
                final_image_path = ""

            elif os.path.getsize(final_image_path) <= 0:
    
                print(
                    "IMAGE FILE EMPTY:",
                    final_image_path
                )
    
                final_image_path = ""

    # =====================================================
    # EDIT
    # =====================================================

        if self.edit_mode:

            try:

                self.db.update_item(
                    self.edit_id,
                    name,
                    category_id,
                    location,
                    description,
                    final_image_path
                )

                self.db.add_history(
                    self.edit_id,
                    "Updated",
                    location
                )

            except Exception as e:

                print(
                    "UPDATE ITEM ERROR:",
                    repr(e)
                )

                return

    # =====================================================
    # NOVI ITEM
    # =====================================================

        else:
    
            try:

                item_id = self.db.add_item(
                    name,
                    category_id,
                    location,
                    description,
                    final_image_path
                )

                self.db.add_history(
                    item_id,
                    "Created",
                    location
                )

            except Exception as e:

                print(
                    "ADD ITEM ERROR:",
                    repr(e)
                )

                return

    # =====================================================
    # RESET
    # =====================================================

        self.clear_form()

    # =====================================================
    # HOME
    # =====================================================

        self.manager.current = "home"

        try:

            home = self.manager.get_screen(
                "home"
            )

            home.load_items()

        except Exception as e:

            print(
                "HOME REFRESH ERROR:",
                repr(e)
            )
    
    # =========================================================
        # RESET
        # =========================================================

    def clear_form(self):

        self.edit_mode = False
        self.edit_id = None

        app = App.get_running_app()

        self.title.text = app.tr(
            "add_item"
        )

        self.save_button.text = app.tr(
            "save_item"
        )

        self.name_input.text = ""
        self.location_input.text = ""
        self.description_input.text = ""

        self.category_spinner.text = (
            app.tr(
                "choose_category"
            )
        )

        self.image_path = ""

        self.preview.source = ""

    # =========================================================
    # NAVIGATION
    # =========================================================

    def go_back(
        self,
        instance
    ):

        self.manager.current = "home"

    # =========================================================
    # BACKGROUND
    # =========================================================

    def update_bg(
        self,
        *args
    ):

        self.bg.pos = self.pos
        self.bg.size = self.size

    # =========================================================
    # REFRESH THEME
    # =========================================================

    def refresh_theme(self):

        self.clear_widgets()

        self.__init__(
            name=self.name
        )