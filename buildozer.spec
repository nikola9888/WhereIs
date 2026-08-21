[app]

title = WhereIs

package.name = whereis
package.domain = com.develop4world

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,json,atlas,ttf

version = 1.0.0
android.numeric_version = 100000

requirements = python3,kivy,pyjnius,pillow,charset-normalizer==3.4.2

# Current python-for-android develop requires Python 3.14
p4a.branch = develop
p4a.python_version = 3.14

orientation = portrait
fullscreen = 1

icon.filename = assets/icon.png


# Android
android.api = 36
android.minapi = 24
android.build_tools_version = 35.0.0
android.accept_sdk_license = True

# p4a develop is aligned with modern Android NDK versions
android.ndk = 29

android.archs = arm64-v8a

android.debug_artifact = apk

android.enable_androidx = True

android.private_storage = True
android.allow_backup = True


[buildozer]

log_level = 2
warn_on_root = 0
