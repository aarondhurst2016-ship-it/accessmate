from accessibility import enable_accessibility

# Accessibility features for Talkback Assistant
def enable_accessibility(widget, tooltip=None):
    widget.focus_set()
    widget.bind('<Tab>', lambda e: widget.tk_focusNext().focus())
    widget.bind('<Shift-Tab>', lambda e: widget.tk_focusPrev().focus())
    widget.bind('<Return>', lambda e: widget.invoke() if hasattr(widget, 'invoke') else None)
    if tooltip:
        def show_tooltip(event):
            from speech import speak
            speak(tooltip)
        widget.bind('<FocusIn>', show_tooltip)

enable_accessibility = enable_accessibility
