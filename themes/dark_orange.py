from kivy.utils import get_color_from_hex


# =========================================================
# WHEREIS PREMIUM DARK ORANGE THEME
# =========================================================


# =========================
# BACKGROUND
# =========================

BACKGROUND = get_color_from_hex("#151515")
BACKGROUND_DARK = get_color_from_hex("#0D0D0D")



# =========================
# CARDS
# =========================

CARD = get_color_from_hex("#242424")
CARD_LIGHT = get_color_from_hex("#303030")

SURFACE = get_color_from_hex("#3A3A3A")
SURFACE_2 = get_color_from_hex("#484848")


# =========================
# PRIMARY
# =========================

PRIMARY = get_color_from_hex("#FF9800")

PRIMARY_DARK = get_color_from_hex("#F57C00")

ORANGE_LIGHT = get_color_from_hex("#FFB74D")

ORANGE_GLOW = get_color_from_hex("#FFE0B2")

# =========================
# BORDERS
# =========================

BORDER_COLOR = get_color_from_hex("#FFFFFF40")

INPUT_BORDER = get_color_from_hex("#FFFFFF80")

CARD_BORDER = get_color_from_hex("#FF980080")

ITEM_BORDER = get_color_from_hex("#FFFFFF90")

ITEM_GLOW = get_color_from_hex("#FF980050")

ICON_SIZE = 32
# =========================
# SECONDARY
# =========================

CYAN = get_color_from_hex("#06B6D4")

AQUA = get_color_from_hex("#22D3EE")



# =========================
# STATUS
# =========================

SUCCESS = get_color_from_hex("#22C55E")

WARNING = get_color_from_hex("#FFB300")

DANGER = get_color_from_hex("#EF4444")



# =========================
# TEXT
# =========================

WHITE = get_color_from_hex("#FFFFFF")

TEXT = get_color_from_hex("#FFFFFF")

TEXT_SECONDARY = get_color_from_hex("#D0D0D0")

TEXT_MUTED = get_color_from_hex("#888888")



# =========================
# TRANSPARENCY
# =========================

GLASS = get_color_from_hex("#FFFFFF22")

ORANGE_GLASS = get_color_from_hex("#FF980040")

SHADOW = get_color_from_hex("#00000099")



# =========================
# CATEGORY COLORS
# =========================

CATEGORY = {

    "keys": get_color_from_hex("#FF980055"),

    "documents": get_color_from_hex("#3B82F655"),

    "tools": get_color_from_hex("#FFB30055"),

    "electronics": get_color_from_hex("#06B6D455"),

    "clothes": get_color_from_hex("#A855F755"),

    "other": get_color_from_hex("#77777755"),

}



# =========================
# UI SETTINGS
# =========================

RADIUS_SMALL = 10

RADIUS = 24

RADIUS_LARGE = 32



PADDING = 16

PADDING_LARGE = 24



SPACING = 12

SPACING_SMALL = 20



# =========================
# TYPOGRAPHY
# =========================

TITLE = 50

SUBTITLE = 24

BODY = 18

SMALL = 15

TINY = 12



def darken(color, factor=0.8):

    r, g, b, a = color

    return (
        r * factor,
        g * factor,
        b * factor,
        a
    )