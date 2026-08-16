from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.storage.jsonstore import JsonStore

from theme_manager import ThemeManager
from translations import translations

from screens.home import HomeScreen
from screens.detail import DetailScreen
from screens.add_item import AddItemScreen
from screens.settings import SettingsScreen
from screens.search import SearchScreen


class WhereIsApp(App):

    # =========================================================
    # CONSTANTS
    # =========================================================

    CAMERA_REQUEST_CODE = 200

    # =========================================================
    # BUILD
    # =========================================================

    def build(self):

        # -----------------------------------------------------
        # ANDROID ACTIVITY RESULT
        # -----------------------------------------------------

        try:

            from android import activity

            activity.bind(
                on_activity_result=self.on_activity_result
            )

            print(
                "MAIN: ANDROID ACTIVITY RESULT BIND OK"
            )

        except Exception as e:

            print(
                "MAIN: ANDROID ACTIVITY RESULT BIND SKIPPED:",
                repr(e)
            )

        # =====================================================
        # THEME
        # =====================================================

        self.theme_manager = ThemeManager(self)

        # =====================================================
        # SETTINGS
        # =====================================================

        self.store = JsonStore(
            "settings.json"
        )

        if self.store.exists("app"):

            self.language = self.store.get(
                "app"
            ).get(
                "language",
                "en"
            )

        else:

            self.language = "en"

        # =====================================================
        # SCREEN MANAGER
        # =====================================================

        self.root = self.create_screen_manager()

        return self.root

    # =========================================================
    # ANDROID ACTIVITY RESULT
    # =========================================================

    def on_activity_result(
        self,
        request_code,
        result_code,
        intent
    ):

        print("========================================")
        print("MAIN: ACTIVITY RESULT")
        print(
            "REQUEST:",
            request_code
        )
        print(
            "RESULT:",
            result_code
        )
        print(
            "INTENT:",
            intent
        )
        print("========================================")

        try:

            if not self.root:
                return

            screen = self.root.get_screen(
                "add_item"
            )

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

    # =========================================================
    # SCREEN MANAGER
    # =========================================================

    def create_screen_manager(self):

        sm = ScreenManager(
            transition=FadeTransition(
                duration=0.25
            )
        )

        # =====================================================
        # HOME
        # =====================================================

        sm.add_widget(
            HomeScreen(
                name="home"
            )
        )

        # =====================================================
        # SEARCH
        # =====================================================

        sm.add_widget(
            SearchScreen(
                name="search"
            )
        )

        # =====================================================
        # DETAIL
        # =====================================================

        sm.add_widget(
            DetailScreen(
                name="detail"
            )
        )

        # =====================================================
        # ADD ITEM
        # =====================================================

        sm.add_widget(
            AddItemScreen(
                name="add_item"
            )
        )

        # =====================================================
        # SETTINGS
        # =====================================================

        sm.add_widget(
            SettingsScreen(
                name="settings"
            )
        )

        # =====================================================
        # START SCREEN
        # =====================================================

        sm.current = "home"

        return sm

    # =========================================================
    # TRANSLATIONS
    # =========================================================

    def tr(self, key):

        return translations.get(
            self.language,
            translations["en"]
        ).get(
            key,
            key
        )

    # =========================================================
    # THEME
    # =========================================================

    def change_theme(self):

        self.theme_manager.next_theme()

        import theme
        import importlib

        importlib.reload(
            theme
        )

        if not self.root:
            return

        for screen in self.root.screens:

            if hasattr(
                screen,
                "refresh_theme"
            ):

                try:

                    screen.refresh_theme()

                except Exception as e:

                    print(
                        "THEME REFRESH ERROR:",
                        repr(e)
                    )


# =============================================================
# RUN APP
# =============================================================

if __name__ == "__main__":

    WhereIsApp().run()
