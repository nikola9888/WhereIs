from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.storage.jsonstore import JsonStore

from theme_manager import ThemeManager
from translations import translations
from translation_completion import apply_translation_completion

apply_translation_completion(translations)

from screens.home import HomeScreen
from screens.detail import DetailScreen
from screens.add_item import AddItemScreen
from screens.settings import SettingsScreen
from screens.search import SearchScreen
from screens.profile import ProfileScreen
from screens.receive import ReceiveScreen


class WhereIsApp(App):

    CAMERA_REQUEST_CODE = 200

    def build(self):

        try:
            from android import activity

            activity.bind(
                on_activity_result=self.on_activity_result
            )

            print("MAIN: ANDROID ACTIVITY RESULT BIND OK")

        except Exception as e:
            print(
                "MAIN: ANDROID ACTIVITY RESULT BIND SKIPPED:",
                repr(e)
            )

        self.theme_manager = ThemeManager(self)

        self.store = JsonStore("settings.json")

        if self.store.exists("app"):
            self.language = self.store.get("app").get(
                "language",
                "en"
            )
        else:
            self.language = "en"

        self.root = self.create_screen_manager()

        return self.root

    def on_activity_result(
        self,
        request_code,
        result_code,
        intent
    ):

        print("========================================")
        print("MAIN: ACTIVITY RESULT")
        print("REQUEST:", request_code)
        print("RESULT:", result_code)
        print("INTENT:", intent)
        print("========================================")

        try:
            if not self.root:
                return

            if request_code == SettingsScreen.RESTORE_REQUEST_CODE:
                screen = self.root.get_screen("settings")
                screen.on_restore_result(
                    request_code,
                    result_code,
                    intent
                )
                return

            screen = self.root.get_screen("add_item")

            screen.on_activity_result(
                request_code,
                result_code,
                intent
            )

        except Exception as e:
            print(
                "MAIN CAMERA RESULT ERROR:",
                repr(e)
            )

    def create_screen_manager(self):

        sm = ScreenManager(
            transition=FadeTransition(duration=0.25)
        )

        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(SearchScreen(name="search"))
        sm.add_widget(DetailScreen(name="detail"))
        sm.add_widget(AddItemScreen(name="add_item"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(ReceiveScreen(name="receive"))

        sm.current = "home"

        return sm

    def tr(self, key):

        return translations.get(
            self.language,
            translations["en"]
        ).get(
            key,
            key
        )

    def change_theme(self):

        self.theme_manager.next_theme()

        import theme
        import importlib

        importlib.reload(theme)

        if not self.root:
            return

        for screen in self.root.screens:
            if hasattr(screen, "refresh_theme"):
                try:
                    screen.refresh_theme()
                except Exception as e:
                    print(
                        "THEME REFRESH ERROR:",
                        repr(e)
                    )


if __name__ == "__main__":
    WhereIsApp().run()
