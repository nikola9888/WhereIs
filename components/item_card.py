import theme
import os
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line





class ItemCard(ButtonBehavior, BoxLayout):


    def __init__(
        self,
        item_id,
        name,
        category,
        icon,
        location,
        description="",
        image_path="",
        **kwargs
    ):


        super().__init__(**kwargs)



        self.item_id = item_id

        self.name = name

        self.category = category

        self.icon = icon or "other"

        self.location = location

        self.description = description

        self.image_path = image_path
        
        print("CARD IMAGE PATH:", image_path)
        
        print("POSTOJI:", os.path.exists(image_path))



        self.orientation = "vertical"

        self.size_hint_y = None

        self.height = dp(190)

        self.padding = dp(16)

        self.spacing = dp(10)



        # =========================
        # CARD
        # =========================


        with self.canvas.before:


            Color(*theme.CARD)


            self.bg = RoundedRectangle(

                pos=self.pos,

                size=self.size,

                radius=[26]

            )


        with self.canvas.after:


            Color(*theme.ITEM_BORDER)


            self.border = Line(

                rounded_rectangle=(

                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    26

                ),

                width=1.3

            )


        self.bind(

            pos=self.update_bg,

            size=self.update_bg

        )



        # =========================
        # MAIN ROW
        # =========================


        row = BoxLayout(

            orientation="horizontal",

            spacing=dp(15)

        )



        # =========================
        # IMAGE / ICON
        # =========================


        if image_path and os.path.exists(image_path):


            img = Image(
                source=image_path,
                size_hint_x=None,
                size_hint_y=None,
                width=dp(150),
                height=dp(150),
                fit_mode="contain"
            )


            row.add_widget(img)



        else:


            self.add_icon(row)



        # =========================
        # INFO
        # =========================


        info = BoxLayout(

            orientation="vertical",

            spacing=dp(4)

        )



        title = Label(

            text=name,

            color=theme.PRIMARY,

            font_size=47,

            bold=True,

            halign="left",

            valign="middle"

        )


        title.bind(

            size=title.setter(
                "text_size"
            )

        )


        info.add_widget(title)



        location = Label(

            text=App.get_running_app().tr(
                "unknown_location"
            ) if not self.location else self.location,

            color=theme.TEXT,

            font_size=38,

            halign="left",

            valign="middle"

        )


        location.bind(

            size=location.setter(
                "text_size"
            )

        )


        info.add_widget(location)



        category_label = Label(

            text=App.get_running_app().tr(
            self.category.lower()
            ),
            color=theme.TEXT_SECONDARY,
 
            font_size=36,

            halign="left",

            valign="middle"

        )


        category_label.bind(

            size=category_label.setter(
                "text_size"
            )

        )


        info.add_widget(category_label)



        row.add_widget(info)



        self.add_widget(row)



        # =========================
        # DESCRIPTION
        # =========================


        if description:


            desc = Label(

                text=description,

                color=theme.TEXT_SECONDARY,

                font_size=35,

                size_hint_y=None,

                height=dp(35),

                halign="left",

                valign="middle"

            )


            desc.bind(

                size=desc.setter(
                    "text_size"
                )

            )


            self.add_widget(desc)




    # =========================
    # ICON
    # =========================


    def add_icon(self,row):


        path = f"icons/{self.icon}.png"


        if not os.path.exists(path):

            path = "icons/other.png"



        icon = Image(

            source=path,

            size_hint_x=None,

            width=dp(75),

            allow_stretch=True,

            keep_ratio=True

        )


        row.add_widget(icon)




    # =========================
    # OPEN DETAIL
    # =========================


    def on_press(self):


        app = App.get_running_app()


        if not app:

            return



        detail = app.root.get_screen(
            "detail"
        )


        detail.load_item(

            self.item_id

        )


        app.root.current = "detail"




    # =========================
    # UPDATE
    # =========================


    def update_bg(self,*args):


        self.bg.pos = self.pos

        self.bg.size = self.size


        self.border.rounded_rectangle = (

            self.x,
            self.y,
            self.width,
            self.height,
            26

        )