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
        """Open the Android system camera without requesting CAMERA permission."""
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

            # Normal ACTION_IMAGE_CAPTURE result: Bitmap in "data".
            bitmap = None
            try:
                bitmap = intent.getParcelableExtra("data")
            except Exception as e:
                print("CAMERA: BITMAP READ ERROR:", repr(e))

            if bitmap is not None:
                print("CAMERA: BITMAP RESULT FOUND")

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

                if success and os.path.isfile(local_path):
                    size = os.path.getsize(local_path)
                    print("CAMERA: BITMAP SAVED:", local_path, size)

                    if size > 0:
                        self._deliver_image(local_path)
                        return

                print("CAMERA: BITMAP SAVE FAILED")

            # Fallback: some camera apps return a content URI instead.
            try:
                uri = intent.getData()
            except Exception as e:
                uri = None
                print("CAMERA: URI READ ERROR:", repr(e))

            if uri is not None:
                print("CAMERA: URI RESULT FOUND:", uri)

                if self._copy_uri_to_file(uri, local_path):
                    self._deliver_image(local_path)
                    return

            print("CAMERA: NO USABLE IMAGE RESULT")

            try:
                if os.path.isfile(local_path):
                    os.remove(local_path)
            except Exception:
                pass

        except Exception as e:
            print("CAMERA HANDLE ERROR:", repr(e))

    def _copy_uri_to_file(self, uri, local_path):
        try:
            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )
            FileOutputStream = autoclass(
                "java.io.FileOutputStream"
            )

            activity = PythonActivity.mActivity
            resolver = activity.getContentResolver()
            stream = resolver.openInputStream(uri)

            if stream is None:
                print("CAMERA: URI INPUT STREAM NONE")
                return False

            output = FileOutputStream(local_path)

            try:
                buffer = bytearray(64 * 1024)
                while True:
                    count = stream.read(buffer)
                    if count <= 0:
                        break
                    output.write(buffer, 0, count)
            finally:
                try:
                    stream.close()
                except Exception:
                    pass
                try:
                    output.close()
                except Exception:
                    pass

            if not os.path.isfile(local_path):
                return False

            size = os.path.getsize(local_path)
            print("CAMERA: URI COPIED:", local_path, size)
            return size > 0

        except Exception as e:
            print("CAMERA URI COPY ERROR:", repr(e))
            return False

    def _deliver_image(self, local_path):
        self.output_path = local_path

        print("CAMERA: SUCCESS:", local_path)
        print("CAMERA: SENDING IMAGE TO ADD ITEM")

        if self.on_image:
            Clock.schedule_once(
                lambda dt: self.on_image(local_path),
                0
            )

    def delete_output(self):
        if self.output_path:
            try:
                if os.path.isfile(self.output_path):
                    os.remove(self.output_path)
                    print("CAMERA: LOCAL OUTPUT DELETED")
            except Exception as e:
                print("CAMERA DELETE ERROR:", repr(e))

        self.output_path = None
