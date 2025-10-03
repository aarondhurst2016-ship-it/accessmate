# Help sheet module for Talkback Assistant

def get_help_sheet():
    """Return comprehensive help information"""
    return """
[HELP] ACCESSMATE HELP GUIDE

📋 QUICK START:
• Select your microphone from the dropdown
- Click "Test Microphone" to verify it works
- Use any feature button for assistance
- Press F1 anytime for accessibility help

[MICROPHONE] MICROPHONE FEATURES:
- Test Microphone: Record and playback test
- Microphone selection dropdown
- Speech recognition ready
- Voice command processing

[TIME] TIME & DATE FEATURES:
- Say Time: Speaks current time
- Say Date: Announces today's date
- Always available offline

[WEATHER] WEATHER:
- Say Weather: Weather information
- Location-based forecasts
- Voice announcements

[THEMES] THEMES & ACCESSIBILITY:
• Dark Theme: Easy on eyes
• Light Theme: High visibility  
• Blue Theme: Modern interface
• High contrast options available

[KEYS] KEYBOARD SHORTCUTS:
• Tab: Navigate between elements
• Enter/Space: Activate buttons
• Ctrl+Shift+C: High contrast mode
• Ctrl+Shift+F: Large font mode
• Ctrl+Shift+S: Toggle screen reader
• F1: Show accessibility help

[SETTINGS] SETTINGS & CUSTOMIZATION:
• Theme selection
• Microphone preferences
• Accessibility options
• Voice settings


� EMAIL MANAGEMENT:
• View your inbox and read emails from Gmail, Outlook, Yahoo, and more
• Accessible email reading interface
• Email login required (see Email button)


 REMINDERS & APPOINTMENTS:
• Add, view, and manage reminders and calendar appointments
• Set one-time or recurring reminders
• Get notified for upcoming events

�️ FILE MANAGER:
• Browse, open, rename, and delete files and folders
• Read files aloud with text-to-speech
• Fully accessible interface on desktop and mobile

[HOME] SMART HOME CONTROL:
• Discover and control smart plugs, bulbs, thermostats, and TVs
• Advanced TV controls: volume, input, app launch, play content
• Works on desktop and mobile


🎵 MEDIA PLAYBACK:
• Play, pause, resume, stop, seek, and adjust volume for local audio files
• Fully accessible interface on desktop and mobile


[TRANSLATE] TRANSLATION SERVICES:
• Instantly translate text to multiple languages
• Choose target language (e.g., Spanish, French, German)
• Accessible on desktop and mobile

💪 HEALTH & FITNESS:
• View health tips and activity suggestions
• Track wellness and healthy habits
• Accessible interface for all users

[SECURITY] SECURITY FEATURES:
• Check device and account security status
• Get security tips and alerts
• Accessible security dashboard

[NOTES] NOTES & TO-DO LISTS:
• Create, edit, and manage notes and to-do items
• Save and organize important information
• Fully accessible notes interface

📍 LOCATION SERVICES:
• Get your current location with one click
• Location-based features and info
• Accessible on all platforms

♿ ACCESSIBILITY FEATURES:
• Full screen reader support
• Keyboard navigation
• Focus highlighting
• Tooltips on all controls
• Voice feedback
• High contrast modes
• Large font options
• Error announcements

🎵 VOICE COMMANDS:
Say these phrases after clicking a voice button:
• "What time is it?" - Gets current time
• "What's the date?" - Gets current date  
• "How's the weather?" - Weather info
• "Hello" - Friendly greeting
• "Help" - Voice help menu

🔊 AUDIO FEATURES:
• Text-to-speech for all content
• Adjustable speech rate
• Multiple voice options
• Clear pronunciation
• Error announcements

💡 TIPS FOR BEST EXPERIENCE:
• Ensure microphone permissions are granted
• Use in quiet environment for voice recognition
• Keep microphone close but not too close
• Speak clearly and at normal pace
• Check microphone levels in system settings

🆘 TROUBLESHOOTING:
• Microphone not working? Check system permissions
• No speech output? Check volume settings
• App not responding? Try restarting
• Features missing? Check internet connection

� SUPPORT:
• For support, use the in-app Support Message Center (found in the Help or Feedback menu)
• Documentation: Check README files
• Updates: Automatic when available

[HELP] GETTING HELP:
• This help guide is always available
• Voice announcements explain each feature
• Hover over buttons for tooltips
• Use F1 key for accessibility guide

Thank you for using AccessMate!
Your accessible, voice-enabled digital companion.
"""

def get_quick_help():
    """Return brief help for voice announcements"""
    return """
Quick help: Use the microphone dropdown to select your input device. 
Test the microphone with the orange button. 
Click Say Time, Say Date, or Say Weather for instant voice information.
Press F1 for detailed accessibility help.
All buttons have voice descriptions when you hover over them.
"""

def get_voice_commands_help():
    """Return help specifically for voice commands"""
    return """
Voice Commands Help:
After clicking a voice input button, you can say:
- What time is it? 
- What's the date?
- How's the weather?
- Hello or Hi for a greeting
- Help for voice assistance
The app will respond with speech and display information on screen.
"""

def get_accessibility_help():
    """Return accessibility-focused help"""
    return """
Accessibility Features:
- Full keyboard navigation with Tab and Shift-Tab
- Screen reader compatible with focus announcements
- High contrast mode: Press Ctrl+Shift+C
- Large font mode: Press Ctrl+Shift+F  
- All buttons have descriptive tooltips
- Voice feedback for all major actions
- Error messages are both spoken and displayed
- Focus highlighting shows current selection
Press F1 anytime to open detailed accessibility help window.
"""

def get_troubleshooting_help():
    """Return troubleshooting information"""
    return """
Common Issues and Solutions:

MICROPHONE PROBLEMS:
- Check system microphone permissions
- Ensure microphone is not muted
- Try selecting different microphone from dropdown
- Test with the orange "Test Microphone" button

SPEECH OUTPUT PROBLEMS:  
- Check system volume settings
- Ensure speakers/headphones are connected
- Try adjusting speech rate in settings
- Restart the application

GENERAL ISSUES:
- Close and restart the application
- Check internet connection for weather features
- Ensure all required permissions are granted
- Update system audio drivers if needed

If problems persist, check the README file or contact support.
"""

def get_feature_overview():
    """Return overview of all features"""
    return """
Talkback Assistant Features Overview:

CURRENT FEATURES:
✓ Microphone selection and testing
✓ Text-to-speech announcements  
✓ Time and date speaking
✓ Weather information (basic)
✓ Theme customization
✓ Full accessibility support
✓ Voice command recognition
✓ Comprehensive help system
✓ Calendar appointments and reminders
✓ Smart home device control (plugs, lights, thermostats, TVs: on/off, volume, input, apps, play content)


CURRENT FEATURES:
✓ File system navigation (browse, open, rename, delete, read aloud)

CURRENT FEATURES:
✓ File system navigation (browse, open, rename, delete, read aloud)
✓ Media playback (play, pause, resume, stop, seek, and volume for local audio files; accessible UI on desktop and mobile)



The app is designed to be your comprehensive digital assistant with full voice control and accessibility features.
"""

# Dictionary for context-sensitive help
CONTEXT_HELP = {
    "microphone": "Select your preferred microphone from the dropdown. Click 'Test Microphone' to verify it's working properly.",
    "themes": "Choose between Dark (easy on eyes), Light (high visibility), or Blue (modern) themes.",
    "time": "Click 'Say Time' to hear the current time announced clearly.",
    "date": "Click 'Say Date' to hear today's full date including day of week.",
    "weather": "Click 'Say Weather' for current weather information in your area.",
    "accessibility": "Full screen reader support with keyboard navigation, high contrast, and voice feedback.",
    "help": "This comprehensive help system provides guidance for all features and accessibility options."
}

def get_context_help(context):
    """Get help for specific context/feature"""
    return CONTEXT_HELP.get(context.lower(), "No specific help available for this feature.")

def speak_help_if_available(help_text):
    """Speak help text if speech module is available"""
    try:
        from speech import speak
        speak("Help information displayed. Check the main window for details.")
    except ImportError:
        print("Speech module not available - help displayed in text only")

if __name__ == "__main__":
    # Test the help system
    print(get_help_sheet())
    print("\n" + "="*50 + "\n")
    print(get_quick_help())