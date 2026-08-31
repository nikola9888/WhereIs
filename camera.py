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
        self.output_uri = None
        self.output_pending = False
        self.camera_package = None

    def open(self, output_dir=None):
        print("CAMERA: OPEN")

        try:
            # The caller handles the Android CAMERA permission request.
            # Do not check it again here because Android may not have updated
            # check_permission() immediately after the permission callback.
            Intent = autoclass("android.content.Intent")
            ClipData = autoclass("android.content.ClipData")
            ContentValues = autoclass("android.content.ContentValues")
            MediaStoreImages = autoclass(
                "android.provider.MediaStore$Images$Media"
            )
            BuildVersion = autoclass("android.os.Build$VERSION")
            PythonActivity = autoclass("org.kivy.android.PythonActivity")

            activity = PythonActivity.mActivity
            resolver = activity.getContentResolver()

            app = App.get_running_app()
            if app is None:
                print("CAMERA: APP IS NONE")
                return False

            image_dir = output_dir or os.path.join(
                app.user_data_dir,
                "images"
            )
            os.makedirs(image_dir, exist_ok=True)

            filename = (
                "whereis_camera_"
                + str(int(time.time() * 1000))
                + ".jpg"
            )

            values = ContentValues()
            values.put("display_name", filename)
            values.put("mime_type", "image/jpeg")

            if BuildVersion.SDK_INT >= 29:
                values.put("relative_path", "Pictures/WhereIs")
                values.put("is_pending", 1)

            uri = resolver.insert(
                MediaStoreImages.EXTERNAL_CONTENT_URI,
                values
            )

            if uri is None:
                print("CAMERA: MEDIASTORE INSERT FAILED")
                return False

            intent = Intent(Intent.ACTION_IMAGE_CAPTURE)
            intent.putExtra(Intent.EXTRA_OUTPUT, uri)
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            intent.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION)
            intent.setClipData(ClipData.newRawUri("WhereIs", uri))

            package_manager = activity.getPackageManager()
            resolve_info = intent.resolveActivity(package_manager)

            if resolve_info is None:
                print("CAMERA: NO CAMERA APPLICATION")
                try:
                    resolver.delete(uri, None, None)
                except Exception:
                    pass
                return False

            camera_package = resolve_info.activityInfo.packageName

            try:
                activity.grantUriPermission(
                    camera_package,
                    uri,
                    Intent.FLAG_GRANT_READ_URI_PERMISSION
                    | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                )
                self.camera_package = camera_package
                print("CAMERA: URI GRANTED TO:", camera_package)
            except Exception as e:
                print("CAMERA: EXPLICIT URI GRANT FAILED:", repr(e))

            self.output_uri = uri
            self.output_path = None
            self.output_pending = BuildVersion.SDK_INT >= 29

            print("CAMERA: OUTPUT URI:", uri)
            print("CAMERA: STARTING NATIVE CAMERA")

            activity.startActivityForResult(
                intent,
                self.request_code
            )

            print("CAMERA: STARTED")
            return True

        except Exception as e:
            print("CAMERA OPEN ERROR:", repr(e))
            self._delete_output_uri()
            self._clear_state()
            return False

    def handle_result(self, request_code, result_code, intent):
        print("CAMERA: HANDLE RESULT", request_code, result_code)

        if request_code != self.request_code:
            return

        try:
            Activity = autoclass("android.app.Activity")
            Intent = autoclass("android.content.Intent")

            if result_code != Activity.RESULT_OK:
                print("CAMERA: USER CANCELLED")
                self._delete_output_uri()
                self._clear_state()
                return

            if self.output_uri is None:
                print("CAMERA: OUTPUT URI NONE")
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

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            FileOutputStream = autoclass("java.io.FileOutputStream")
            BuildVersion = autoclass("android.os.Build$VERSION")

            activity = PythonActivity.mActivity
            resolver = activity.getContentResolver()
            stream = resolver.openInputStream(self.output_uri)

            if stream is None:
                print("CAMERA: OUTPUT INPUT STREAM NONE")
                self._delete_output_uri()
                self._clear_state()
                return

            output_stream = FileOutputStream(local_path)

            try:
                buffer = bytearray(64 * 1024)
                total = 0

                while True:
                    count = stream.read(buffer)
                    if count <= 0:
                        break
                    output_stream.write(buffer, 0, count)
                    total += count
            finally:
                try:
                    stream.close()
                except Exception:
                    pass
                try:
                    output_stream.close()
                except Exception:
                    pass

            if BuildVersion.SDK_INT >= 29 and self.output_pending:
                ContentValues = autoclass("android.content.ContentValues")
                values = ContentValues()
                values.put("is_pending", 0)
                resolver.update(
                    self.output_uri,
                    values,
                    None,
                    None
                )

            print("CAMERA: COPIED BYTES:", total)

            if not os.path.isfile(local_path):
                print("CAMERA: LOCAL FILE NOT CREATED")
                self._delete_output_uri()
                self._clear_state()
                return

            size = os.path.getsize(local_path)
            print("CAMERA: LOCAL FILE SIZE:", size)

            if size <= 0:
                print("CAMERA: LOCAL FILE EMPTY")
                try:
                    os.remove(local_path)
                except Exception:
                    pass
                self._delete_output_uri()
                self._clear_state()
                return

            self.output_path = local_path
            print("CAMERA: SUCCESS:", local_path)

            saved_uri = self.output_uri
            saved_package = self.camera_package

            if saved_package:
                try:
                    activity.revokeUriPermission(
                        saved_package,
                        saved_uri,
                        Intent.FLAG_GRANT_READ_URI_PERMISSION
                        | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                    )
                except Exception as e:
                    print("CAMERA: REVOKE URI GRANT ERROR:", repr(e))

            self._delete_output_uri()
            self.output_uri = None
            self.output_pending = False
            self.camera_package = None

            if self.on_image:
                Clock.schedule_once(
                    lambda dt: self.on_image(local_path),
                    0
                )

        except Exception as e:
            print("CAMERA HANDLE ERROR:", repr(e))
            self._delete_output_uri()
            self._clear_state()

    def _clear_state(self):
        self.output_path = None
        self.output_uri = None
        self.output_pending = False
        self.camera_package = None

    def _delete_output_uri(self):
        if self.output_uri is None:
            return

        try:
            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )
            activity = PythonActivity.mActivity
            resolver = activity.getContentResolver()
            resolver.delete(self.output_uri, None, None)
            print("CAMERA: OUTPUT URI DELETED")
        except Exception as e:
            print("CAMERA URI DELETE ERROR:", repr(e))

    def delete_output(self):
        if self.output_path:
            try:
                if os.path.isfile(self.output_path):
                    os.remove(self.output_path)
                    print("CAMERA: LOCAL OUTPUT DELETED")
            except Exception as e:
                print("CAMERA DELETE ERROR:", repr(e))

        self._delete_output_uri()
        self._clear_state()
