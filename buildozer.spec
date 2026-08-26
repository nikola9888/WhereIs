[app]

title = WhereIs

package.name = whereis
package.domain = com.develop4world

source.dir = .
source.include_exts = py,png,jpg,jpeg,webp,kv,json,atlas,ttf

version = 1.0.0
android.numeric_version = 100001

requirements = python3==3.10.11,hostpython3==3.10.11,kivy,pyjnius,pillow

p4a.branch = master
p4a.python_version = 3.10
p4a.source_dir = python-for-android

orientation = portrait
fullscreen = 1

icon.filename = assets/Icon.png/home.png

# Android / Google Play
android.api = 35
android.minapi = 24
android.build_tools_version = 35.0.0
android.accept_sdk_license = True
android.ndk = 25c
android.archs = arm64-v8a
android.debug_artifact = apk
android.enable_androidx = True
android.private_storage = True
android.allow_backup = True

# Native Android camera intent.
android.permissions = android.permission.CAMERA
android.features = android.hardware.camera

[buildozer]
log_level = 2
warn_on_root = 0
