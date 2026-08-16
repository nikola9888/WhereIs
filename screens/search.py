import theme
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.app import App
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line


from components.search_bar import SearchBar
from components.item_card import ItemCard
from components.icons import (
    get_icon,
    SEARCH,
    EMPTY,
    BACK
)


from database import Database




class SearchScreen(Screen):


    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        
        app = App.get_running_app()

        self.db = Database()



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
        # ROOT
        # =========================


        root = BoxLayout(

            orientation="vertical",

            spacing=dp(16),

            padding=dp(18)

        )



        # =========================
        # TITLE
        # =========================


        title = Label(

            text=app.tr("search"),

            color=theme.PRIMARY,

            font_size=36,

            bold=True,

            size_hint_y=None,

            height=dp(60)

        )


        root.add_widget(title)



        # =========================
        # SEARCH BAR
        # =========================


        self.search_bar = SearchBar()


        self.search_bar.input.bind(
            text=self.search_items
        )


        root.add_widget(
            self.search_bar
        )



        # =========================
        # RESULTS
        # =========================


        self.scroll = ScrollView(
            do_scroll_x=False
        )


        self.list_container = BoxLayout(

            orientation="vertical",

            spacing=dp(14),

            size_hint_y=None

        )


        self.list_container.bind(

            minimum_height=
            self.list_container.setter(
                "height"
            )

        )


        self.scroll.add_widget(

            self.list_container

        )


        root.add_widget(

            self.scroll

        )



        self.show_items([])



        # =========================
        # BACK BUTTON
        # =========================


        back = Button(

            text=app.tr("back"),

            size_hint_y=None,

            height=dp(60),

            background_normal="",

            background_down="",

            background_color=theme.CARD,

            color=theme.TEXT,

            font_size=38

        )


        with back.canvas.after:

            Color(*theme.ITEM_BORDER)

            self.back_border = Line(

                rounded_rectangle=(

                    back.x,
                    back.y,
                    back.width,
                    back.height,
                    22

                ),

                width=1

            )


        back.bind(

            pos=self.update_back_border,

            size=self.update_back_border

        )


        back.bind(
            on_press=self.go_home
        )


        root.add_widget(back)



        self.add_widget(root)




    # =========================
    # SEARCH
    # =========================


    def search_items(
        self,
        instance,
        text
    ):


        text=text.strip()


        if text:

            rows=self.db.search_items(text)

        else:

            rows=[]



        self.show_items(rows)




    # =========================
    # SHOW RESULTS
    # =========================


    def show_items(self,rows):

        app = App.get_running_app()
        
        self.list_container.clear_widgets()
        

        if not rows:


            empty_box=BoxLayout(

                orientation="vertical",

                spacing=dp(10),

                size_hint_y=None,

                height=dp(180)

            )


            empty_icon=Image(

                source=get_icon(EMPTY),

                size_hint_y=None,

                height=dp(70)

            )


            empty_text=Label(

                text=app.tr("no_results"),

                color=theme.TEXT_SECONDARY,

                font_size=42,

                bold=True

            )


            empty_box.add_widget(
                empty_icon
            )


            empty_box.add_widget(
                empty_text
            )


            self.list_container.add_widget(
                empty_box
            )


            return




        for item in rows:


            (
                item_id,
                name,
                category,
                icon,
                location,
                description,
                image_path

            ) = item



            card=ItemCard(

                item_id=item_id,

                name=name,

                category=category or "Other",

                icon=icon or "other",

                location=location or "Unknown",

                description=description or "",

                image_path=image_path or ""

            )


            self.list_container.add_widget(
                card
            )





    # =========================
    # UPDATE
    # =========================


    def update_bg(self,*args):

        self.bg.pos=self.pos

        self.bg.size=self.size




    def update_back_border(self,*args):

        self.back_border.rounded_rectangle=(

            self.children[-1].x,
            self.children[-1].y,
            self.children[-1].width,
            self.children[-1].height,
            22

        )




    # =========================
    # NAVIGATION
    # =========================


    def go_home(self,instance):

        self.manager.current="home"
        
    def refresh_theme(self):

        self.clear_widgets()

        self.__init__(
            name=self.name
        )