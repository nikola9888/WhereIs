import os


# =========================================================
# ICON FOLDER
# =========================================================

ICON_FOLDER = "assets/icons"



def get_icon(name):

    return os.path.join(
        ICON_FOLDER,
        name
    )



# =========================================================
# NAVIGATION
# =========================================================

HOME = "home.png"
SEARCH = "search.png"
SETTINGS = "settings.png"
BACK = "back.png"



# =========================================================
# ACTIONS
# =========================================================

ADD = "add.png"
EDIT = "edit.png"
DELETE = "delete.png"
SAVE = "save.png"

CAMERA = "camera.png"
IMAGE = "image.png"



# =========================================================
# ITEMS
# =========================================================

BOX = "box.png"
KEYS = "keys.png"
DOCUMENTS = "documents.png"
TOOLS = "tools.png"

ELECTRONICS = "electronics.png"
CLOTHES = "clothes.png"

WALLET = "wallet.png"

OTHER = "other.png"



# =========================================================
# LOCATION
# =========================================================

LOCATION = "location.png"
MAP = "map.png"



# =========================================================
# HISTORY
# =========================================================

HISTORY = "history.png"
TIME = "time.png"
UPDATE = "update.png"



# =========================================================
# STATES
# =========================================================

EMPTY = "empty.png"



# =========================================================
# CATEGORY ICON MAP
# =========================================================

CATEGORY_ICONS = {

    "Keys": KEYS,

    "Documents": DOCUMENTS,

    "Electronics": ELECTRONICS,

    "Clothes": CLOTHES,

    "Tools": TOOLS,

    "Wallet": WALLET,

    "Other": OTHER

}



def get_category_icon(category):

    return get_icon(
        CATEGORY_ICONS.get(
            category,
            OTHER
        )
    )