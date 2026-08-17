[app]

title = WhereIs

package.name = whereis
package.domain = com.develop4world

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,json,atlas,ttf

version = 1.0.0
android.numeric_version = 100000

requirements = python3,kivy,pyjnius

p4a.branch = develop
p4a.python_version = 3.10

orientation = portrait
fullscreen = 1

icon.filename = assets/icon.png


# Android
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
