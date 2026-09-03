import os
import time

from kivy.app import App
from kivy.clock import Clock
from jnius import autoclass


class Camera:

    def __init__(self, request_code=200, on_image=None):
        self.request_code = request_code
        self.on_image = on_image
        self.output_path = None

    def open(self, output_dir=None):
        """Open the Android system camera without requesting CAMERA permission.

        The system camera app owns camera access. We intentionally do not use
        MediaStore, FileProvider, URI grants, or android.permissions here.
        The camera returns a Bitmap thumbnail through the activity result,
        which we save into the app's private storage.
        """
        print("CAMERA: OPEN")

        try:
            Intent = autoclass("android.content.Intent")
            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            activity = PythonActivity.mActivity
            package_manager = activity.getPackageManager()

            intent = Intent(Intent.ACTION_IMAGE_CAPTURE)

            if intent.resolveActivity(package_manager) is None:
                print("CAMERA: NO CAMERA APPLICATION")
                return False

            print("CAMERA: STARTING NATIVE CAMERA")
            activity.startActivityForResult(
                intent,
                self.request_code
            )
            print("CAMERA: STARTED")
            return True

        except Exception as e:
            print("CAMERA OPEN ERROR:", repr(e))
            return False

    def handle_result(self, request_code, result_code, intent):
        print("CAMERA: HANDLE RESULT", request_code, result_code)

        if request_code != self.request_code:
            return

        try:
            Activity = autoclass("android.app.Activity")

            if result_code != Activity.RESULT_OK:
                print("CAMERA: USER CANCELLED")
                return

            if intent is None:
                print("CAMERA: RESULT INTENT NONE")
                return

            # ACTION_IMAGE_CAPTURE without EXTRA_OUTPUT returns the captured
            # image as a Bitmap in the "data" extra.
            bitmap = intent.getParcelableExtra("data")

            if bitmap is None:
                print("CAMERA: BITMAP RESULT NONE")
                return

            app = App.get_running_app()
            if app is None:
                print("CAMERA: APP IS NONE")
                return

            image_dir = os.path.join(
                app.user_data_dir,
                "images"
            )
            os.makedirs(image_dir, exist_ok=True)

            local_path = os.path.join(
                image_dir,
                "camera_" + str(int(time.time() * 1000)) + ".jpg"
            )

            FileOutputStream = autoclass(
                "java.io.FileOutputStream"
            )
            BitmapCompressFormat = autoclass(
                "android.graphics.Bitmap$CompressFormat"
            )

            output_stream = FileOutputStream(local_path)

            try:
                success = bitmap.compress(
                    BitmapCompressFormat.JPEG,
                    92,
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
                Clock.schedule_once(
                    lambda dt: self.on_image(local_path),
                    0
                )

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
