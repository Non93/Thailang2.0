[app]

# (str) Title of your application
title = SampleApp

# (str) Package name
package.name = nfsApk

# (str) Package domain (needed for android/ios packaging)
package.domain = org.novfensec

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
source.include_patterns = images/*.png

# (list) Application requirements
# แก้ไข: ลบ pycairo และ materialshapes ออก และล็อคเวอร์ชัน materialyoucolor
requirements = python3, kivy==2.3.1, https://github.com/kivymd/KivyMD/archive/master.zip, exceptiongroup, asyncgui, asynckivy, materialyoucolor==3.0.3, android

# (str) Presplash of the application
presplash.filename = %(source.dir)s/images/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/images/favicon.png

# (list) Supported orientations
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API, should be as high as possible.
# แก้ไข: ลดลงมาเป็น 34 เพื่อความเสถียร
android.api = 34

# (int) Minimum API your APK / AAB will support.
android.minapi = 30

# (bool) If True, then automatically accept SDK license agreements.
android.accept_sdk_license = True

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk or aar).
android.release_artifact = aab

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk

#
# Python for android (p4a) specific
#

# (str) python-for-android branch to use, defaults to master
# แก้ไข: คอมเมนต์ develop ออก เพื่อใช้ master (เสถียรกว่า)
#p4a.branch = develop

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# Another platform dependency: ios-deploy
ios.ios_deploy_url = https://github.com/ios-control/ios-deploy
ios.ios_deploy_branch = master

# (bool) Whether or not to sign the code
ios.codesign.allowed = false


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
