[app]
title = ThaiLang Compiler
package.name = thailang
package.domain = org.thaicompiler
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf,txt
version = 1.0
# openssl + certifi: จำเป็นสำหรับ "โหลดข้อมูลจากเว็บ" ผ่าน https
requirements = python3,kivy==2.3.1,openssl,certifi
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.accept_sdk_license = True
android.api = 31
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
