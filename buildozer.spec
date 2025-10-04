[app]

# (str) Title of your application
title = AccessMate

# (str) Package name
package.name = accessmate

# (str) Package domain (needed for android/ios packaging)
package.domain = com.accessmate

# (str) Source code where the main.py live
source.dir = src

# (str) Main script for Android (use Android-compatible version)
source.main = main_android.py

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt,json,wav,mp3

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,data/*,*.md

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests,bin,build,dist,__pycache__,.git,.github

# (list) List of exclusions using pattern matching
source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"]([^'"]*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,pillow

# (str) Bootstrap to use for android builds  
p4a.bootstrap = sdl2

# (bool) Indicate if the application should be fullscreen or not
autofullscreen = 0

# (str) Android entry point, default is ok for Kivy-based app
# android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to whitelist for the whole project
# android.whitelist =

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
presplash.filename = %(source.dir)s/android_icon.png

# (str) Icon of the application  
icon.filename = %(source.dir)s/android_icon.png

# (str) Android specific icons
# Use the properly structured Android icons 
android.add_src = android_icons

# Android adaptive icon configuration
android.adaptive_icon.background_color = #000000
android.adaptive_icon.foreground_color = #FFD600

# Android presplash configuration
android.presplash_color = #000000

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
# services = AccessMateService:./service/accessmate_service.py:foreground

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 1.9.1

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format.
# see https://lottie.github.io/lottie-spec/ for examples and https://airbnb.design/lottie/
# for general documentation.
# Lottie files can be created using various tools, like Adobe After Effects or Synfig.
#android.presplash_lottie = "path/to/lottie/file.json"

# (str) Adaptive icon of the application (used if Android API level is 26+ at runtime)
#icon.adaptive_foreground.filename = %(source.dir)s/data/icon_fg.png
#icon.adaptive_background.filename = %(source.dir)s/data/icon_bg.png

# (list) Permissions
# (See https://developer.android.com/guide/topics/permissions/overview for all available permissions)
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,RECORD_AUDIO,MODIFY_AUDIO_SETTINGS,WAKE_LOCK,FOREGROUND_SERVICE,ACCESS_NETWORK_STATE,CAMERA,BLUETOOTH,BLUETOOTH_ADMIN,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,VIBRATE,SYSTEM_ALERT_WINDOW,BIND_ACCESSIBILITY_SERVICE,RECEIVE_BOOT_COMPLETED

# (list) features (adds uses-feature -tags to manifest)
android.features = android.hardware.microphone,android.hardware.camera,android.hardware.bluetooth,android.software.leanback

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
android.ndk_path = 

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
android.sdk_path = 

# (str) ANT directory (if empty, it will be automatically downloaded.)
android.ant_path = 

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
# use that parameter together with android.entrypoint to set custom Java class instead of PythonActivity
android.activity_class_name = org.kivy.android.PythonActivity

# (str) Extra xml to write directly inside the <manifest> element of AndroidManifest.xml
# use that parameter to provide a filename from where to load your custom XML code
android.extra_manifest_xml = %(source.dir)s/android_manifest/extra_manifest.xml

# (str) Extra xml to write directly inside the <manifest><application> element of AndroidManifest.xml
# use that parameter to provide a filename from where to load your custom XML code
android.extra_manifest_application_xml = %(source.dir)s/android_manifest/extra_application.xml

# (str) Full name including package path of the Java class that implements Python Service
# use that parameter to set custom Java class which extends PythonService
android.service_class_name = org.kivy.android.PythonService

# (str) Android app theme, default is ok for Kivy-based app
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
android.whitelist = 

# (str) Path to a custom whitelist file
android.whitelist_src = 

# (str) Path to a custom blacklist file
android.blacklist_src = 

# (list) List of Java .jar files to add to the libs so that pyjnius can access their classes. Don't add jars that you do not need, since extra jars can slow down the build process. Allows wildcards matching, for example: OUYA-ODK/libs/*.jar
android.add_jars = 

# (list) List of Java files to add to the android project (can be java or a directory containing the files)
android.add_src = 

# (list) Android AAR archives to add
android.add_aars = 

# (list) Put these files or directories in the apk assets directory.
# Either form may be used, and assets need not be in 'source.include_exts'.
# 1) android.add_assets = file1.txt,file2.png,dir1,dir2/
# 2) android.add_assets.1 = path/to/file1.txt
#    android.add_assets.2 = path/to/file2.png
#    android.add_assets.3 = path/to/dir1
#    android.add_assets.4 = path/to/dir2/
android.add_assets = 

# (list) Gradle dependencies to add
android.gradle_dependencies = 

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' package, or any package from Kotlin source.
# android.enable_androidx requires android.api >= 28
android.enable_androidx = True

# (list) add java compile options
# this can for example be necessary when importing certain java libraries using the 'android.gradle_dependencies' option
# see https://developer.android.com/studio/write/java8-support for further information
# android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (list) Gradle repositories to add {can be necessary for some android.gradle_dependencies}
# please enclose in double quotes 
# e.g. android.gradle_repositories = "google()", "jcenter()", "mavenCentral()"
android.gradle_repositories = "google()", "mavenCentral()"

# (list) packaging options to add 
# see https://google.github.io/android-gradle-dsl/current/com.android.build.gradle.internal.dsl.PackagingOptions.html
# can be necessary to solve conflicts in gradle_dependencies
# please enclose in double quotes 
# e.g. android.add_packaging_options = "exclude 'META-INF/common.kotlin_module'", "exclude 'META-INF/*.kotlin_module'"
android.add_packaging_options = 

# (list) Java classes to add as activities to the manifest.
android.add_activities = com.accessmate.AccessibilityService,com.accessmate.BootReceiver

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
android.ouya.category = APP

# (str) Filename of OUYA Console icon. It must be a 732x412 jpg image.
android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.jpg

# (str) XML file to include as an intent filters in <activity> tag
android.manifest.intent_filters = 

# (str) launchMode to set for the main activity
android.manifest.launch_mode = standard

# (str) screenOrientation to set for the main activity.
# Valid values can be found at https://developer.android.com/guide/topics/manifest/activity-element
android.manifest.orientation = portrait

# (list) Android application meta-data to set (key=value format)
android.meta_data = 

# (list) Android library project to add (will be added in the
# project.properties automatically.)
android.library_references = 

# (list) Android shared libraries which will be added to AndroidManifest.xml using <uses-library> tag
android.uses_library = 

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Android logcat only display log for activity's pid
android.logcat_pid_only = False

# (str) Android additional adb arguments
android.adb_args = -H host.docker.internal

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# In past, was `android.arch` as we weren't supporting builds for multiple archs at the same time.
android.archs = arm64-v8a, armeabi-v7a

# (int) overrides automatic versionCode computation (used in build.gradle)
# this is not the same as app version and should only be edited if you know what you're doing
# android.numeric_version = 1

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for custom backup rules (see official auto backup documentation)
# android.backup_rules = 

# (bool) If True, then zip the libs after the gradle build
android.no_byte_compile_python = False

# (str) The format used to package the app for release mode (aab or apk or 'both').
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aab).
android.debug_artifact = apk

#
# Python for android (p4a) specific
#

# (str) python-for-android URL, defaults to upstream (kivy)
#p4a.url = 

# (str) python-for-android fork to use in case if p4a.url is not specified, defaults to upstream (kivy)
#p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
#p4a.branch = main

# (str) python-for-android specific commit to use, defaults to HEAD, must be within p4a.branch
#p4a.commit = HEAD

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir = 

# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes = 

# (str) Filename to the hook for p4a
#p4a.hook = 

# (str) Bootstrap to use for android builds
# Run `buildozer android p4a -- bootstraps` for a list of valid bootstraps.
# p4a.bootstrap = sdl2 (configured above)

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port = 

# Control passing the --use-setup-py vs --ignore-setup-py to p4a
# "in the future" --use-setup-py is going to be the default behaviour in p4a, right now it is not
# Setting this to false will pass --ignore-setup-py, true will pass --use-setup-py
# NOTE: this is general setuptools integration, having pyproject.toml is enough, no need to generate
# setup.py if you're using Poetry, but you need to add "toml" to source.include_exts.
#p4a.setup_py = false

# (str) extra command line arguments to pass when invoking pythonforandroid.toolchain
#p4a.extra_args = 


#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_url = https://github.com/kivy/kivy-ios
# Alternately, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# Another platform dependency: ios-deploy
# Uncomment to use a custom checkout
#ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
#ios.ios_deploy_branch = 1.7.0

# (bool) Whether or not to sign the code
ios.codesign.allowed = false

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: Xcode > Window > Devices and Simulators > Select a device > View Device Logs
# Also available in the Output log of Xcode when you Build
ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) The development team to use for signing the debug version
ios.codesign.development_team.debug = <hexstring>

# (str) Name of the certificate to use for signing the release version
ios.codesign.release = %(ios.codesign.debug)s

# (str) The development team to use for signing the release version
ios.codesign.development_team.release = <hexstring>

# (str) URL pointing to .ipa file to be installed
# This option should be defined along with `display_image_url` and `full_size_image_url` options.
ios.manifest.app_url = 

# (str) URL pointing to an icon (57x57px) to be displayed during download
# This option should be defined along with `app_url` and `full_size_image_url` options.
ios.manifest.display_image_url = 

# (str) URL pointing to a large icon (512x512px) to be displayed during download
# This option should be defined along with `app_url` and `display_image_url` options.
ios.manifest.full_size_image_url = 


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
bin_dir = ./bin

# Android specific configurations for better icon support