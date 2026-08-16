import json
import os


class ThemeManager:

    THEMES = [

        "dark_orange",

        "ocean",

        "coffee",

        "light"

    ]


    def __init__(self, app):

        self.app = app

        self.file = os.path.join(

            app.user_data_dir,

            "settings.json"

        )

        self.theme = "dark_orange"

        self.load()


    def load(self):

        try:

            with open(self.file, "r") as f:

                data = json.load(f)

                self.theme = data.get(

                    "theme",

                    "dark_orange"

                )

        except:

            self.theme = "dark_orange"


        if self.theme not in self.THEMES:

            self.theme = "dark_orange"


    def save(self):

        with open(self.file, "w") as f:

            json.dump(

                {

                    "theme": self.theme

                },

                f,

                indent=4

            )


    def next_theme(self):

        index = self.THEMES.index(

            self.theme

        )

        index += 1

        if index >= len(self.THEMES):

            index = 0

        self.theme = self.THEMES[index]

        self.save()

        return self.theme


    def set_theme(self, theme):

        if theme in self.THEMES:

            self.theme = theme

            self.save()


    def get_theme(self):

        return self.theme