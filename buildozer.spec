[app]
title = kitris
package.name = kitris
package.domain = com.github.sbeaugrand
source.dir = .
source.include_exts = py,png,kv,wav
source.exclude_patterns = Makefile
version = 1.0.0
requirements = kivy
icon.filename = %(source.dir)s/data/icon.png
orientation = landscape
# Android specific
fullscreen = 0
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.permissions = BLUETOOTH

[app@release]
source.include_exts = py,png,kv

[buildozer]
log_level = 2
