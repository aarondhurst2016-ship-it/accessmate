[app]
title = AccessMate
package.name = accessmate
package.domain = com.accessmate.app

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,txt,json,wav,mp3

version = 1.0.0

requirements = python3,kivy,pillow,plyer,pyjnius

[buildozer]
log_level = 2

[app:ios]
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

# iOS specific settings
orientation = portrait
osx.python_version = 3.11
osx.kivy_version = 2.1.0

# Icon settings for iOS
icon.filename = ios_icons/Icon-1024x1024@1x.png

# iOS deployment settings
ios.codesign.allowed = true
ios.codesign.debug = true

[buildozer:ios]
codesign.mode = adhoc
