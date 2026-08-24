import os

ICON_FOLDER = os.path.join(
    "assets",
    "Icon.png"
)


def get_icon(name):
    return os.path.join(
        ICON_FOLDER,
        name
    )


HOME = "home.png"
SEARCH = "search.png"
SETTINGS = "settings.png"
BACK = "back.png"

ADD = "add.png"
EDIT = "edit.png"
DELETE = "delete.png"
SAVE = "save.png"

CAMERA = "camera.png"
IMAGE = "image.png"

BOX = "box.png"
KEYS = "keys.png"
DOCUMENTS = "documents.png"
TOOLS = "tools.png"
ELECTRONICS = "electronic.png"
CLOTHES = "clothes.png"
WALLET = "wallet.png"
OTHER = "other.png"

LOCATION = "location.png"
MAP = "map.png"
HISTORY = "history.png"
TIME = "time.png"
UPDATE = "update.png"
EMPTY = "empty.png"

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
