[app]

title = WhereIs

package.name = whereis
package.domain = com.develop4world

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,json,atlas,ttf

version = 1.0.0
android.numeric_version = 100000

# Pin both Android Python and host Python to 3.10.
# This prevents p4a from selecting Python 3.14 and downloading
# an Android-specific charset-normalizer wheel that host pip cannot install.
requirements = python3==3.10.11,hostpython3==3.10.11,kivy,pyjnius,pillow

p4a.branch = master
p4a.python_version = 3.10

orientation = portrait
fullscreen = 1

# Use an existing valid PNG from the repository as the Android icon.
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

[buildozer]

log_level = 2
warn_on_root = 0
