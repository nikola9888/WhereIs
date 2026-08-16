import os

from jnius import autoclass
from android import activity

from kivy.app import App


class ImagePicker:

    def __init__(self, callback):

        self.callback = callback
        self.file_path = None


    def open_camera(self):

        Intent = autoclass(
            "android.content.Intent"
        )

        MediaStore = autoclass(
            "android.provider.MediaStore"
        )

        PythonActivity = autoclass(
            "org.kivy.android.PythonActivity"
        )

        intent = Intent(
            MediaStore.ACTION_IMAGE_CAPTURE
        )

        activity.bind(
            on_activity_result=self.result_callback
        )

        PythonActivity.mActivity.startActivityForResult(
            intent,
            200
        )


    def open_gallery(self):

        Intent = autoclass(
            "android.content.Intent"
        )

        PythonActivity = autoclass(
            "org.kivy.android.PythonActivity"
        )


        intent = Intent(
            Intent.ACTION_PICK
        )

        intent.setType(
            "image/*"
        )


        activity.bind(
            on_activity_result=self.result_callback
        )


        PythonActivity.mActivity.startActivityForResult(
            intent,
            201
        )


    def result_callback(
        self,
        requestCode,
        resultCode,
        intent
    ):

        if intent is None:
            return True


        uri = intent.getData()


        if uri:

            path = self.save_uri(uri)

            if self.callback:
                self.callback(path)


        return True



    def save_uri(self, uri):

        app = App.get_running_app()


        folder = os.path.join(
            app.user_data_dir,
            "images"
        )


        os.makedirs(
            folder,
            exist_ok=True
        )


        filename = os.path.join(
            folder,
            "item_image.jpg"
        )


        PythonActivity = autoclass(
            "org.kivy.android.PythonActivity"
        )


        resolver = (
            PythonActivity
            .mActivity
            .getContentResolver()
        )


        stream = resolver.openInputStream(uri)


        with open(filename,"wb") as f:

            buffer = bytearray(4096)

            while True:

                length = stream.read(buffer)

                if length <= 0:
                    break

                f.write(
                    buffer[:length]
                )


        stream.close()


        return filename