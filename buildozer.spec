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

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3, kivy==2.3.1, https://github.com/kivymd/KivyMD/archive/master.zip, exceptiongroup, asyncgui, asynckivy, materialyoucolor==3.0.3, android, google-genai

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/images/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/images/favicon.png

# (list) Supported orientations
orientation = portrait

#
# Android specific
#

fullscreen = 0
android.api = 34
android.minapi = 30
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True
android.release_artifact = aab
android.debug_artifact = apk

# 
# Python for android (p4a) specific
#

# (str) python-for-android branch to use, defaults to master
#p4a.branch = develop

#
# iOS specific
#

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/ios-control/ios-deploy
ios.ios_deploy_branch = master
ios.codesign.allowed = false


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
