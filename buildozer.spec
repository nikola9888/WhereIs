[app]

title = WhereIs

package.name = whereis
package.domain = com.develop4world

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,json,atlas,ttf

version = 1.0.0
android.numeric_version = 100000

requirements = python3,kivy,pyjnius,pillow

# Use the stable python-for-android branch with Python 3.12.
p4a.branch = master
p4a.python_version = 3.12

orientation = portrait
fullscreen = 1

icon.filename = assets/icon.png

# Android
# Google Play currently requires target API 35 for new Android releases.
android.api = 35
android.minapi = 24
android.build_tools_version = 35.0.0
android.accept_sdk_license = True

# Current python-for-android recommendation.
android.ndk = 28c

android.archs = arm64-v8a

android.debug_artifact = apk

android.enable_androidx = True

android.private_storage = True
android.allow_backup = True

[buildozer]

log_level = 2
warn_on_root = 0
