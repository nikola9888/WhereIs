[app]

title = WhereIs

package.name = whereis
package.domain = com.develop4world

source.dir = .
source.include_exts = py,png,jpg,jpeg,webp,kv,json,atlas,ttf

version = 1.0.0
android.numeric_version = 100001

requirements = python3==3.10.11,hostpython3==3.10.11,kivy,pyjnius,pillow

# Use the current python-for-android development branch required for
# current Android Store submissions / API 36.
p4a.branch = develop
p4a.python_version = 3.10
p4a.source_dir = python-for-android

orientation = portrait
fullscreen = 1

# No app icon configured here because assets/Icon.png is a directory
# containing the application's UI icons, not a single PNG file.

# Android / Google Play
android.api = 36
android.minapi = 24
android.accept_sdk_license = True
android.ndk = 28c
android.archs = arm64-v8a
android.release_artifact = aab
android.enable_androidx = True
android.private_storage = True
android.allow_backup = True

# Camera permission. Do not use android.features here: the current
# python-for-android toolchain rejects --feature.
android.permissions = android.permission.CAMERA

[buildozer]
log_level = 2
warn_on_root = 0
