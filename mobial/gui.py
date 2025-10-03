# --- Reminder Notification Polling for Mobile ---
import threading
import time
import datetime
def poll_reminders_for_notifications():
    import sys
    sys.path.append("../src")
    import reminders as reminders_backend
    import tkinter.messagebox as messagebox
    while True:
        now = datetime.datetime.now()
        reminders = reminders_backend.get_reminders(user="local")
        for r in reminders:
            if r.get("notified"):
                continue
            try:
                dt = r["datetime"]
                try:
                    due = datetime.datetime.fromisoformat(dt)
                except Exception:
                    due = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M")
                if due <= now:
                    msg = f"{r.get('title','Reminder')}: {r.get('description','') or ''}"
                    try:
                        messagebox.showinfo("Reminder", msg)
                    except Exception:
                        pass
                    reminders_backend.update_reminder(r["id"], notified=True)
            except Exception:
                continue
        time.sleep(60)

def start_reminder_notification_thread():
    t = threading.Thread(target=poll_reminders_for_notifications, daemon=True)
    t.start()

# Start notification polling on import (main app entry)
try:
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    start_reminder_notification_thread()
except Exception:
    pass
# --- Accessible File Manager UI for Mobile ---
def open_file_manager_ui():
    import tkinter as tk
    from tkinter import simpledialog, messagebox
    import sys
    sys.path.append("../src")
    import accessible_file_manager as afm
    import os
    win = tk.Toplevel()
    win.title("Accessible File Manager")
    win.geometry("400x540")
    win.configure(bg="#222")
    path_var = tk.StringVar(value=os.path.expanduser("~"))
    status_var = tk.StringVar()
    file_list = tk.Listbox(win, font=("Arial", 12), bg="#111", fg="#fff", width=32, height=16)
    file_list.pack(side="left", fill="y", padx=8, pady=8)
    def refresh():
        file_list.delete(0, tk.END)
        items = afm.list_dir(path_var.get())
        for i, item in enumerate(items):
            tag = "[DIR]" if item["is_dir"] else "     "
            file_list.insert(tk.END, f"{tag} {item['name']}")
        status_var.set(f"{len(items)} items in {path_var.get()}")
    def on_select(event=None):
        idx = file_list.curselection()
        if not idx:
            return
        items = afm.list_dir(path_var.get())
        item = items[idx[0]]
        if item["is_dir"]:
            path_var.set(item["path"])
            refresh()
        else:
            content = afm.read_file(item["path"])
            if content is not None:
                text.delete("1.0", tk.END)
                text.insert(tk.END, content)
            else:
                text.delete("1.0", tk.END)
                text.insert(tk.END, "[Could not read file]")
    def go_up():
        path = os.path.dirname(path_var.get())
        path_var.set(path)
        refresh()
    def delete_selected():
        idx = file_list.curselection()
        if not idx:
            status_var.set("Select a file/folder to delete.")
            return
        items = afm.list_dir(path_var.get())
        item = items[idx[0]]
        if item["is_dir"]:
            messagebox.showinfo("Delete", "Folder deletion not supported.")
            return
        if messagebox.askyesno("Delete", f"Delete {item['name']}?"):
            if afm.delete_file(item["path"]):
                status_var.set(f"Deleted {item['name']}.")
                refresh()
            else:
                status_var.set("Delete failed.")
    def rename_selected():
        idx = file_list.curselection()
        if not idx:
            status_var.set("Select a file/folder to rename.")
            return
        items = afm.list_dir(path_var.get())
        item = items[idx[0]]
        new_name = simpledialog.askstring("Rename", f"Rename {item['name']} to:")
        if new_name:
            result = afm.rename_file(item["path"], new_name)
            if result:
                status_var.set(f"Renamed to {new_name}.")
                refresh()
            else:
                status_var.set("Rename failed.")
    def read_aloud():
        idx = file_list.curselection()
        if not idx:
            status_var.set("Select a file to read aloud.")
            return
        items = afm.list_dir(path_var.get())
        item = items[idx[0]]
        if item["is_dir"]:
            status_var.set("Cannot read folders aloud.")
            return
        ok = afm.read_file_aloud(item["path"], platform="mobile")
        if ok:
            status_var.set(f"Reading {item['name']} aloud...")
        else:
            status_var.set("Could not read aloud.")
    # UI controls
    btn_frame = tk.Frame(win, bg="#222")
    btn_frame.pack(side="top", fill="x", padx=8, pady=2)
    tk.Button(btn_frame, text="Up", command=go_up, font=("Arial", 11), bg="#1976D2", fg="#fff").pack(side="left", padx=2)
    tk.Button(btn_frame, text="Delete", command=delete_selected, font=("Arial", 11), bg="#D32F2F", fg="#fff").pack(side="left", padx=2)
    tk.Button(btn_frame, text="Rename", command=rename_selected, font=("Arial", 11), bg="#FFD600", fg="#222").pack(side="left", padx=2)
    tk.Button(btn_frame, text="Read Aloud", command=read_aloud, font=("Arial", 11), bg="#43A047", fg="#fff").pack(side="left", padx=2)
    tk.Button(btn_frame, text="Close", command=win.destroy, font=("Arial", 11), bg="#888", fg="#fff").pack(side="right", padx=2)
    tk.Label(win, textvariable=status_var, font=("Arial", 11), bg="#222", fg="#FFD600").pack(pady=2)
    text = tk.Text(win, font=("Arial", 11), bg="#333", fg="#fff", width=32, height=16, wrap="word")
    text.pack(side="right", fill="both", expand=True, padx=8, pady=8)
    file_list.bind('<<ListboxSelect>>', on_select)
    refresh()

# Add File Manager to feature list
def add_file_manager_feature_button():
    global feature_buttons
    feature_buttons.append(("File Manager", "#388E3C", "Browse and manage files and folders.", open_file_manager_ui))

add_file_manager_feature_button()
# --- Minimal Reminders UI for Mobile ---
def open_reminders_ui():
    import tkinter as tk
    from tkinter import messagebox
    import datetime
    import sys
    sys.path.append("../src")
    import reminders as reminders_backend

    win = tk.Toplevel()
    win.title("Reminders & Alarms")
    win.geometry("400x500")
    win.configure(bg="#222")

    def refresh_list():
        reminder_list.delete(0, tk.END)
        all_reminders = reminders_backend.get_reminders(user="local")
        for r in all_reminders:
            dt = r["datetime"][:16].replace("T", " ")
            label = f"{r['title']} @ {dt}"
            reminder_list.insert(tk.END, label)
        return all_reminders

    def on_select(event=None):
        idx = reminder_list.curselection()
        if not idx:
            return
        idx = idx[0]
        all_reminders = reminders_backend.get_reminders(user="local")
        r = all_reminders[idx]
        title_var.set(r["title"])
        desc_var.set(r["description"])
        dt_var.set(r["datetime"][:16])
        recurrence_var.set(r.get("recurrence") or "None")
        selected_id.set(r["id"])

    def clear_fields():
        title_var.set("")
        desc_var.set("")
        dt_var.set("")
        recurrence_var.set("None")
        selected_id.set("")

    def add_reminder():
        title = title_var.get().strip()
        desc = desc_var.get().strip()
        dt = dt_var.get().strip()
        recurrence = recurrence_var.get()
        if not title or not dt:
            messagebox.showerror("Missing Info", "Title and Date/Time required.")
            return
        try:
            # Validate datetime
            datetime.datetime.fromisoformat(dt)
        except Exception:
            messagebox.showerror("Invalid Date", "Date/Time must be in YYYY-MM-DDTHH:MM format.")
            return
        reminders_backend.add_reminder("local", title, desc, dt, recurrence if recurrence != "None" else None)
        refresh_list()
        clear_fields()

    def update_reminder():
        rid = selected_id.get()
        if not rid:
            messagebox.showerror("No Selection", "Select a reminder to update.")
            return
        title = title_var.get().strip()
        desc = desc_var.get().strip()
        dt = dt_var.get().strip()
        recurrence = recurrence_var.get()
        if not title or not dt:
            messagebox.showerror("Missing Info", "Title and Date/Time required.")
            return
        try:
            datetime.datetime.fromisoformat(dt)
        except Exception:
            messagebox.showerror("Invalid Date", "Date/Time must be in YYYY-MM-DDTHH:MM format.")
            return
        reminders_backend.update_reminder(rid, title=title, description=desc, datetime=dt, recurrence=recurrence if recurrence != "None" else None)
        refresh_list()
        clear_fields()

    def delete_reminder():
        rid = selected_id.get()
        if not rid:
            messagebox.showerror("No Selection", "Select a reminder to delete.")
            return
        if messagebox.askyesno("Delete Reminder", "Are you sure?"):
            reminders_backend.delete_reminder(rid)
            refresh_list()
            clear_fields()

    # UI Layout
    tk.Label(win, text="Reminders & Alarms", font=("Arial", 15, "bold"), bg="#222", fg="#FFD600").pack(pady=8)
    reminder_list = tk.Listbox(win, font=("Arial", 12), width=38, height=10, bg="#111", fg="#fff")
    reminder_list.pack(pady=5)
    reminder_list.bind("<<ListboxSelect>>", on_select)

    # Fields
    title_var = tk.StringVar()
    desc_var = tk.StringVar()
    dt_var = tk.StringVar()
    recurrence_var = tk.StringVar(value="None")
    selected_id = tk.StringVar()

    tk.Label(win, text="Title:", bg="#222", fg="#FFD600").pack(anchor="w", padx=20)
    tk.Entry(win, textvariable=title_var, font=("Arial", 12), bg="#fff").pack(fill="x", padx=20)
    tk.Label(win, text="Description:", bg="#222", fg="#FFD600").pack(anchor="w", padx=20)
    tk.Entry(win, textvariable=desc_var, font=("Arial", 12), bg="#fff").pack(fill="x", padx=20)
    tk.Label(win, text="Date/Time (YYYY-MM-DDTHH:MM):", bg="#222", fg="#FFD600").pack(anchor="w", padx=20)
    tk.Entry(win, textvariable=dt_var, font=("Arial", 12), bg="#fff").pack(fill="x", padx=20)
    tk.Label(win, text="Recurrence:", bg="#222", fg="#FFD600").pack(anchor="w", padx=20)
    tk.OptionMenu(win, recurrence_var, "None", "daily", "weekly").pack(fill="x", padx=20)

    btn_frame = tk.Frame(win, bg="#222")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Add", command=add_reminder, font=("Arial", 12), bg="#43A047", fg="#fff", width=8).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Update", command=update_reminder, font=("Arial", 12), bg="#1976D2", fg="#fff", width=8).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Delete", command=delete_reminder, font=("Arial", 12), bg="#D32F2F", fg="#fff", width=8).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Clear", command=clear_fields, font=("Arial", 12), bg="#888", fg="#fff", width=8).pack(side="left", padx=5)
    tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#888", fg="#fff").pack(pady=8)

    refresh_list()

# --- Minimal Smart Home UI for Mobile ---
def open_smart_home_ui():
    import tkinter as tk
    from tkinter import messagebox
    import sys
    sys.path.append("../src")
    import smart_home as sh

    win = tk.Toplevel()
    win.title("Smart Home Control")
    win.geometry("430x540")
    win.configure(bg="#222")

    controller = getattr(open_smart_home_ui, "controller", None)
    if controller is None:
        controller = sh.SmartHomeController()
        open_smart_home_ui.controller = controller

    def discover():
        devices = controller.discover_devices()
        device_list.delete(0, tk.END)
        for d in devices:
            device_list.insert(tk.END, f"{d.name} ({d.device_type})")
        status_var.set("Discovered devices.")

    def on_select(event=None):
        idx = device_list.curselection()
        if not idx:
            clear_fields()
            return
        idx = idx[0]
        d = controller.get_devices()[idx]
        selected_name.set(d.name)
        type_var.set(d.device_type)
        status_var.set(f"{d.name} is {d.get_status()}")
        # TV controls
        if d.device_type == "smart_tv":
            tv_frame.pack(fill="x", padx=10, pady=5)
            vol_var.set(str(getattr(d, "volume", 10)))
            input_var.set(getattr(d, "input_source", "HDMI1"))
            app_var.set(getattr(d, "current_app", ""))
        else:
            tv_frame.pack_forget()

    def clear_fields():
        selected_name.set("")
        type_var.set("")
        vol_var.set("")
        input_var.set("")
        app_var.set("")
        status_var.set("")
        tv_frame.pack_forget()

    def do_on():
        name = selected_name.get()
        if not name:
            messagebox.showerror("No Device", "Select a device.")
            return
        controller.control_device(name, "on")
        status_var.set(f"{name} turned ON.")

    def do_off():
        name = selected_name.get()
        if not name:
            messagebox.showerror("No Device", "Select a device.")
            return
        controller.control_device(name, "off")
        status_var.set(f"{name} turned OFF.")

    def do_status():
        name = selected_name.get()
        if not name:
            messagebox.showerror("No Device", "Select a device.")
            return
        d = next((d for d in controller.get_devices() if d.name == name), None)
        if d:
            status_var.set(f"{name} is {d.get_status()}")
        else:
            status_var.set("Device not found.")

    # TV controls
    def set_volume():
        name = selected_name.get()
        try:
            value = int(vol_var.get())
        except Exception:
            messagebox.showerror("Invalid Volume", "Enter a number 0-100.")
            return
        controller.control_device(name, "set_volume", value=value)
        status_var.set(f"{name} volume set to {value}")

    def change_input():
        name = selected_name.get()
        source = input_var.get()
        controller.control_device(name, "change_input", source=source)
        status_var.set(f"{name} input set to {source}")

    def launch_app():
        name = selected_name.get()
        app = app_var.get()
        controller.control_device(name, "launch_app", app_name=app)
        status_var.set(f"{name} launched {app}")

    def play_content():
        name = selected_name.get()
        title = content_var.get()
        controller.control_device(name, "play_content", title=title)
        status_var.set(f"{name} playing '{title}'")

    # UI Layout
    tk.Label(win, text="Smart Home Device Control", font=("Arial", 15, "bold"), bg="#222", fg="#FFD600").pack(pady=8)
    device_list = tk.Listbox(win, font=("Arial", 12), width=38, height=8, bg="#111", fg="#fff")
    device_list.pack(pady=5)
    device_list.bind("<<ListboxSelect>>", on_select)

    btn_frame = tk.Frame(win, bg="#222")
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Discover Devices", command=discover, font=("Arial", 12), bg="#43A047", fg="#fff", width=15).pack(side="left", padx=5)
    tk.Button(btn_frame, text="On", command=do_on, font=("Arial", 12), bg="#1976D2", fg="#fff", width=7).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Off", command=do_off, font=("Arial", 12), bg="#D32F2F", fg="#fff", width=7).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Status", command=do_status, font=("Arial", 12), bg="#888", fg="#fff", width=8).pack(side="left", padx=5)

    # Device info/controls
    selected_name = tk.StringVar()
    type_var = tk.StringVar()
    status_var = tk.StringVar()
    tk.Label(win, textvariable=status_var, font=("Arial", 12), bg="#222", fg="#FFD600").pack(pady=2)

    # TV controls frame (hidden unless TV selected)
    tv_frame = tk.Frame(win, bg="#333")
    tk.Label(tv_frame, text="TV Controls", font=("Arial", 13, "bold"), bg="#333", fg="#FFD600").pack(pady=2)
    vol_var = tk.StringVar()
    tk.Label(tv_frame, text="Volume (0-100):", bg="#333", fg="#FFD600").pack(anchor="w", padx=10)
    tk.Entry(tv_frame, textvariable=vol_var, font=("Arial", 12), width=8).pack(padx=10)
    tk.Button(tv_frame, text="Set Volume", command=set_volume, font=("Arial", 11), bg="#1976D2", fg="#fff").pack(padx=10, pady=2)
    input_var = tk.StringVar()
    tk.Label(tv_frame, text="Input Source:", bg="#333", fg="#FFD600").pack(anchor="w", padx=10)
    tk.Entry(tv_frame, textvariable=input_var, font=("Arial", 12), width=10).pack(padx=10)
    tk.Button(tv_frame, text="Change Input", command=change_input, font=("Arial", 11), bg="#1976D2", fg="#fff").pack(padx=10, pady=2)
    app_var = tk.StringVar()
    tk.Label(tv_frame, text="App:", bg="#333", fg="#FFD600").pack(anchor="w", padx=10)
    tk.Entry(tv_frame, textvariable=app_var, font=("Arial", 12), width=12).pack(padx=10)
    tk.Button(tv_frame, text="Launch App", command=launch_app, font=("Arial", 11), bg="#1976D2", fg="#fff").pack(padx=10, pady=2)
    content_var = tk.StringVar()
    tk.Label(tv_frame, text="Play Content:", bg="#333", fg="#FFD600").pack(anchor="w", padx=10)
    tk.Entry(tv_frame, textvariable=content_var, font=("Arial", 12), width=18).pack(padx=10)
    tk.Button(tv_frame, text="Play", command=play_content, font=("Arial", 11), bg="#43A047", fg="#fff").pack(padx=10, pady=2)

    # Hide TV controls by default
    tv_frame.pack_forget()

    tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#888", fg="#fff").pack(pady=8)

    discover()
# --- Second User Mode logic ---
SECOND_USER_MODE = False

def activate_second_user_mode():
    global SECOND_USER_MODE
    SECOND_USER_MODE = True
    try:
        import tkinter.messagebox as messagebox
        messagebox.showinfo("Second User Mode", "Second User Mode activated. All features are disabled.")
    except Exception:
        pass

def deactivate_second_user_mode():
    global SECOND_USER_MODE
    SECOND_USER_MODE = False
    try:
        import tkinter.messagebox as messagebox
        messagebox.showinfo("Second User Mode", "Second User Mode deactivated. Full features restored.")
    except Exception:
        pass

def is_feature_allowed():
    return not SECOND_USER_MODE

def is_screen_reader_allowed():
    return not SECOND_USER_MODE

# --- 14-day free trial logic (MOBILE DEMO) ---
import datetime
TRIAL_DAYS = 14

def get_trial_status():
    # For demo: store trial_start in a local file. In production, use account backend.
    import os, json
    trial_file = "trial_status.json"
    if os.path.exists(trial_file):
        with open(trial_file, "r") as f:
            data = json.load(f)
    else:
        data = {}
    trial_start = data.get("trial_start")
    purchased = data.get("purchased", False)
    if purchased:
        return ("full", 0)
    if not trial_start:
        trial_start = datetime.datetime.now().isoformat()
        data["trial_start"] = trial_start
        with open(trial_file, "w") as f:
            json.dump(data, f)
    start = datetime.datetime.fromisoformat(trial_start)
    days_used = (datetime.datetime.now() - start).days
    days_left = max(0, TRIAL_DAYS - days_used)
    if days_left > 0:
        return ("trial", days_left)
    return ("expired", 0)

def is_trial_active():
    status, days = get_trial_status()
    return status == "trial"

def is_full_or_trial():
    status, days = get_trial_status()
    return status in ("full", "trial")

# GUI module for Talkback Assistant

import tkinter as tk
from tkinter import ttk
from accessibility import enable_accessibility
import speech
from speech import select_microphone_gui, speak, say_time, say_date, say_weather
from help_sheet import get_help_sheet


THEMES = {
    "Dark": {"bg": "#222", "fg": "#fff", "btn_bg": "#333", "btn_fg": "#FFD600"},
    "Light": {"bg": "#fff", "fg": "#222", "btn_bg": "#eee", "btn_fg": "#222"},
    "Blue": {"bg": "#1976D2", "fg": "#fff", "btn_bg": "#2196F3", "btn_fg": "#FFD600"}
}
current_theme = tk.StringVar(value="Dark")
accessibility_enabled = True  # Boolean flag to control accessibility features

# --- New Feature UIs for Mobile ---
def open_translation_ui():
    import tkinter as tk
    import sys
    sys.path.append("../src")
    import translation
    win = tk.Toplevel()
    win.title("Translation")
    win.geometry("400x320")
    win.configure(bg="#222")
    tk.Label(win, text="Enter text to translate:", font=("Arial", 13), bg="#222", fg="#FFD600").pack(pady=8)
    input_var = tk.StringVar()
    tk.Entry(win, textvariable=input_var, font=("Arial", 12), width=30).pack(pady=4)
    lang_var = tk.StringVar(value="es")
    tk.Label(win, text="Target Language (e.g. es, fr, de):", font=("Arial", 11), bg="#222", fg="#FFD600").pack(pady=2)
    tk.Entry(win, textvariable=lang_var, font=("Arial", 12), width=8).pack(pady=2)
    result_var = tk.StringVar()
    def do_translate():
        text = input_var.get()
        lang = lang_var.get()
        try:
            translated = translation.translate_text(text, lang)
            result_var.set(translated)
        except Exception as e:
            result_var.set(f"Error: {e}")
    tk.Button(win, text="Translate", command=do_translate, font=("Arial", 12), bg="#43A047", fg="#fff").pack(pady=6)
    tk.Label(win, textvariable=result_var, font=("Arial", 12), bg="#222", fg="#FFD600", wraplength=350).pack(pady=6)
    tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#888", fg="#fff").pack(pady=8)

def open_health_ui():
    import tkinter as tk
    import sys
    sys.path.append("../src")
    import health
    win = tk.Toplevel()
    win.title("Health & Fitness")
    win.geometry("400x320")
    win.configure(bg="#222")
    tk.Label(win, text="Health & Fitness", font=("Arial", 15, "bold"), bg="#222", fg="#FFD600").pack(pady=8)
    tips = health.get_health_tips()
    tips_str = "\n".join(tips) if tips else "No tips available."
    tk.Label(win, text=tips_str, font=("Arial", 12), bg="#222", fg="#fff", wraplength=350).pack(pady=6)
    tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#888", fg="#fff").pack(pady=8)

def open_security_ui():
    import tkinter as tk
    import sys
    sys.path.append("../src")
    import security
    win = tk.Toplevel()
    win.title("Security")
    win.geometry("400x320")
    win.configure(bg="#222")
    tk.Label(win, text="Security Status", font=("Arial", 15, "bold"), bg="#222", fg="#FFD600").pack(pady=8)
    status = security.get_security_status()
    tk.Label(win, text=status, font=("Arial", 12), bg="#222", fg="#fff", wraplength=350).pack(pady=6)
    tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#888", fg="#fff").pack(pady=8)

def open_notes_ui():
    import tkinter as tk
    import sys
    sys.path.append("../src")
    import notes
    win = tk.Toplevel()
    win.title("Notes & To-Do")
    win.geometry("400x400")
    win.configure(bg="#222")
    tk.Label(win, text="Notes & To-Do", font=("Arial", 15, "bold"), bg="#222", fg="#FFD600").pack(pady=8)
    notes_var = tk.StringVar(value="\n".join(notes.get_notes()))
    notes_box = tk.Text(win, font=("Arial", 12), bg="#333", fg="#fff", width=36, height=10)
    notes_box.pack(pady=6)
    notes_box.insert("1.0", notes_var.get())
    def save_notes():
        content = notes_box.get("1.0", tk.END).strip()
        notes.save_notes(content)
        notes_var.set(content)
    tk.Button(win, text="Save", command=save_notes, font=("Arial", 12), bg="#43A047", fg="#fff").pack(pady=4)
    tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#888", fg="#fff").pack(pady=8)

def open_location_ui():
    import tkinter as tk
    import sys
    sys.path.append("../src")
    import location
    win = tk.Toplevel()
    win.title("Location Services")
    win.geometry("400x320")
    win.configure(bg="#222")
    tk.Label(win, text="Location Services", font=("Arial", 15, "bold"), bg="#222", fg="#FFD600").pack(pady=8)
    loc_var = tk.StringVar()
    def get_loc():
        try:
            loc = location.get_location()
            loc_var.set(loc)
        except Exception as e:
            loc_var.set(f"Error: {e}")
    tk.Button(win, text="Get Location", command=get_loc, font=("Arial", 12), bg="#43A047", fg="#fff").pack(pady=6)
    tk.Label(win, textvariable=loc_var, font=("Arial", 12), bg="#222", fg="#FFD600", wraplength=350).pack(pady=6)
    tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#888", fg="#fff").pack(pady=8)

def launch(gui_instance):
    global accessibility_enabled
    # Set accessibility flag based on your requirements
    # accessibility_enabled = False  # Uncomment to disable accessibility

    # If you have a settings object, you can use it here
    # settings = ... (define or import settings if needed)
    # accessibility_enabled = False
    # if settings and settings.get("accessibility"):
    #     accessibility_enabled = True

    # Condition to enable accessibility, can be based on settings or other logic
    # condition = True  # Replace with actual condition
    # if condition:
    #     accessibility_enabled = True

    root = tk.Tk()
    root.title("Talkback Assistant")
    root.geometry("1000x800")
    root.configure(bg="#222")

    canvas = tk.Canvas(root, bg="#222", highlightthickness=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#222")
    canvas.create_window((0,0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    content_var = tk.StringVar(value="Welcome to Talkback Assistant!")
    content_label = tk.Label(scroll_frame, textvariable=content_var, font=("Arial", 16), bg="#222", fg="#fff", wraplength=900)
    content_label.grid(row=0, column=0, columnspan=3, pady=10)

    mic_names = speech.list_microphones()
    mic_var = tk.StringVar(value=mic_names[0] if mic_names else "")
    def set_mic(event=None):
        idx = mic_names.index(mic_var.get()) if mic_var.get() in mic_names else None
        speech.selected_mic_index = idx
        content_var.set(f"Microphone selected: {mic_var.get()} (index {idx})")
    mic_label = tk.Label(scroll_frame, text="Select Microphone:", font=("Arial", 16), bg="#222", fg="#FFD600")
    mic_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    mic_combo = ttk.Combobox(scroll_frame, textvariable=mic_var, values=mic_names, font=("Arial", 16), width=30)
    mic_combo.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    mic_combo.bind("<<ComboboxSelected>>", set_mic)
    enable_accessibility(mic_combo, tooltip="Choose which microphone to use for speech input.")

    def open_email_ui():
        import tkinter as tk
        from email_integration import list_emails, read_email
        email_win = tk.Toplevel(root)
        email_win.title("Email Management")
        email_win.geometry("600x400")
        email_win.configure(bg="#222")
        tk.Label(email_win, text="Inbox:", font=("Arial", 16), bg="#222", fg="#FFD600").pack(pady=10)
        listbox = tk.Listbox(email_win, font=("Arial", 13), width=60, height=12, bg="#111", fg="#fff")
        listbox.pack(pady=5)
        status_var = tk.StringVar(value="Select an email to read.")
        tk.Label(email_win, textvariable=status_var, font=("Arial", 12), bg="#222", fg="#FFD600").pack(pady=5)
        def refresh_inbox():
            listbox.delete(0, tk.END)
            try:
                emails = list_emails()
                for idx, mail in enumerate(emails):
                    listbox.insert(tk.END, f"{idx+1}. {mail['subject']} - {mail['from']}")
                status_var.set(f"Loaded {len(emails)} emails.")
            except Exception as e:
                status_var.set(f"Failed to load inbox: {e}")
        def on_select(event=None):
            sel = listbox.curselection()
            if not sel:
                return
            idx = sel[0]
            try:
                emails = list_emails()
                mail = emails[idx]
                content = read_email(mail['id'])
                top = tk.Toplevel(email_win)
                top.title(mail['subject'])
                top.geometry("500x300")
                top.configure(bg="#222")
                tk.Label(top, text=mail['subject'], font=("Arial", 14, "bold"), bg="#222", fg="#FFD600").pack(pady=5)
                text = tk.Text(top, font=("Arial", 12), bg="#111", fg="#fff", wrap="word")
                text.insert(tk.END, content)
                text.config(state="disabled")
                text.pack(expand=True, fill="both", padx=10, pady=10)
            except Exception as e:
                status_var.set(f"Failed to read email: {e}")
        listbox.bind("<<ListboxSelect>>", on_select)
        tk.Button(email_win, text="Refresh Inbox", command=refresh_inbox, font=("Arial", 12), bg="#4FC3F7", fg="#222").pack(pady=10)
        tk.Button(email_win, text="Close", command=email_win.destroy, font=("Arial", 12), bg="#D32F2F", fg="#fff").pack(pady=5)
        refresh_inbox()

    feature_buttons = [
    ("Screen Reader ON/OFF", "#455A64", "Toggle screen reader feature.", lambda: None),
    ("Settings", "#4FC3F7", "Open app settings.", lambda: None),
    ("Help", "#FFD600", "Show help sheet and speak instructions.", lambda: (content_var.set(get_help_sheet()), speak(get_help_sheet()))),
    ("Say Time", "#4CAF50", "Speak the current time.", say_time),
    ("Say Date", "#009688", "Speak today's date.", say_date),
    ("Say Weather", "#1976D2", "Speak the weather.", say_weather),
    ("Reminders & Alarms", "#FFB300", "Set reminders and alarms.", lambda: open_reminders_ui() if 'open_reminders_ui' in globals() else content_var.set("Reminders feature coming soon.")),
    ("Calendar", "#7CB342", "View and sync calendar.", lambda: content_var.set("Calendar feature coming soon.")),
    ("Email", "#E91E63", "Send and receive emails.", open_email_ui),
    ("Smart Home", "#8BC34A", "Control smart home devices.", lambda: open_smart_home_ui() if 'open_smart_home_ui' in globals() else content_var.set("Smart Home feature coming soon.")),
    ("File Manager", "#388E3C", "Manage your files.", lambda: content_var.set("File Manager feature coming soon.")),
    ("Media", "#7E57C2", "Play and manage media.", lambda: open_media_ui()),
    ("Translation", "#3949AB", "Translate text to another language.", open_translation_ui),
    ("Health & Fitness", "#D32F2F", "View health tips and activity.", open_health_ui),
    ("Security", "#E53935", "Check security status and features.", open_security_ui),
    ("Notes & To-Do", "#FFB300", "Take notes and manage to-dos.", open_notes_ui),
    ("Location Services", "#0097A7", "Get your current location.", open_location_ui),
    ]

# (Removed duplicate/redefining feature_buttons here to avoid NameError for content_var)

# --- Media Playback UI for Mobile ---
def open_media_ui():
    import tkinter as tk
    from tkinter import filedialog, messagebox
    import sys
    sys.path.append("../src")
    import media
    win = tk.Toplevel()
    win.title("Media Player")
    win.geometry("400x320")
    win.configure(bg="#222")
    status_var = tk.StringVar(value="Select a file to play.")
    file_var = tk.StringVar()
    def select_file():
        f = filedialog.askopenfilename(filetypes=[("Audio Files", ".wav .mp3 .ogg .flac"), ("All Files", ".*")])
        if f:
            file_var.set(f)
            status_var.set(f"Selected: {f}")
    def play():
        f = file_var.get()
        if not f:
            status_var.set("No file selected.")
            return
        result = media.play_media(f)
        status_var.set(result)
    def pause():
        status_var.set(media.pause_media())
    def resume():
        status_var.set(media.resume_media())
    def stop():
        status_var.set(media.stop_media())
    def seek():
        try:
            sec = int(seek_entry.get())
        except Exception:
            status_var.set("Enter seconds to seek.")
            return
        status_var.set(media.seek_media(sec))
    def set_vol():
        try:
            v = float(vol_entry.get())
            if v > 1: v = v/100
        except Exception:
            status_var.set("Enter 0-1 or 0-100.")
            return
        status_var.set(media.set_media_volume(v))
    tk.Label(win, text="Media Player", font=("Arial", 15, "bold"), bg="#222", fg="#FFD600").pack(pady=8)
    tk.Button(win, text="Select File", command=select_file, font=("Arial", 12), bg="#4FC3F7", fg="#222").pack(pady=4)
    tk.Label(win, textvariable=file_var, font=("Arial", 10), bg="#222", fg="#fff").pack(pady=2)
    btn_frame = tk.Frame(win, bg="#222")
    btn_frame.pack(pady=6)
    tk.Button(btn_frame, text="Play", command=play, font=("Arial", 12), bg="#43A047", fg="#fff", width=7).pack(side="left", padx=2)
    tk.Button(btn_frame, text="Pause", command=pause, font=("Arial", 12), bg="#FFD600", fg="#222", width=7).pack(side="left", padx=2)
    tk.Button(btn_frame, text="Resume", command=resume, font=("Arial", 12), bg="#1976D2", fg="#fff", width=7).pack(side="left", padx=2)
    tk.Button(btn_frame, text="Stop", command=stop, font=("Arial", 12), bg="#D32F2F", fg="#fff", width=7).pack(side="left", padx=2)
    seek_frame = tk.Frame(win, bg="#222")
    seek_frame.pack(pady=4)
    tk.Label(seek_frame, text="Seek (s):", font=("Arial", 11), bg="#222", fg="#FFD600").pack(side="left")
    seek_entry = tk.Entry(seek_frame, width=6, font=("Arial", 11))
    seek_entry.pack(side="left", padx=2)
    tk.Button(seek_frame, text="Go", command=seek, font=("Arial", 11), bg="#4FC3F7", fg="#222").pack(side="left", padx=2)
    vol_frame = tk.Frame(win, bg="#222")
    vol_frame.pack(pady=4)
    tk.Label(vol_frame, text="Volume (0-1 or 0-100):", font=("Arial", 11), bg="#222", fg="#FFD600").pack(side="left")
    vol_entry = tk.Entry(vol_frame, width=6, font=("Arial", 11))
    vol_entry.pack(side="left", padx=2)
    tk.Button(vol_frame, text="Set", command=set_vol, font=("Arial", 11), bg="#FFD600", fg="#222").pack(side="left", padx=2)
    tk.Label(win, textvariable=status_var, font=("Arial", 11), bg="#222", fg="#FFD600").pack(pady=6)
    tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#888", fg="#fff").pack(pady=8)

    # Theme selection UI is not needed in the media player window, so it is omitted here.

    def test_microphone():
        import speech_recognition as sr
        import pygame
        import tempfile, os
        recognizer = sr.Recognizer()
        mic_index = speech.selected_mic_index
        if mic_index is None:
            source = sr.Microphone()
        else:
            source = sr.Microphone(device_index=mic_index)
        with source as src:
            status_var.set("Recording... Please speak.")
            try:
                audio = recognizer.listen(src, timeout=5)
                status_var.set("Playing back your recording...")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tf:
                    temp_filename = tf.name
                with open(temp_filename, "wb") as f:
                    f.write(audio.get_wav_data())
                pygame.mixer.init()
                pygame.mixer.music.load(temp_filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.music.unload()
                try:
                    os.remove(temp_filename)
                except PermissionError:
                    status_var.set("Mic test complete, but could not delete temp file (access denied).")
                    return
                status_var.set("Mic test complete.")
            except Exception as e:
                status_var.set(f"Mic test failed: {e}")

    feature_buttons.insert(0, ("Test Microphone", "#FF9800", "Record and play back your voice to test the mic.", test_microphone))

    def make_on_enter(tip, widget):
        def on_enter(event):
            text = tip or widget.cget('text')
            try:
                speak(text)
            except Exception:
                pass
        return on_enter

    # Use a local frame for media player feature buttons
    media_frame = tk.Frame(win, bg="#222")
    media_frame.pack(pady=10)
    buttons = []
    for i, (label, color, tooltip, cmd) in enumerate(feature_buttons):
        btn = tk.Button(media_frame, text=label, command=cmd, font=("Arial", 18), bg=color, fg="white", width=22, height=2)
        btn.grid(row=i // 3, column=i % 3, padx=10, pady=10)
        enable_accessibility(btn, tooltip=tooltip)
        btn.bind('<Enter>', make_on_enter(tooltip, btn))
        buttons.append(btn)

    # If in Second User Mode, disable all feature buttons
    if SECOND_USER_MODE:
        for btn in buttons:
            btn.configure(state="disabled")

    # Show trial status in UI
    trial_status, trial_days = get_trial_status()
    if trial_status == "full":
        trial_msg = "Full Version Unlocked!"
    elif trial_status == "trial":
        trial_msg = f"Trial: {trial_days} days left"
    else:
        trial_msg = "Trial expired. Please purchase to unlock."
    trial_label = tk.Label(media_frame, text=trial_msg, font=("Arial", 14), bg="#222", fg="#FFD600")
    trial_label.grid(row=10, column=0, columnspan=3, padx=10, pady=10, sticky="w")

    # Block premium features after trial expires
    if not is_full_or_trial():
        for btn in buttons:
            if btn['text'] not in ("Settings", "Help", "Test Microphone"):
                btn.configure(state="disabled")

    # Settings access: require owner approval if in Second User Mode
    def open_settings():
        if SECOND_USER_MODE:
            import tkinter.messagebox as messagebox
            allow = messagebox.askyesno("Owner Permission Required", "Second User is requesting access to Settings. Allow?")
            if not allow:
                messagebox.showinfo("Access Denied", "Settings access denied by device owner.")
                return
        # ...existing settings logic here...

    # Show Second User Mode status and allow owner to exit it
    if SECOND_USER_MODE:
        status_frame = tk.Frame(win, bg="#222")
        status_frame.pack(pady=10)
        tk.Label(status_frame, text="Second User Mode is ACTIVE", font=("Arial", 13, "bold"), bg="#222", fg="#FFD600").pack(side="left", padx=5)
        def exit_second_user():
            global SECOND_USER_MODE
            SECOND_USER_MODE = False
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Second User Mode", "Second User Mode has been turned off.")
            win.destroy()
        tk.Button(status_frame, text="Exit Second User Mode", command=exit_second_user, font=("Arial", 12), bg="#43A047", fg="#fff").pack(side="left", padx=10)

    root.mainloop()

accessibility_enabled = True   # global
# accessibility_enabled is set above as a global variable

if __name__ == "__main__":
    launch(None)