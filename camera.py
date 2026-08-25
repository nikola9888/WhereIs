import os
import time

from kivy.app import App
from jnius import autoclass


class Camera:

    def __init__(self, request_code=200, on_image=None):
        self.request_code = request_code
        self.on_image = on_image
        self.output_path = None

    def open(self, output_dir=None):
        print("CAMERA: OPEN")

        try:
            from android.permissions import check_permission, Permission

            if not check_permission(Permission.CAMERA):
                print("CAMERA: PERMISSION NOT GRANTED YET")
                return False

            Intent = autoclass("android.content.Intent")
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            activity = PythonActivity.mActivity

            # Use the standard camera intent without EXTRA_OUTPUT for the
            # initial capture. This avoids MediaStore/URI permission problems
            # that can prevent some Android camera apps from opening at all.
            intent = Intent(Intent.ACTION_IMAGE_CAPTURE)
            intent.putExtra("return-data", True)

            package_manager = activity.getPackageManager()
            resolve_info = intent.resolveActivity(package_manager)

            if resolve_info is None:
                print("CAMERA: NO CAMERA APPLICATION")
                return False

            app = App.get_running_app()
            if app is None:
                print("CAMERA: APP IS NONE")
                return False

            image_dir = output_dir or os.path.join(
                app.user_data_dir,
                "images"
            )
            os.makedirs(image_dir, exist_ok=True)

            self.output_path = os.path.join(
                image_dir,
                "camera_" + str(int(time.time() * 1000)) + ".jpg"
            )

            print("CAMERA: STARTING NATIVE CAMERA")
            activity.startActivityForResult(
                intent,
                self.request_code
            )
            print("CAMERA: STARTED")
            return True

        except Exception as e:
            print("CAMERA OPEN ERROR:", repr(e))
            self.output_path = None
            return False

    def handle_result(self, request_code, result_code, intent):
        print("CAMERA: HANDLE RESULT", request_code, result_code)

        if request_code != self.request_code:
            return

        try:
            Activity = autoclass("android.app.Activity")

            if result_code != Activity.RESULT_OK:
                print("CAMERA: USER CANCELLED")
                self.output_path = None
                return

            if intent is None:
                print("CAMERA: RESULT INTENT NONE")
                return

            extras = intent.getExtras()
            if extras is None:
                print("CAMERA: RESULT EXTRAS NONE")
                return

            bitmap = extras.get("data")
            if bitmap is None:
                print("CAMERA: RESULT BITMAP NONE")
                return

            app = App.get_running_app()
            if app is None:
                return

            image_dir = os.path.join(app.user_data_dir, "images")
            os.makedirs(image_dir, exist_ok=True)

            local_path = os.path.join(
                image_dir,
                "camera_local_" + str(int(time.time() * 1000)) + ".jpg"
            )

            FileOutputStream = autoclass("java.io.FileOutputStream")
            CompressFormat = autoclass("android.graphics.Bitmap$CompressFormat")

            output_stream = FileOutputStream(local_path)

            try:
                success = bitmap.compress(
                    CompressFormat.JPEG,
                    95,
                    output_stream
                )
            finally:
                try:
                    output_stream.close()
                except Exception:
                    pass

            if not success:
                print("CAMERA: BITMAP COMPRESS FAILED")
                try:
                    os.remove(local_path)
                except Exception:
                    pass
                return

            if not os.path.isfile(local_path):
                print("CAMERA: LOCAL FILE NOT CREATED")
                return

            size = os.path.getsize(local_path)
            print("CAMERA: LOCAL FILE SIZE:", size)

            if size <= 0:
                print("CAMERA: LOCAL FILE EMPTY")
                try:
                    os.remove(local_path)
                except Exception:
                    pass
                return

            self.output_path = local_path
            print("CAMERA: SUCCESS:", local_path)

            if self.on_image:
                self.on_image(local_path)

        except Exception as e:
            print("CAMERA HANDLE ERROR:", repr(e))

    def delete_output(self):
        if self.output_path:
            try:
                if os.path.isfile(self.output_path):
                    os.remove(self.output_path)
                    print("CAMERA: LOCAL OUTPUT DELETED")
            except Exception as e:
                print("CAMERA DELETE ERROR:", repr(e))

        self.output_path = None
