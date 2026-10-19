[app]
title = Locker
package.name = locker
package.domain = com.pidori.locker
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav
version = 1.0
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 1
android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.permissions = SYSTEM_ALERT_WINDOW, FOREGROUND_SERVICE, MODIFY_AUDIO_SETTINGS, WAKE_LOCK, POST_NOTIFICATIONS
android.accept_sdk_license = True
android.allow_backup = False
