[app]

title = WhereIs

package.name = whereis
package.domain = com.develop4world

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,json,atlas,ttf

version = 1.0.0
android.numeric_version = 100000

requirements = python3,kivy,pyjnius,pillow

# Pin python-for-android to the tested 2026.05.09 release.
# Do not use master here: newer master currently resolves Python 3.14
# and can select Android-specific charset-normalizer wheels during the
# host-side pip installation stage.
p4a.branch = v2026.05.09
p4a.python_version = 3.12

orientation = portrait
fullscreen = 1

icon.filename = assets/icon.png

# Android / Google Play
android.api = 35
android.minapi = 24
android.build_tools_version = 35.0.0
android.accept_sdk_license = True

# Keep the NDK version explicitly pinned for reproducible CI builds.
android.ndk = 28c

android.archs = arm64-v8a

android.debug_artifact = apk

android.enable_androidx = True
android.private_storage = True
android.allow_backup = True

[buildozer]

log_level = 2
warn_on_root = 0
