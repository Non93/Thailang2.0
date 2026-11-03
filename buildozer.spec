[app]
title = ThaiLang Compiler
package.name = thailang
package.domain = org.thaicompiler
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf,txt
version = 1.0
requirements = python3,kivy==2.3.1,cython==0.29.36
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
