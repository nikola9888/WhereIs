import os
import time

from kivy.app import App
from jnius import autoclass


class Camera:

    def __init__(
        self,
        request_code=200,
        on_image=None
    ):

        self.request_code = request_code
        self.on_image = on_image

        self.output_uri = None
        self.output_path = None

    # =========================================================
    # OPEN CAMERA
    # =========================================================

    def open(self, output_dir=None):

        print("========================================")
        print("CAMERA: OPEN")
        print("========================================")

        try:

            Intent = autoclass(
                "android.content.Intent"
            )

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            activity = PythonActivity.mActivity

            # -------------------------------------------------
            # CAMERA INTENT
            # -------------------------------------------------

            intent = Intent(
                "android.media.action.IMAGE_CAPTURE"
            )

            package_manager = (
                activity.getPackageManager()
            )

            resolve_info = (
                intent.resolveActivity(
                    package_manager
                )
            )

            if resolve_info is None:

                print(
                    "CAMERA: NO CAMERA APPLICATION"
                )

                return False

            # -------------------------------------------------
            # APP STORAGE
            # -------------------------------------------------

            app = App.get_running_app()

            if app is None:

                print(
                    "CAMERA: APP IS NONE"
                )

                return False

            image_dir = os.path.join(
                app.user_data_dir,
                "images"
            )

            os.makedirs(
                image_dir,
                exist_ok=True
            )

            # -------------------------------------------------
            # FILE NAME
            # -------------------------------------------------

            filename = (
                "camera_"
                + str(
                    int(
                        time.time() * 1000
                    )
                )
                + ".jpg"
            )

            path = os.path.join(
                image_dir,
                filename
            )

            self.output_path = path

            print(
                "CAMERA: OUTPUT PATH:",
                path
            )

            # -------------------------------------------------
            # ANDROID CLASSES
            # -------------------------------------------------

            ContentValues = autoclass(
                "android.content.ContentValues"
            )

            MediaStoreImages = autoclass(
                "android.provider.MediaStore$Images$Media"
            )

            Build = autoclass(
                "android.os.Build"
            )

            VERSION_CODES = autoclass(
                "android.os.Build$VERSION_CODES"
            )

            # -------------------------------------------------
            # CONTENT VALUES
            # -------------------------------------------------

            values = ContentValues()

            values.put(
                "display_name",
                filename
            )

            values.put(
                "mime_type",
                "image/jpeg"
            )

            # Android 10+
            if Build.VERSION.SDK_INT >= VERSION_CODES.Q:

                values.put(
                    "relative_path",
                    "Pictures/WhereIs"
                )

                values.put(
                    "is_pending",
                    1
                )

            # -------------------------------------------------
            # INSERT MEDIASTORE
            # -------------------------------------------------

            resolver = (
                activity.getContentResolver()
            )

            uri = resolver.insert(
                MediaStoreImages.EXTERNAL_CONTENT_URI,
                values
            )

            if uri is None:

                print(
                    "CAMERA: MEDIASTORE INSERT FAILED"
                )

                self.output_uri = None
                self.output_path = None

                return False

            self.output_uri = uri

            print(
                "CAMERA: OUTPUT URI:",
                uri
            )

            # -------------------------------------------------
            # GIVE CAMERA URI
            # -------------------------------------------------

            intent.putExtra(
                "android.provider.MediaStore.EXTRA_OUTPUT",
                uri
            )

            intent.addFlags(
                Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                | Intent.FLAG_GRANT_READ_URI_PERMISSION
            )

            # -------------------------------------------------
            # START CAMERA
            # -------------------------------------------------

            print(
                "CAMERA: STARTING"
            )

            activity.startActivityForResult(
                intent,
                self.request_code
            )

            print(
                "CAMERA: STARTED"
            )

            return True

        except Exception as e:

            print("========================================")
            print(
                "CAMERA OPEN ERROR:",
                repr(e)
            )
            print("========================================")

            return False

    # =========================================================
    # HANDLE RESULT
    # =========================================================

    def handle_result(
        self,
        request_code,
        result_code,
        intent
    ):

        print("========================================")
        print("CAMERA: HANDLE RESULT")
        print("REQUEST:", request_code)
        print("RESULT:", result_code)
        print("URI:", self.output_uri)
        print("========================================")

        if request_code != self.request_code:

            return

        try:

            Activity = autoclass(
                "android.app.Activity"
            )

            # -------------------------------------------------
            # CANCELLED
            # -------------------------------------------------

            if result_code != Activity.RESULT_OK:

                print(
                    "CAMERA: USER CANCELLED"
                )

                self.delete_output()

                return

            if self.output_uri is None:

                print(
                    "CAMERA: OUTPUT URI NONE"
                )

                return

            # -------------------------------------------------
            # ANDROID ACTIVITY
            # -------------------------------------------------

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            activity = PythonActivity.mActivity

            resolver = (
                activity.getContentResolver()
            )

            # -------------------------------------------------
            # FINISH MEDIASTORE
            # -------------------------------------------------

            Build = autoclass(
                "android.os.Build"
            )

            VERSION_CODES = autoclass(
                "android.os.Build$VERSION_CODES"
            )

            if Build.VERSION.SDK_INT >= VERSION_CODES.Q:

                ContentValues = autoclass(
                    "android.content.ContentValues"
                )

                values = ContentValues()

                values.put(
                    "is_pending",
                    0
                )

                resolver.update(
                    self.output_uri,
                    values,
                    None,
                    None
                )

            # -------------------------------------------------
            # OPEN URI
            # -------------------------------------------------

            input_stream = resolver.openInputStream(
                self.output_uri
            )

            if input_stream is None:

                print(
                    "CAMERA: INPUT STREAM NONE"
                )

                return

            # -------------------------------------------------
            # CREATE LOCAL FILE
            # -------------------------------------------------

            app = App.get_running_app()

            image_dir = os.path.join(
                app.user_data_dir,
                "images"
            )

            os.makedirs(
                image_dir,
                exist_ok=True
            )

            filename = (
                "camera_local_"
                + str(
                    int(
                        time.time() * 1000
                    )
                )
                + ".jpg"
            )

            local_path = os.path.join(
                image_dir,
                filename
            )

            print(
                "CAMERA: COPYING TO:",
                local_path
            )

            # -------------------------------------------------
            # COPY STREAM
            # -------------------------------------------------

            FileOutputStream = autoclass(
                "java.io.FileOutputStream"
            )

            output_stream = FileOutputStream(
                local_path
            )

            try:

                buffer = bytearray(
                    64 * 1024
                )

                while True:

                    count = input_stream.read(
                        buffer
                    )

                    if count <= 0:

                        break

                    output_stream.write(
                        buffer,
                        0,
                        count
                    )

            finally:

                try:
                    input_stream.close()
                except Exception:
                    pass

                try:
                    output_stream.close()
                except Exception:
                    pass

            # -------------------------------------------------
            # VERIFY LOCAL FILE
            # -------------------------------------------------

            if not os.path.exists(
                local_path
            ):

                print(
                    "CAMERA: LOCAL FILE NOT CREATED"
                )

                return

            size = os.path.getsize(
                local_path
            )

            print(
                "CAMERA: LOCAL FILE SIZE:",
                size
            )

            if size <= 0:

                print(
                    "CAMERA: LOCAL FILE EMPTY"
                )

                try:
                    os.remove(local_path)
                except Exception:
                    pass

                return

            # -------------------------------------------------
            # FINAL PATH
            # -------------------------------------------------

            self.output_path = local_path

            print(
                "========================================"
            )

            print(
                "CAMERA: SUCCESS"
            )

            print(
                "CAMERA: FINAL LOCAL PATH:",
                local_path
            )

            print(
                "========================================"
            )

            # -------------------------------------------------
            # CALLBACK
            # -------------------------------------------------

            if self.on_image:

                self.on_image(
                    local_path
                )

        except Exception as e:

            print("========================================")
            print(
                "CAMERA HANDLE ERROR:",
                repr(e)
            )
            print("========================================")

    # =========================================================
    # DELETE OUTPUT
    # =========================================================

    def delete_output(self):

        try:

            if self.output_uri is None:

                return

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            activity = PythonActivity.mActivity

            resolver = (
                activity.getContentResolver()
            )

            resolver.delete(
                self.output_uri,
                None,
                None
            )

            print(
                "CAMERA: OUTPUT DELETED"
            )

        except Exception as e:

            print(
                "CAMERA DELETE ERROR:",
                repr(e)
            )

        finally:

            self.output_uri = None
            self.output_path = None