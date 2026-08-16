import importlib

from kivy.app import App



# =========================================================
# LOAD ACTIVE THEME
# =========================================================


def get_theme():


    app = App.get_running_app()


    if app and hasattr(app, "theme_manager"):


        return app.theme_manager.theme



    return "dark_orange"





def load_theme():


    theme_name = get_theme()



    try:


        return importlib.import_module(

            f"themes.{theme_name}"

        )


    except Exception as e:


        print(

            "Theme loading error:",

            e

        )


        return importlib.import_module(

            "themes.dark_orange"

        )





current = load_theme()





# =========================================================
# BACKGROUND
# =========================================================


BACKGROUND = current.BACKGROUND

BACKGROUND_DARK = current.BACKGROUND_DARK





# =========================================================
# CARDS
# =========================================================


CARD = current.CARD

CARD_LIGHT = current.CARD_LIGHT

SURFACE = current.SURFACE

SURFACE_2 = current.SURFACE_2





# =========================================================
# PRIMARY COLORS
# =========================================================


PRIMARY = current.PRIMARY

PRIMARY_DARK = current.PRIMARY_DARK





# =========================================================
# TEXT
# =========================================================


WHITE = current.WHITE

TEXT = current.TEXT

TEXT_SECONDARY = current.TEXT_SECONDARY

TEXT_MUTED = current.TEXT_MUTED





# =========================================================
# EXTRA COLORS
# =========================================================


CYAN = current.CYAN

AQUA = current.AQUA


SUCCESS = current.SUCCESS

WARNING = current.WARNING

DANGER = current.DANGER





# =========================================================
# TRANSPARENCY
# =========================================================


GLASS = current.GLASS

ORANGE_GLASS = current.ORANGE_GLASS

SHADOW = current.SHADOW





# =========================================================
# CATEGORY
# =========================================================


CATEGORY = current.CATEGORY





# =========================================================
# ITEM CARD
# =========================================================


ITEM_BORDER = current.ITEM_BORDER

ITEM_GLOW = current.ITEM_GLOW





# =========================================================
# BORDERS
# =========================================================


BORDER_COLOR = getattr(

    current,

    "BORDER_COLOR",

    (1,1,1,0.25)

)



INPUT_BORDER = getattr(

    current,

    "INPUT_BORDER",

    (1,1,1,0.35)

)



CARD_BORDER = getattr(

    current,

    "CARD_BORDER",

    (1,1,1,0.30)

)



ICON_SIZE = getattr(

    current,

    "ICON_SIZE",

    32

)





# =========================================================
# ORANGE
# =========================================================


ORANGE_LIGHT = getattr(

    current,

    "ORANGE_LIGHT",

    PRIMARY

)



ORANGE_GLOW = getattr(

    current,

    "ORANGE_GLOW",

    PRIMARY

)





# =========================================================
# UI
# =========================================================


RADIUS_SMALL = current.RADIUS_SMALL

RADIUS = current.RADIUS

RADIUS_LARGE = current.RADIUS_LARGE



PADDING = current.PADDING

PADDING_LARGE = current.PADDING_LARGE



SPACING = current.SPACING

SPACING_SMALL = current.SPACING_SMALL





# =========================================================
# TYPOGRAPHY
# =========================================================


TITLE = current.TITLE

SUBTITLE = current.SUBTITLE

BODY = current.BODY

SMALL = current.SMALL

TINY = current.TINY





# =========================================================
# RELOAD THEME
# =========================================================


def reload_theme():


    global current


    global BACKGROUND

    global BACKGROUND_DARK

    global CARD

    global PRIMARY

    global TEXT

    global TEXT_SECONDARY

    global ITEM_BORDER



    current = load_theme()



    BACKGROUND = current.BACKGROUND

    BACKGROUND_DARK = current.BACKGROUND_DARK

    CARD = current.CARD

    PRIMARY = current.PRIMARY

    TEXT = current.TEXT

    TEXT_SECONDARY = current.TEXT_SECONDARY

    ITEM_BORDER = current.ITEM_BORDER





# =========================================================
# HELPERS
# =========================================================


def darken(color, factor=0.8):


    r,g,b,a = color


    return (

        r * factor,

        g * factor,

        b * factor,

        a

    )