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

# ล็อคเวอร์ชันให้เป็น 31 ซึ่งเป็นเวอร์ชันที่ Build ผ่านชัวร์ๆ
android.api = 31
android.minapi = 21
android.build_tools_version = 31.0.0
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
