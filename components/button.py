from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class ModernButton(Button):

    def __init__(
        self,
        text="",
        icon=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_color = (0,0,0,0)

        layout = BoxLayout(
            orientation="horizontal",
            spacing=10,
            padding=10
        )

        if icon:

            img = Image(
                source=icon,
                size_hint_x=None,
                width=40
            )

            layout.add_widget(img)


        label = Label(
            text=text,
            color=(1,1,1,1),
            halign="left",
            valign="middle"
        )

        label.bind(
            size=label.setter("text_size")
        )

        layout.add_widget(label)


        self.add_widget(layout)