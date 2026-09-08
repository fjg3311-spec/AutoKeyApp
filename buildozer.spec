[app]

# (str) Title of your application
title = ออโต้หาคีย์

# (str) Package name
package.name = autokey

# (str) Package domain (needed for android/ios packaging)
package.domain = com.bottos

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (including ttf for Thai fonts)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let's keep it empty)
#source.exclude_exts = spec

# (list) List of directory to exclude
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,README.md

# (str) Application versioning
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,requests,urllib3,chardet,idna,certifi

# (str) Custom source folders for requirements
# Sets custom source for any requirement with recipes
# requirements.source.kivy = ../kivy

# (list) Garden modules to install
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = Name:service_script.py

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the most common color names.
#android.presplash_color = #FFFFFF

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android NDK version to use
#android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 21

# (bool) Use --private data dir ( True ) or --dir public storage ( False )
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip python-for-android compilation
#android.skip_update = False

# (bool) If True, then the build will accept all the SDK licenses automatically
android.accept_sdk_license = True

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable Android auto backup feature (API >= 23)
android.allow_backup = True

#
# Python for android (p4a) specific
#

# (str) python-for-android git repo to use
#p4a.git_clone = False

# (str) python-for-android branch to use
p4a.branch = master


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable, 1 = enable)
warn_on_root = 1
