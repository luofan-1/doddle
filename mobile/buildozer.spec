[app]
title = doddle
package.name = doddle
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1

# Android 版本
android.api = 33
android.ndk = 25b
android.sdk = 24
android.accept_sdk_license = True

# 权限（必须开网络才能同步坚果云）
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# 主程序
entrypoint = mobile.py

# 依赖
requirements = python3,kivy,kivymd,webdav-client

# 方向
android.arch = arm64-v8a
android.use_aapt2 = True