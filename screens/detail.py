import os
import theme
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line


from database import Database


from components.icons import (
    get_icon,
    EMPTY,
    DELETE,
    EDIT,
    BACK,
    LOCATION,
    HISTORY
)

class DetailScreen(Screen):


    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        self.db = Database()

        self.item_id = None



        # =========================
        # BACKGROUND
        # =========================


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



        # =========================
        # SCROLL
        # =========================


        self.scroll = ScrollView(
            do_scroll_x=False
        )


        self.root_box = BoxLayout(

            orientation="vertical",

            spacing=dp(15),

            padding=dp(18),

            size_hint_y=None

        )


        self.root_box.bind(

            minimum_height=
            self.root_box.setter(
                "height"
            )

        )


        self.scroll.add_widget(
            self.root_box
        )


        self.add_widget(
            self.scroll
        )



    # =========================
    # LOAD
    # =========================


    def load_item(self,item_id):


        self.item_id=item_id
        app = App.get_running_app()


        self.root_box.clear_widgets()



        item=self.db.get_item(item_id)



        if not item:
            return



        (
            item_id,
            name,
            category_id,
            location,
            description,
            image_path,
            created,
            updated

        )=item



        category="Other"



        for cat in self.db.get_categories():

            if cat[0]==category_id:

                category=cat[1]

                break




        self.add_title(
            name
        )



        # =========================
        # IMAGE
        # =========================


        if image_path and os.path.exists(image_path):


            image=Image(

                source=image_path,

                size_hint_y=None,

                height=dp(240),

                allow_stretch=True,

                keep_ratio=True

            )


            self.root_box.add_widget(
                image
            )


        else:


            empty=Image(

                source=get_icon(EMPTY),

                size_hint_y=None,

                height=dp(120)

            )


            self.root_box.add_widget(
                empty
            )



        # =========================
        # INFO CARD
        # =========================


        card=BoxLayout(

            orientation="vertical",

            spacing=dp(10),

            padding=dp(18),

            size_hint_y=None

        )


        card.bind(

            minimum_height=
            card.setter(
                "height"
            )

        )


        with card.canvas.before:

            Color(*theme.CARD)

            card.bg=RoundedRectangle(

                radius=[25],

                pos=card.pos,

                size=card.size

            )


        with card.canvas.after:

            Color(*theme.ITEM_BORDER)

            card.border=Line(

                rounded_rectangle=(

                    card.x,
                    card.y,
                    card.width,
                    card.height,
                    25

                ),

                width=1

            )


        card.bind(

            pos=lambda *x:
            self.update_card(card),

            size=lambda *x:
            self.update_card(card)

        )




        details = [

            f"{app.tr('category')}\n{category}",

            f"{app.tr('location')}\n{location or '-'}",

            f"{app.tr('description')}\n{description or '-'}",
            f"{app.tr('date_added')}\n{created or '-'}",
            f"{app.tr('updated')}\n{updated or '-'}"

        ]



        for data in details:


            label=Label(

                text=data,

                color=theme.TEXT,

                font_size=37,

                size_hint_y=None,

                height=dp(60),

                halign="left",

                valign="middle"

            )


            label.bind(

                size=label.setter(
                    "text_size"
                )

            )


            card.add_widget(label)




        self.root_box.add_widget(card)




        # =========================
        # HISTORY
        # =========================


        self.add_title(
            app.tr("history"),
            24
        )



        history=self.db.get_item_history(
            self.item_id
        )



        if history:


            for h in history:


                self.root_box.add_widget(

                    Label(

                        text=f"{h[0]} | {h[1]} | {h[2]}",

                        color=theme.TEXT_SECONDARY,

                        font_size=34,

                        size_hint_y=None,

                        height=dp(35)

                    )

                )

        else:


            self.root_box.add_widget(

                Label(

                    
                    text=app.tr("no_history"),

                    color=theme.TEXT_SECONDARY,

                    size_hint_y=None,

                    height=dp(35)

                )

            )



        # BUTTONS


        self.create_button(
            app.tr("edit_item"),
            theme.PRIMARY,
            self.edit_item
        )


        self.create_button(
            app.tr("delete_item"),
            theme.DANGER,
            self.delete_item
        )


        self.create_button(
            app.tr("back"),
            theme.CARD,
            self.go_back
        )




    # =========================
    # TITLE
    # =========================


    def add_title(self,text,size=52):


        label=Label(

            text=text,

            color=theme.PRIMARY,

            font_size=size,

            bold=True,

            size_hint_y=None,

            height=dp(55)

        )


        self.root_box.add_widget(label)




    # =========================
    # BUTTON
    # =========================


    def create_button(
        self,
        text,
        color,
        callback
    ):


        btn=Button(

            text=text,

            size_hint_y=None,

            height=dp(60),

            background_normal="",

            background_down="",

            background_color=color,

            color=theme.TEXT,

            font_size=38,

            bold=True

        )


        btn.bind(
            on_press=callback
        )


        self.root_box.add_widget(btn)




    # =========================
    # EDIT
    # =========================


    def edit_item(self,instance):


        screen=self.manager.get_screen(
            "add_item"
        )


        screen.load_edit_item(
            self.item_id
        )


        self.manager.current="add_item"




    # =========================
    # DELETE
    # =========================


    def delete_item(self,instance):
        
        app = App.get_running_app()

        box=BoxLayout(

            orientation="vertical",

            spacing=dp(10),

            padding=dp(15)

        )


        popup=Popup(

            title=app.tr("delete_question"),
            content=box,

            size_hint=(0.8,0.35)

        )


        yes=Button(
            text=app.tr("delete"),
            background_color=theme.DANGER
        )


        no=Button(
            text=app.tr("cancel")
        )


        yes.bind(

            on_press=lambda x:
            self.confirm_delete(popup)

        )


        no.bind(
            on_press=popup.dismiss
        )


        box.add_widget(yes)

        box.add_widget(no)


        popup.open()




    def confirm_delete(self,popup):


        self.db.delete_item(
            self.item_id
        )


        popup.dismiss()


        self.manager.current="home"




    # =========================
    # UPDATE
    # =========================


    def update_card(self,card):

        card.bg.pos=card.pos

        card.bg.size=card.size


        card.border.rounded_rectangle=(

            card.x,
            card.y,
            card.width,
            card.height,
            25

        )



    def update_bg(self,*args):

        self.bg.pos=self.pos

        self.bg.size=self.size




    def go_back(self,instance):

        self.manager.current="home"
        
        
    def refresh_theme(self):

        self.clear_widgets()

        self.__init__(
            name=self.name
        )