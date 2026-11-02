[app]

# ชื่อแอปที่แสดงบนมือถือ
title = ThaiLang Compiler

# ชื่อแพ็กเกจ (ต้องเป็นตัวพิมพ์เล็ก ไม่มีช่องว่าง)
package.name = thailang
package.domain = org.thaicompiler

# โฟลเดอร์ที่มีโค้ด
source.dir = .

# นามสกุลไฟล์ที่จะรวมใน APK
source.include_exts = py,png,jpg,kv,atlas,json,ttf,txt

# เวอร์ชัน
version = 1.0

# Dependencies ที่ต้องติดตั้งใน APK
# - python3 และ kivy จำเป็น
# - urllib, hashlib, json, math, random, re มีใน standard library อยู่แล้ว ไม่ต้องใส่
requirements = python3,kivy==2.3.1,urllib3,chardet,idna,certifi

# การตั้งค่าหน้าจอ
orientation = portrait
fullscreen = 0

# Permissions ที่ต้องการ
android.permissions = INTERNET

# ค่า Android SDK/NDK (ค่าที่เสถียร)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# ป้องกันปัญหา build บางกรณี
android.accept_sdk_license = True
android.allow_backup = True

# ค่า build
# (ปล่อยค่าเริ่มต้นไว้ก็ได้ ยกเว้นถ้าอยากปรับ)
[buildozer]
log_level = 2
warn_on_root = 1
