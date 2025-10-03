# Accessibility module for Talkback Assistant

import tkinter as tk
from tkinter import ttk
import os

def enable_accessibility(widget, tooltip=None):
    """
    Enable accessibility features for a widget.
    
    Args:
        widget: The tkinter widget to enhance
        tooltip: Optional tooltip text for the widget
    """
    if tooltip:
        # Create tooltip functionality
        create_tooltip(widget, tooltip)
    
    # Add keyboard navigation support
    if isinstance(widget, (tk.Button, ttk.Button)):
        # Make buttons focusable with keyboard
        widget.configure(takefocus=True)
        
        # Add Enter key support
        def on_enter_key(event):
            if hasattr(widget, 'invoke'):
                widget.invoke()
        widget.bind('<Return>', on_enter_key)
        widget.bind('<space>', on_enter_key)
    
    elif isinstance(widget, (ttk.Combobox)):
        # Ensure comboboxes are keyboard accessible
        widget.configure(takefocus=True)

def create_tooltip(widget, text):
    """
    Create a tooltip for a widget.
    
    Args:
        widget: The widget to add tooltip to
        text: The tooltip text
    """
    def on_enter(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        
        label = tk.Label(
            tooltip,
            text=text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Arial", 10),
            wraplength=300
        )
        label.pack()
        
        widget.tooltip = tooltip
    
    def on_leave(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
            delattr(widget, 'tooltip')
    
    widget.bind('<Enter>', on_enter)
    widget.bind('<Leave>', on_leave)

