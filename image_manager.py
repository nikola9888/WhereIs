import os
import uuid
import shutil

from PIL import Image as PILImage
from PIL import ImageOps


class ImageManager:

    def __init__(self):

        # =====================================================
        # PRIVATNI STORAGE APLIKACIJE
        # =====================================================

        try:

            from kivy.app import App

            app = App.get_running_app()

            self.images_dir = os.path.join(
                app.user_data_dir,
                "images"
            )

        except Exception:

            self.images_dir = os.path.join(
                os.getcwd(),
                "images"
            )

        os.makedirs(
            self.images_dir,
            exist_ok=True
        )

    # =========================================================
    # COPY ORIGINAL FILE
    # =========================================================

    def copy_file(self, source_path):

        if not source_path:
            return ""

        if not os.path.exists(source_path):

            print(
                "COPY ERROR: FILE NE POSTOJI:",
                source_path
            )

            return ""

        extension = (
            os.path.splitext(source_path)[1]
            .lower()
        )

        if extension not in (
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        ):

            extension = ".jpg"

        filename = (
            str(uuid.uuid4())
            + extension
        )

        destination = os.path.join(
            self.images_dir,
            filename
        )

        try:

            shutil.copy2(
                source_path,
                destination
            )

            print(
                "IMAGE COPIED:",
                destination
            )

            return destination

        except Exception as e:

            print(
                "COPY ERROR:",
                repr(e)
            )

            return ""

    # =========================================================
    # RESIZE WITHOUT CROP
    # =========================================================

    def resize_image(
        self,
        image_path,
        max_width=1000,
        max_height=1000,
        quality=90
    ):

        if not image_path:
            return ""

        if not os.path.exists(image_path):

            print(
                "RESIZE ERROR: FILE NE POSTOJI:",
                image_path
            )

            return ""

        try:

            image = PILImage.open(
                image_path
            )

            print(
                "ORIGINAL SIZE:",
                image.width,
                "x",
                image.height
            )

            # =================================================
            # ISPRAVLJANJE ROTACIJE
            # =================================================

            image = ImageOps.exif_transpose(
                image
            )

            # =================================================
            # PROPORCIONALNO SMANJIVANJE
            # BEZ CROP-A
            # =================================================

            image.thumbnail(
                (
                    max_width,
                    max_height
                ),
                PILImage.Resampling.LANCZOS
            )

            print(
                "FINAL SIZE:",
                image.width,
                "x",
                image.height
            )

            # =================================================
            # RGB
            # =================================================

            if image.mode != "RGB":

                if image.mode in (
                    "RGBA",
                    "LA"
                ):

                    background = PILImage.new(
                        "RGB",
                        image.size,
                        "white"
                    )

                    alpha = image.getchannel(
                        "A"
                    )

                    background.paste(
                        image,
                        mask=alpha
                    )

                    image = background

                else:

                    image = image.convert(
                        "RGB"
                    )

            # =================================================
            # OUTPUT
            # =================================================

            output_path = os.path.join(
                self.images_dir,
                "resized_"
                + str(uuid.uuid4())
                + ".jpg"
            )

            image.save(
                output_path,
                "JPEG",
                quality=quality,
                optimize=True
            )

            image.close()

            if not os.path.exists(
                output_path
            ):

                print(
                    "RESIZE ERROR: FAJL NIJE NAPRAVLJEN"
                )

                return ""

            print(
                "IMAGE SAVED:",
                output_path
            )

            return output_path

        except Exception as e:

            print(
                "RESIZE ERROR:",
                repr(e)
            )

            return ""

    # =========================================================
    # COPY + RESIZE
    # =========================================================

    def copy_and_resize(
        self,
        source_path,
        max_size=1000,
        quality=90
    ):

        if not source_path:

            print(
                "COPY + RESIZE ERROR: PRAZAN PATH"
            )

            return ""

        if not os.path.exists(
            source_path
        ):

            print(
                "COPY + RESIZE ERROR: FILE NE POSTOJI:",
                source_path
            )

            return ""

        try:

            image = PILImage.open(
                source_path
            )

            print(
                "ORIGINAL SIZE:",
                image.width,
                "x",
                image.height
            )

            # =================================================
            # ISPRAVI ROTACIJU
            # =================================================

            image = ImageOps.exif_transpose(
                image
            )

            # =================================================
            # PROPORCIONALNO SMANJIVANJE
            # NIKAKAV CROP
            # =================================================

            image.thumbnail(
                (
                    max_size,
                    max_size
                ),
                PILImage.Resampling.LANCZOS
            )

            print(
                "FINAL SIZE:",
                image.width,
                "x",
                image.height
            )

            # =================================================
            # RGB
            # =================================================

            if image.mode != "RGB":

                if image.mode in (
                    "RGBA",
                    "LA"
                ):

                    background = PILImage.new(
                        "RGB",
                        image.size,
                        "white"
                    )

                    alpha = image.getchannel(
                        "A"
                    )

                    background.paste(
                        image,
                        mask=alpha
                    )

                    image = background

                else:

                    image = image.convert(
                        "RGB"
                    )

            # =================================================
            # SACUVAVANJE
            # =================================================

            output_path = os.path.join(
                self.images_dir,
                str(uuid.uuid4())
                + ".jpg"
            )

            image.save(
                output_path,
                "JPEG",
                quality=quality,
                optimize=True
            )

            image.close()

            # =================================================
            # PROVERA
            # =================================================

            if not os.path.exists(
                output_path
            ):

                print(
                    "COPY + RESIZE ERROR: "
                    "FAJL NIJE NAPRAVLJEN"
                )

                return ""

            print(
                "IMAGE SAVED:",
                output_path
            )

            return output_path

        except Exception as e:

            print(
                "COPY + RESIZE ERROR:",
                repr(e)
            )

            return ""

    # =========================================================
    # DELETE IMAGE
    # =========================================================

    def delete_image(
        self,
        image_path
    ):

        if not image_path:
            return False

        try:

            if os.path.exists(
                image_path
            ):

                os.remove(
                    image_path
                )

                print(
                    "IMAGE DELETED:",
                    image_path
                )

                return True

        except Exception as e:

            print(
                "DELETE IMAGE ERROR:",
                repr(e)
            )

        return False