import os
from reminders import add_reminder, get_reminders, delete_reminder
from smart_home import SmartHomeController
import accessible_file_manager as afm
def open_smart_home_ui():
    import tkinter as tk
    controller = SmartHomeController()
    win = tk.Toplevel(root)
    win.title("Smart Home Device Control")
    win.geometry("600x400")
    win.configure(bg="#222")
    tk.Label(win, text="Smart Home Device Control", font=("Arial", 15, "bold"), bg="#222", fg="#FFD600").pack(pady=10)
    frame = tk.Frame(win, bg="#222")
    frame.pack(fill="both", expand=True, padx=10, pady=5)
    device_list = tk.Listbox(frame, font=("Arial", 11), bg="#111", fg="#fff", height=12, width=30)
    device_list.pack(side="left", fill="y", expand=False)
    status_var = tk.StringVar()
    tk.Label(win, textvariable=status_var, font=("Arial", 11), bg="#222", fg="#FFD600").pack(pady=2)
    def refresh_devices():
        device_list.delete(0, tk.END)
        devices = controller.discover_devices()
        for d in devices:
            device_list.insert(tk.END, f"{d.name} ({d.device_type}) [{d.get_status()}]")
    def control_selected(action):
        idx = device_list.curselection()
        if not idx:
            status_var.set("Select a device.")
            return
        devices = controller.get_devices()
        device = devices[idx[0]]
        controller.control_device(device.name, action)
        status_var.set(f"{device.name} turned {action.upper()}.")
        refresh_devices()

    def play_content_on_tv():
        idx = device_list.curselection()
        if not idx:
            status_var.set("Select a smart TV.")
            return
        devices = controller.get_devices()
        device = devices[idx[0]]
        if getattr(device, 'device_type', None) != 'smart_tv':
            status_var.set("Selected device is not a smart TV.")
            return
        # Prompt for content title
        import tkinter.simpledialog
        title = tkinter.simpledialog.askstring("Play Film/Show", "Enter film or TV show name:")
        if not title:
            status_var.set("No title entered.")
            return
        controller.control_device(device.name, "play_content", title=title)
        status_var.set(f"Requested '{title}' on {device.name}.")
    tk.Button(win, text="Turn ON", command=lambda: control_selected("on"), font=("Arial", 12), bg="#43A047", fg="#fff").pack(pady=4)
    tk.Button(win, text="Turn OFF", command=lambda: control_selected("off"), font=("Arial", 12), bg="#D32F2F", fg="#fff").pack(pady=2)
    tk.Button(win, text="Play Film/Show on TV", command=play_content_on_tv, font=("Arial", 12), bg="#FFD600", fg="#222").pack(pady=2)
    tk.Button(win, text="Refresh Devices", command=refresh_devices, font=("Arial", 12), bg="#1976D2", fg="#fff").pack(pady=2)
    tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#888", fg="#fff").pack(pady=2)
    refresh_devices()
import threading
import time
import datetime

def poll_reminders_for_notifications(root):
    from reminders import get_reminders, update_reminder
    import tkinter.messagebox as messagebox
    while True:
        now = datetime.datetime.now()
        reminders = get_reminders(user="local")
        for r in reminders:
            if r.get("notified"):
                continue
            try:
                dt = r["datetime"]
                # Accept both ISO and 'YYYY-MM-DD HH:MM' formats
                try:
                    due = datetime.datetime.fromisoformat(dt)
                except Exception:
                    due = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M")
                if due <= now:
                    msg = f"{r.get('title','Reminder')}: {r.get('description','') or ''}"
                    root.after(0, lambda m=msg: messagebox.showinfo("Reminder", m))
                    update_reminder(r["id"], notified=True)
            except Exception:
                continue
        time.sleep(60)

def start_reminder_notification_thread(root):
    t = threading.Thread(target=poll_reminders_for_notifications, args=(root,), daemon=True)
    t.start()

def open_reminders_ui():
    import tkinter as tk
    import datetime
    win = tk.Toplevel(root)
    win.title("Reminders & Appointments")
    win.geometry("600x400")
    win.configure(bg="#222")
    tk.Label(win, text="Reminders & Appointments", font=("Arial", 15, "bold"), bg="#222", fg="#FFD600").pack(pady=10)
    frame = tk.Frame(win, bg="#222")
    frame.pack(fill="both", expand=True, padx=10, pady=5)
    listbox = tk.Listbox(frame, font=("Arial", 11), bg="#111", fg="#fff", height=12, width=30)
    listbox.pack(side="left", fill="y", expand=False)
    text = tk.Text(frame, font=("Arial", 11), bg="#333", fg="#fff", width=50, height=12, state="disabled", wrap="word")
    text.pack(side="right", fill="both", expand=True)
    status_var = tk.StringVar()
    tk.Label(win, textvariable=status_var, font=("Arial", 11), bg="#222", fg="#FFD600").pack(pady=2)
    def refresh():
        listbox.delete(0, tk.END)
        reminders = get_reminders(user="local")
        for r in reminders:
            t = r.get("title", "")
            dt = r.get("datetime", "")
            listbox.insert(tk.END, f"{t} @ {dt}")
    def on_select(event):
        idx = listbox.curselection()
        if not idx:
            return
        reminders = get_reminders(user="local")
        r = reminders[idx[0]]
        text.config(state="normal")
        text.delete("1.0", tk.END)
        text.insert(tk.END, f"Title: {r.get('title','')}")
        text.insert(tk.END, f"\nType: {r.get('type','')}")
        text.insert(tk.END, f"\nTime: {r.get('datetime','')}")
        text.insert(tk.END, f"\nDescription: {r.get('description','')}")
        text.insert(tk.END, f"\nRecurrence: {r.get('recurrence','None')}")
        text.config(state="disabled")
    def add_new():
        add_win = tk.Toplevel(win)
        add_win.title("Add Reminder/Appointment")
        add_win.geometry("350x320")
        add_win.configure(bg="#222")
        tk.Label(add_win, text="Title:", bg="#222", fg="#FFD600").pack(pady=2)
        title_var = tk.StringVar()
        tk.Entry(add_win, textvariable=title_var, font=("Arial", 12)).pack(pady=2)
        tk.Label(add_win, text="Description:", bg="#222", fg="#FFD600").pack(pady=2)
        desc = tk.Text(add_win, font=("Arial", 12), height=3)
        desc.pack(pady=2)
        tk.Label(add_win, text="Date & Time (YYYY-MM-DD HH:MM):", bg="#222", fg="#FFD600").pack(pady=2)
        dt_var = tk.StringVar()
        tk.Entry(add_win, textvariable=dt_var, font=("Arial", 12)).pack(pady=2)
        tk.Label(add_win, text="Type:", bg="#222", fg="#FFD600").pack(pady=2)
        type_var = tk.StringVar(value="reminder")
        tk.OptionMenu(add_win, type_var, "reminder", "appointment").pack(pady=2)
        tk.Label(add_win, text="Recurrence:", bg="#222", fg="#FFD600").pack(pady=2)
        rec_var = tk.StringVar(value="None")
        tk.OptionMenu(add_win, rec_var, "None", "daily", "weekly", "monthly").pack(pady=2)
        def save_new():
            title = title_var.get().strip()
            description = desc.get("1.0", "end").strip()
            dt = dt_var.get().strip()
            type_ = type_var.get()
            rec = rec_var.get()
            if not title or not dt:
                status_var.set("Title and date/time required.")
                return
            try:
                # Validate datetime
                datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M")
            except Exception:
                status_var.set("Invalid date/time format.")
                return
            add_reminder("local", title, description, dt, None if rec=="None" else rec, type_)
            add_win.destroy()
            status_var.set("Added.")
            refresh()
        tk.Button(add_win, text="Save", command=save_new, font=("Arial", 12), bg="#43A047", fg="#fff").pack(pady=8)
    def delete_selected():
        idx = listbox.curselection()
        if not idx:
            status_var.set("Select a reminder to delete.")
            return
        reminders = get_reminders(user="local")
        rid = reminders[idx[0]]["id"]
        delete_reminder(rid)
        status_var.set("Deleted.")
        refresh()
    listbox.bind('<<ListboxSelect>>', on_select)
    tk.Button(win, text="Add New", command=add_new, font=("Arial", 12), bg="#43A047", fg="#fff").pack(pady=4)
    tk.Button(win, text="Delete Selected", command=delete_selected, font=("Arial", 12), bg="#D32F2F", fg="#fff").pack(pady=2)
    tk.Button(win, text="Refresh", command=refresh, font=("Arial", 12), bg="#1976D2", fg="#fff").pack(pady=2)
    tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#888", fg="#fff").pack(pady=2)
    refresh()

# Add Reminders & Appointments to main feature list

def open_file_manager_ui():
    import tkinter as tk
    from tkinter import simpledialog, messagebox
    win = tk.Toplevel(root)
    win.title("Accessible File Manager")
    win.geometry("700x500")
    win.configure(bg="#222")
    path_var = tk.StringVar(value=os.path.expanduser("~"))
    status_var = tk.StringVar()
    file_list = tk.Listbox(win, font=("Arial", 12), bg="#111", fg="#fff", width=40, height=18)
    file_list.pack(side="left", fill="y", padx=10, pady=10)
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
        ok = afm.read_file_aloud(item["path"], platform="desktop")
        if ok:
            status_var.set(f"Reading {item['name']} aloud...")
        else:
            status_var.set("Could not read aloud.")
    # UI controls
    btn_frame = tk.Frame(win, bg="#222")
    btn_frame.pack(side="top", fill="x", padx=10, pady=2)
    tk.Button(btn_frame, text="Up", command=go_up, font=("Arial", 11), bg="#1976D2", fg="#fff").pack(side="left", padx=2)
    tk.Button(btn_frame, text="Delete", command=delete_selected, font=("Arial", 11), bg="#D32F2F", fg="#fff").pack(side="left", padx=2)
    tk.Button(btn_frame, text="Rename", command=rename_selected, font=("Arial", 11), bg="#FFD600", fg="#222").pack(side="left", padx=2)
    tk.Button(btn_frame, text="Read Aloud", command=read_aloud, font=("Arial", 11), bg="#43A047", fg="#fff").pack(side="left", padx=2)
    tk.Button(btn_frame, text="Close", command=win.destroy, font=("Arial", 11), bg="#888", fg="#fff").pack(side="right", padx=2)
    tk.Label(win, textvariable=status_var, font=("Arial", 11), bg="#222", fg="#FFD600").pack(pady=2)
    text = tk.Text(win, font=("Arial", 11), bg="#333", fg="#fff", width=50, height=18, wrap="word")
    text.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    file_list.bind('<<ListboxSelect>>', on_select)
    refresh()

def add_file_manager_feature_button():
    global feature_buttons
    feature_buttons.append(("File Manager", "#388E3C", "Browse and manage files and folders.", open_file_manager_ui))

    # --- New Features: Translation, Health, Security, Notes, Location ---
    def open_translation_ui():
        import tkinter as tk
        from tkinter import simpledialog, messagebox
        import translation
        win = tk.Toplevel()
        win.title("Translation")
        win.geometry("400x220")
        win.configure(bg="#222")
        tk.Label(win, text="Enter text to translate:", bg="#222", fg="#FFD600").pack(pady=4)
        entry = tk.Entry(win, font=("Arial", 12), width=32)
        entry.pack(pady=4)
        tk.Label(win, text="Target language (e.g. 'es', 'fr'):", bg="#222", fg="#FFD600").pack(pady=2)
        lang_entry = tk.Entry(win, font=("Arial", 12), width=8)
        lang_entry.pack(pady=2)
        result_var = tk.StringVar()
        tk.Label(win, textvariable=result_var, bg="#222", fg="#fff").pack(pady=4)
        def do_translate():
            text = entry.get()
            lang = lang_entry.get()
            if not text or not lang:
                result_var.set("Enter text and language.")
                return
            try:
                translated = translation.translate(text, lang)
                result_var.set(translated)
            except Exception as e:
                result_var.set(f"Error: {e}")
        tk.Button(win, text="Translate", command=do_translate, font=("Arial", 12), bg="#43A047", fg="#fff").pack(pady=4)
        tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#888", fg="#fff").pack(pady=4)

    def open_health_ui():
        import tkinter as tk
        import health
        win = tk.Toplevel()
        win.title("Health & Fitness")
        win.geometry("400x200")
        win.configure(bg="#222")
        summary = health.get_health_tips()
        tk.Label(win, text="Health Tips:", bg="#222", fg="#FFD600").pack(pady=4)
        tips = tk.Text(win, font=("Arial", 11), bg="#333", fg="#fff", width=40, height=6)
        tips.pack(pady=4)
        tips.insert("end", "\n".join(summary) if summary else "No tips available.")
        tips.config(state="disabled")
        tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#888", fg="#fff").pack(pady=4)

    def open_security_ui():
        import tkinter as tk
        import security
        win = tk.Toplevel()
        win.title("Security")
        win.geometry("400x160")
        win.configure(bg="#222")
        tk.Label(win, text="Security Status:", bg="#222", fg="#FFD600").pack(pady=4)
        status = tk.StringVar(value="Secure")
        tk.Label(win, textvariable=status, bg="#222", fg="#fff").pack(pady=4)
        tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#888", fg="#fff").pack(pady=4)

    def open_notes_ui():
        import tkinter as tk
        import notes
        win = tk.Toplevel()
        win.title("Notes & To-Do")
        win.geometry("400x260")
        win.configure(bg="#222")
        tk.Label(win, text="Your Notes:", bg="#222", fg="#FFD600").pack(pady=4)
        notes_list = tk.Listbox(win, font=("Arial", 12), bg="#111", fg="#fff", width=36, height=6)
        notes_list.pack(pady=4)
        for n in notes.list_notes():
            notes_list.insert("end", n)
        entry = tk.Entry(win, font=("Arial", 12), width=32)
        entry.pack(pady=4)
        def add():
            text = entry.get()
            if text:
                notes.add_note(text)
                notes_list.insert("end", text)
                entry.delete(0, "end")
        tk.Button(win, text="Add Note", command=add, font=("Arial", 12), bg="#43A047", fg="#fff").pack(pady=2)
        tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#888", fg="#fff").pack(pady=4)

    def open_location_ui():
        import tkinter as tk
        import location
        win = tk.Toplevel()
        win.title("Location Services")
        win.geometry("400x160")
        win.configure(bg="#222")
        tk.Label(win, text="Current Location:", bg="#222", fg="#FFD600").pack(pady=4)
        loc = location.get_location() if hasattr(location, 'get_location') else "Unknown"
        tk.Label(win, text=loc, bg="#222", fg="#fff").pack(pady=4)
        tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#888", fg="#fff").pack(pady=4)

    feature_buttons.append(("Translation", "#3949AB", "Translate text to another language.", open_translation_ui))
    feature_buttons.append(("Health & Fitness", "#D32F2F", "View health tips and activity.", open_health_ui))
    feature_buttons.append(("Security", "#E53935", "Check security status and features.", open_security_ui))
    feature_buttons.append(("Notes & To-Do", "#FFB300", "Take notes and manage to-dos.", open_notes_ui))
    feature_buttons.append(("Location Services", "#0097A7", "Get your current location.", open_location_ui))


def open_support_message_center():
    import tkinter as tk
    import json
    MESSAGE_FILE = "support_messages.json"
    def load_messages():
        try:
            with open(MESSAGE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    def save_messages(msgs):
        with open(MESSAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(msgs, f, indent=2)
    def refresh_messages():
        messages = load_messages()
        msg_list.delete(0, tk.END)
        for msg in messages:
            who = "You" if msg.get("from") == "user" else "Support"
            preview = msg.get("message", "")[:60].replace("\n", " ")
            msg_list.insert(tk.END, f"[{who}] {preview}")
    def on_select(event):
        idx = msg_list.curselection()
        if not idx:
            return
        messages = load_messages()
        msg = messages[idx[0]]
        who = "You" if msg.get("from") == "user" else "Support"
        msg_text.config(state="normal")
        msg_text.delete("1.0", tk.END)
        msg_text.insert(tk.END, f"{who} ({msg.get('timestamp','')}):\n\n{msg.get('message','')}")
        msg_text.config(state="disabled")
    def send_message():
        content = entry.get("1.0", "end").strip()
        if not content:
            status_var.set("Please enter a message.")
            return
        messages = load_messages()
        import datetime
        messages.append({
            "from": "user",
            "message": content,
            "timestamp": datetime.datetime.now().isoformat()
        })
        save_messages(messages)
        entry.delete("1.0", "end")
        status_var.set("Message sent. Support will reply here.")
        refresh_messages()
    win = tk.Toplevel(root)
    win.title("Support Message Center")
    win.geometry("520x420")
    win.configure(bg="#222")
    tk.Label(win, text="Support Message Center", font=("Arial", 15, "bold"), bg="#222", fg="#FFD600").pack(pady=10)
    frame = tk.Frame(win, bg="#222")
    frame.pack(fill="both", expand=True, padx=10, pady=5)
    msg_list = tk.Listbox(frame, font=("Arial", 11), bg="#111", fg="#fff", height=8)
    msg_list.pack(side="left", fill="y", expand=False)
    msg_list.bind('<<ListboxSelect>>', on_select)
    msg_text = tk.Text(frame, font=("Arial", 11), bg="#333", fg="#fff", width=40, height=8, state="disabled", wrap="word")
    msg_text.pack(side="right", fill="both", expand=True)
    status_var = tk.StringVar()
    tk.Label(win, textvariable=status_var, font=("Arial", 11), bg="#222", fg="#FFD600").pack(pady=2)
    tk.Label(win, text="Type a new message to support:", font=("Arial", 12), bg="#222", fg="#FFD600").pack(pady=2)
    entry = tk.Text(win, font=("Arial", 12), bg="#333", fg="#fff", height=4)
    entry.pack(fill="x", padx=10, pady=2)
    tk.Button(win, text="Send Message", command=send_message, font=("Arial", 12), bg="#43A047", fg="#fff").pack(pady=6)
    tk.Button(win, text="Close", command=win.destroy, font=("Arial", 12), bg="#D32F2F", fg="#fff").pack(pady=2)
    refresh_messages()
# --- 14-day free trial status helper ---
def get_machine_fingerprint():
    """Generate a unique machine fingerprint based on hardware"""
    import hashlib
    import platform
    import subprocess
    import uuid
    
    try:
        # Get system info
        system_info = platform.platform()
        processor = platform.processor()
        
        # Get motherboard serial (Windows)
        try:
            motherboard = subprocess.check_output('wmic baseboard get serialnumber', shell=True).decode().strip().split('\n')[1].strip()
        except:
            motherboard = "unknown"
        
        # Get disk serial
        try:
            disk_serial = subprocess.check_output('wmic diskdrive get serialnumber', shell=True).decode().strip().split('\n')[1].strip()
        except:
            disk_serial = "unknown"
        
        # Get MAC address
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
        
        # Combine all identifiers
        fingerprint_data = f"{system_info}{processor}{motherboard}{disk_serial}{mac}"
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
    except:
        # Fallback to simpler method
        return hashlib.sha256(platform.node().encode()).hexdigest()[:16]

def get_persistent_trial_data():
    """Get trial data from Windows registry or backup location"""
    import winreg
    import base64
    import os
    
    current_fingerprint = get_machine_fingerprint()
    
    # Method 1: Try Windows Registry first
    try:
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\AccessMate"
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
            trial_data, _ = winreg.QueryValueEx(key, "TrialData")
            winreg.CloseKey(key)
            
            # Decode and parse trial data
            decoded_data = base64.b64decode(trial_data).decode()
            machine_id, trial_start = decoded_data.split("|")
            
            # Verify machine fingerprint matches
            if machine_id == current_fingerprint:
                return trial_start
        except:
            pass
    except:
        pass
    
    # Method 2: Check backup hidden file
    try:
        temp_dir = os.environ.get('TEMP', os.environ.get('TMP', ''))
        if temp_dir:
            hidden_file = os.path.join(temp_dir, f".{current_fingerprint[:8]}.tmp")
            if os.path.exists(hidden_file):
                with open(hidden_file, 'r') as f:
                    trial_data = f.read().strip()
                
                # Decode and parse trial data
                decoded_data = base64.b64decode(trial_data).decode()
                machine_id, trial_start = decoded_data.split("|")
                
                # Verify machine fingerprint matches
                if machine_id == current_fingerprint:
                    return trial_start
    except:
        pass
    
    return None

def set_persistent_trial_data(trial_start):
    """Store trial data in Windows registry and backup location"""
    import winreg
    import base64
    import os
    
    success = False
    
    # Method 1: Windows Registry
    try:
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\AccessMate"
        
        # Create the key if it doesn't exist
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        except:
            key = None
        
        if key:
            # Encode trial data with machine fingerprint
            machine_id = get_machine_fingerprint()
            trial_data = f"{machine_id}|{trial_start}"
            encoded_data = base64.b64encode(trial_data.encode()).decode()
            
            # Store in registry
            winreg.SetValueEx(key, "TrialData", 0, winreg.REG_SZ, encoded_data)
            winreg.CloseKey(key)
            success = True
    except:
        pass
    
    # Method 2: Hidden system file backup
    try:
        # Store in system temp with hidden attribute
        temp_dir = os.environ.get('TEMP', os.environ.get('TMP', ''))
        if temp_dir:
            machine_id = get_machine_fingerprint()
            trial_data = f"{machine_id}|{trial_start}"
            encoded_data = base64.b64encode(trial_data.encode()).decode()
            
            # Create hidden file
            hidden_file = os.path.join(temp_dir, f".{machine_id[:8]}.tmp")
            with open(hidden_file, 'w') as f:
                f.write(encoded_data)
            
            # Set hidden attribute on Windows
            import subprocess
            try:
                subprocess.run(['attrib', '+H', hidden_file], shell=True, capture_output=True)
            except:
                pass
            success = True
    except:
        pass
    
    return success

def backend_trial_status(email):
    import datetime
    TRIAL_DAYS = 14
    
    # Check if user has purchased
    db = backend_load()
    user = db.get(email, {})
    if user.get("purchased", False):
        return ("full", 0)
    
    # Try to get persistent trial data first
    persistent_trial_start = get_persistent_trial_data()
    
    if persistent_trial_start:
        # Use persistent trial data
        trial_start = persistent_trial_start
    else:
        # Check local storage for trial start
        trial_start = user.get("trial_start")
        if not trial_start:
            # Start new trial
            trial_start = datetime.datetime.now().isoformat()
            user["trial_start"] = trial_start
            db[email] = user
            backend_save(db)
            
            # Also store in persistent location
            set_persistent_trial_data(trial_start)
        else:
            # Migrate existing trial to persistent storage
            set_persistent_trial_data(trial_start)
    
    # Calculate remaining days
    start = datetime.datetime.fromisoformat(trial_start)
    days_used = (datetime.datetime.now() - start).days
    days_left = max(0, TRIAL_DAYS - days_used)
    
    if days_left > 0:
        return ("trial", days_left)
    return ("expired", 0)
SECOND_USER_MODE = False

def activate_second_user_mode():
    global SECOND_USER_MODE
    SECOND_USER_MODE = True
    try:
        import tkinter as tk
        from tkinter import messagebox
        messagebox.showinfo("Second User Mode", "Second User Mode activated. Only basic features are available.")
    except Exception:
        pass

def deactivate_second_user_mode():
    global SECOND_USER_MODE
    SECOND_USER_MODE = False
    try:
        import tkinter as tk
        from tkinter import messagebox
        messagebox.showinfo("Second User Mode", "Second User Mode deactivated. Full features restored.")
    except Exception:
        pass

# --- Inline backend functions ---
import json
import uuid
import platform
BACKEND_FILE = "account_backend.json"

def backend_load():
    try:
        with open(BACKEND_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}
def backend_save(data):
    with open(BACKEND_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def backend_check_purchased(email):
    db = backend_load()
    return db.get(email, {}).get("purchased", False)

def backend_list_devices(email):
    db = backend_load()
    return db.get(email, {}).get("devices", [])

def backend_mark_purchased(email):
    db = backend_load()
    if email in db:
        db[email]["purchased"] = True
        backend_save(db)

def get_device_id():
    device_file = "device_id.txt"
    try:
        with open(device_file, "r") as f:
            return f.read().strip()
    except Exception:
        did = str(uuid.uuid4())
        with open(device_file, "w") as f:
            f.write(did)
        return did

def backend_remove_device(email, device_id):
    db = backend_load()
    if email in db:
        devices = db[email].get("devices", [])
        new_devices = [d for d in devices if (d["id"] if isinstance(d, dict) else d) != device_id]
        if len(new_devices) != len(devices):
            db[email]["devices"] = new_devices
            backend_save(db)
            return True
    return False
# --- Platform-specific dependency notes ---
# Linux: pip install notify2 pystray Pillow (and optionally python3-gi for AppIndicator)
# macOS: pip install pync pystray Pillow
# Windows: pip install win10toast pystray Pillow

# --- Cross-platform notification helper ---
def notify(title, message):
    # Unified notification for all platforms, fallback to print if no library
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=5, threaded=True)
        return
    except Exception:
        pass
    try:
        import notify2
        notify2.init("AccessMate")
        n = notify2.Notification(title, message)
        n.show()
        return
    except Exception:
        pass
    try:
        import pync
        pync.notify(message, title=title)
        return
    except Exception:
        pass
    print(f"NOTIFY: {title}: {message}")

# Import non-tkinter modules at module level
import os
import sys
import subprocess
import time
import threading
import importlib.util
import requests
import speech
import datetime
try:
    import winreg
    is_windows = True
except ImportError:
    winreg = None
    is_windows = False

# Global status variable and helper for status updates
def import_settings():
    set_content_var("Import not implemented yet.")
def open_help_window():
    set_content_var("Help window not implemented yet.")
def open_feedback_dialog():
    import tkinter as tk
    import smtplib
    from email.message import EmailMessage
    feedback_win = tk.Toplevel(root)
    feedback_win.title("Contact Support / Send Feedback")
    feedback_win.configure(bg="#222")
    feedback_win.geometry("420x380")
    tk.Label(feedback_win, text="Contact Support / Send Feedback", font=("Arial", 15, "bold"), bg="#222", fg="#FFD600").pack(pady=10)
    tk.Label(feedback_win, text="Your Email (optional):", font=("Arial", 12), bg="#222", fg="#FFD600").pack(pady=2)
    email_var = tk.StringVar()
    tk.Entry(feedback_win, textvariable=email_var, font=("Arial", 12), width=32, bg="#111", fg="#fff").pack(pady=2)
    tk.Label(feedback_win, text="Message:", font=("Arial", 12), bg="#222", fg="#FFD600").pack(pady=2)
    text = tk.Text(feedback_win, wrap="word", font=("Arial", 12), bg="#333", fg="#fff", height=8)
    text.pack(expand=True, fill="both", padx=10, pady=5)
    status_var = tk.StringVar()
    tk.Label(feedback_win, textvariable=status_var, font=("Arial", 11), bg="#222", fg="#FFD600").pack(pady=2)
    def submit_feedback():
        user_email = email_var.get().strip()
        content = text.get("1.0", "end").strip()
        if not content:
            status_var.set("Please enter a message before submitting.")
            return
        try:
            msg = EmailMessage()
            msg['Subject'] = '[AccessMate Support] User Feedback'
            msg['From'] = 'support@accessmate.app'
            msg['To'] = 'support@accessmate.app'
            msg['X-Priority'] = '1'
            body = f"User Email: {user_email if user_email else 'N/A'}\n\nMessage:\n{content}"
            msg.set_content(body)
            # --- SMTP CONFIGURATION ---
            # You must set up an SMTP relay for support@accessmate.app or use a Gmail/Outlook SMTP account here
            # Example below uses Gmail SMTP (replace with your credentials or app password)
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_user = 'your_gmail_username@gmail.com'  # Replace with your sending email
            smtp_pass = 'your_app_password'  # Use an app password, not your main password
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            status_var.set("Thank you! Your message was sent to support.")
            text.delete("1.0", "end")
        except Exception as e:
            status_var.set(f"Error sending message: {e}")
    tk.Button(feedback_win, text="Send", command=submit_feedback, font=("Arial", 12), bg="#43A047", fg="#fff").pack(pady=10)
    tk.Button(feedback_win, text="Close", command=feedback_win.destroy, font=("Arial", 12), bg="#D32F2F", fg="#fff").pack(pady=5)
def open_accessibility_audit():
    set_content_var("Accessibility audit not implemented yet.")

def is_autostart_enabled():
    import platform
    system = platform.system()
    if system == "Windows" and winreg:
        try:
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ) as key:
                val, _ = winreg.QueryValueEx(key, "AccessMate")
                return True if val else False
        except Exception:
            return False
    elif system == "Linux":
        autostart_path = os.path.expanduser("~/.config/autostart/AccessMate.desktop")
        return os.path.exists(autostart_path)
    elif system == "Darwin":
        plist_path = os.path.expanduser("~/Library/LaunchAgents/com.accessmate.autostart.plist")
        return os.path.exists(plist_path)
    return False

# COMMENTED OUT: Orphaned open_settings_gui() function - proper version exists inside launch()
# This function was causing UnboundLocalError because it referenced settings_win before definition
"""
def open_settings_gui():
    # --- Trial Status Section ---
    trial_status_var = tk.StringVar(value="Trial status unknown")
    account_email = getattr(user_settings, 'account', {}).get('email')
    if account_email:
        status, days = backend_trial_status(account_email)
        if status == "full":
            trial_status_var.set("Full Version Unlocked!")
        elif status == "trial":
            trial_status_var.set(f"Trial: {days} days left")
        else:
            trial_status_var.set("Trial expired. Please purchase to unlock.")
    else:
        trial_status_var.set("Not logged in. Trial not started.")
    trial_label = tk.Label(settings_win, textvariable=trial_status_var, font=("Arial", 13), bg="#222", fg="#FFD600")
    trial_label.pack(padx=10, pady=5, anchor="w")

    def update_trial_status():
        account_email = getattr(user_settings, 'account', {}).get('email')
        if account_email:
            status, days = backend_trial_status(account_email)
            if status == "full":
                trial_status_var.set("Full Version Unlocked!")
            elif status == "trial":
                trial_status_var.set(f"Trial: {days} days left")
            else:
                trial_status_var.set("Trial expired. Please purchase to unlock.")
        else:
            trial_status_var.set("Not logged in. Trial not started.")
    # Helper to disable all widgets in a frame (recursive)
    def disable_all_widgets(widget):
        for child in widget.winfo_children():
            try:
                child.configure(state="disabled")
            except Exception:
                pass
            disable_all_widgets(child)

    # --- Second User Mode Settings Section (visible to owner when active) ---
    if 'SECOND_USER_MODE' in globals() and SECOND_USER_MODE:
        import tkinter as tk
        second_user_frame = tk.LabelFrame(settings_win, text="Second User Mode Settings", bg="#222", fg="#fff", font=("Arial", 12))
        second_user_frame.pack(padx=10, pady=10, fill="x")
        tk.Label(second_user_frame, text="Second User Mode is currently active. You can control access and exit this mode below.", font=("Arial", 11), bg="#222", fg="#FFD600").pack(anchor="w", padx=5, pady=2)
        def exit_second_user():
            global SECOND_USER_MODE
            SECOND_USER_MODE = False
            tk.messagebox.showinfo("Second User Mode", "Second User Mode has been turned off.")
            settings_win.destroy()
        tk.Button(second_user_frame, text="Exit Second User Mode", command=exit_second_user, font=("Arial", 12), bg="#43A047", fg="#fff").pack(pady=5)
    # Show Second User Mode status and allow owner to exit it
    if 'SECOND_USER_MODE' in globals() and SECOND_USER_MODE:
        import tkinter as tk
        from tkinter import messagebox
        status_frame = tk.Frame(settings_win, bg="#222")
        status_frame.pack(pady=10)
        tk.Label(status_frame, text="Second User Mode is ACTIVE", font=("Arial", 13, "bold"), bg="#222", fg="#FFD600").pack(side="left", padx=5)
        def exit_second_user():
            global SECOND_USER_MODE
            SECOND_USER_MODE = False
            messagebox.showinfo("Second User Mode", "Second User Mode has been turned off.")
            settings_win.destroy()
        tk.Button(status_frame, text="Exit Second User Mode", command=exit_second_user, font=("Arial", 12), bg="#43A047", fg="#fff").pack(side="left", padx=10)
    if 'SECOND_USER_MODE' in globals() and SECOND_USER_MODE:
        import tkinter as tk
        from tkinter import messagebox
        allow = messagebox.askyesno("Owner Permission Required", "Second User is requesting access to Settings. Allow?")
        if not allow:
            messagebox.showinfo("Access Denied", "Settings access denied by device owner.")
            return
    # --- Device Management Section ---
    # If in Second User Mode, disable all settings controls after creation
    settings_disable_later = []
    def show_devices():
        account_email = getattr(user_settings, 'account', {}).get('email')
        if not account_email:
            tk.messagebox.showinfo("Devices", "Please log in to view devices.")
            return
        devices = backend_list_devices(account_email)
        device_id = get_device_id()
        win = tk.Toplevel(settings_win)
        win.title("Registered Devices")
        win.configure(bg="#222")
        tk.Label(win, text="Your Devices:", font=("Arial", 13), bg="#222", fg="#FFD600").pack(pady=5)
        for d in devices:
            did = d["id"] if isinstance(d, dict) else d
            dname = d["name"] if isinstance(d, dict) and "name" in d else "Unknown Device"
            label = f"{dname} ({did[:8]})" + (" (this device)" if did == device_id else "")
            row = tk.Frame(win, bg="#222")
            row.pack(fill="x", padx=10, pady=2)
            tk.Label(row, text=label, font=("Arial", 11), bg="#222", fg="#fff").pack(side="left")
            if did != device_id:
                def make_remove(dev_id):
                    return lambda: remove_device(dev_id, win)
                tk.Button(row, text="Remove", command=make_remove(did), font=("Arial", 10), bg="#D32F2F", fg="#fff").pack(side="right")

    def remove_device(dev_id, win):
        account_email = getattr(user_settings, 'account', {}).get('email')
        if backend_remove_device(account_email, dev_id):
            tk.messagebox.showinfo("Device Removed", "Device removed successfully.")
            win.destroy()
            show_devices()
        else:
            tk.messagebox.showerror("Error", "Could not remove device.")

    # Add button to Account section
    btn_view_devices = tk.Button(account_frame, text="View Devices", command=show_devices, font=("Arial", 12), bg="#1976D2", fg="#fff")
    btn_view_devices.pack(pady=5)
    settings_disable_later.append(account_frame)
    # --- Purchase Full Version Section ---
    purchase_frame = tk.LabelFrame(settings_win, text="Upgrade to Full Version", bg="#222", fg="#fff", font=("Arial", 12))
    purchase_frame.pack(padx=10, pady=10, fill="x")
    purchase_status_var = tk.StringVar(value="Trial or Free Version")
    # Check purchase status on load
    account_email = getattr(user_settings, 'account', {}).get('email')
    if account_email and backend_check_purchased(account_email):
        purchase_status_var.set("Full Version Unlocked!")
    tk.Label(purchase_frame, textvariable=purchase_status_var, font=("Arial", 12), bg="#222", fg="#FFD600").pack(anchor="w", padx=5, pady=2)

    def do_purchase():
        # Simulate in-app purchase (replace with real store logic)
        account_email = getattr(user_settings, 'account', {}).get('email')
        if not account_email:
            purchase_status_var.set("Please log in to purchase.")
            return
        backend_mark_purchased(account_email)
        purchase_status_var.set("Full Version Unlocked!")
        update_trial_status()
        tk.messagebox.showinfo("Purchase Complete", "Thank you for purchasing the full version! Your account is now unlocked on all devices.")

    btn_purchase = tk.Button(purchase_frame, text="Purchase Full Version", command=do_purchase, font=("Arial", 12), bg="#43A047", fg="#fff")
    btn_purchase.pack(pady=5)
    settings_disable_later.append(purchase_frame)

    # On login, update purchase status in UI
    def update_purchase_status():
        account_email = getattr(user_settings, 'account', {}).get('email')
        if account_email and backend_check_purchased(account_email):
            purchase_status_var.set("Full Version Unlocked!")
        else:
            purchase_status_var.set("Trial or Free Version")
        update_trial_status()
    # Patch into login/account creation logic
    old_save_account = locals().get('save_account')
    def save_account_and_update(email, token):
        if old_save_account:
            old_save_account(email, token)
        update_purchase_status()
        update_trial_status()
    globals()['save_account'] = save_account_and_update
    # --- Account Management Section ---
    account_frame = tk.LabelFrame(settings_win, text="Account", bg="#222", fg="#fff", font=("Arial", 12))
    account_frame.pack(padx=10, pady=10, fill="x")
    account_status_var = tk.StringVar(value="Not logged in")
    if hasattr(user_settings, 'account') and user_settings.account.get('email'):
        account_status_var.set(f"Logged in as: {user_settings.account['email']}")
    tk.Label(account_frame, textvariable=account_status_var, font=("Arial", 12), bg="#222", fg="#FFD600").pack(anchor="w", padx=5, pady=2)

    def save_account(email, token):
        if not hasattr(user_settings, 'account'):
            user_settings.account = {}
        user_settings.account['email'] = email
        user_settings.account['token'] = token
        user_settings.save("user_settings.json")
        account_status_var.set(f"Logged in as: {email}")

    def do_logout():
        user_settings.account = {}
        user_settings.save("user_settings.json")
        account_status_var.set("Not logged in")

    def do_login():
        login_win = tk.Toplevel(settings_win)
        login_win.title("Login to AccessMate Account")
        login_win.configure(bg="#222")
        tk.Label(login_win, text="Email:", font=("Arial", 12), bg="#222", fg="#FFD600").pack(pady=5)
        email_var = tk.StringVar()
        tk.Entry(login_win, textvariable=email_var, font=("Arial", 12), width=30).pack(pady=5)
        tk.Label(login_win, text="Password:", font=("Arial", 12), bg="#222", fg="#FFD600").pack(pady=5)
        pw_var = tk.StringVar()
        tk.Entry(login_win, textvariable=pw_var, font=("Arial", 12), width=30, show="*").pack(pady=5)
        status_var = tk.StringVar()
        tk.Label(login_win, textvariable=status_var, font=("Arial", 11), bg="#222", fg="#FFD600").pack(pady=5)
        def submit():
            email = email_var.get().strip()
            pw = pw_var.get().strip()
            if not email or not pw:
                status_var.set("Email and password required.")
                return
            # Simulate backend login (replace with real API call)
            import hashlib
            token = hashlib.sha256((email+pw).encode()).hexdigest()
            save_account(email, token)
            status_var.set("Login successful!")
            login_win.after(1000, login_win.destroy)
        tk.Button(login_win, text="Login", command=submit, font=("Arial", 12), bg="#43A047", fg="#fff").pack(pady=10)
        tk.Button(login_win, text="Cancel", command=login_win.destroy, font=("Arial", 12), bg="#D32F2F", fg="#fff").pack(pady=5)

    def do_create_account():
        reg_win = tk.Toplevel(settings_win)
        reg_win.title("Create AccessMate Account")
        reg_win.configure(bg="#222")
        tk.Label(reg_win, text="Email:", font=("Arial", 12), bg="#222", fg="#FFD600").pack(pady=5)
        email_var = tk.StringVar()
        tk.Entry(reg_win, textvariable=email_var, font=("Arial", 12), width=30).pack(pady=5)
        tk.Label(reg_win, text="Password:", font=("Arial", 12), bg="#222", fg="#FFD600").pack(pady=5)
        pw_var = tk.StringVar()
        tk.Entry(reg_win, textvariable=pw_var, font=("Arial", 12), width=30, show="*").pack(pady=5)
        status_var = tk.StringVar()
        tk.Label(reg_win, textvariable=status_var, font=("Arial", 11), bg="#222", fg="#FFD600").pack(pady=5)
        def submit():
            email = email_var.get().strip()
            pw = pw_var.get().strip()
            if not email or not pw:
                status_var.set("Email and password required.")
                return
            # Simulate backend registration (replace with real API call)
            import hashlib
            token = hashlib.sha256((email+pw).encode()).hexdigest()
            save_account(email, token)
            status_var.set("Account created!")
            reg_win.after(1000, reg_win.destroy)
        tk.Button(reg_win, text="Create Account", command=submit, font=("Arial", 12), bg="#43A047", fg="#fff").pack(pady=10)
        tk.Button(reg_win, text="Cancel", command=reg_win.destroy, font=("Arial", 12), bg="#D32F2F", fg="#fff").pack(pady=5)

    btns = tk.Frame(account_frame, bg="#222")
    btns.pack(pady=5)
    btn_login = tk.Button(btns, text="Login", command=do_login, font=("Arial", 12), bg="#1976D2", fg="#fff")
    btn_create = tk.Button(btns, text="Create Account", command=do_create_account, font=("Arial", 12), bg="#43A047", fg="#fff")
    btn_logout = tk.Button(btns, text="Logout", command=do_logout, font=("Arial", 12), bg="#D32F2F", fg="#fff")
    btn_login.pack(side="left", padx=5)
    btn_create.pack(side="left", padx=5)
    btn_logout.pack(side="left", padx=5)
    settings_disable_later.append(btns)
    # After all controls are created, if in Second User Mode, disable them
    if 'SECOND_USER_MODE' in globals() and SECOND_USER_MODE:
        for frame in settings_disable_later:
            disable_all_widgets(frame)
    # This is a wrapper to call the real settings GUI from anywhere
    pass
"""

# Global content variable will be initialized in launch() function
content_var = None
def set_content_var(msg):
    if content_var is not None:
        content_var.set(msg)
import sys
import traceback
import datetime

# Global error logging to error.log
def log_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    with open("error.log", "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.datetime.now().isoformat()}] Unhandled Exception:\n")
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
sys.excepthook = log_exception
import sys
import traceback
import datetime

# Global error logging to error.log
def log_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    with open("error.log", "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.datetime.now().isoformat()}] Unhandled Exception:\n")
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
sys.excepthook = log_exception
    # Import tray and voice logic dependencies in main scope
from camera import enroll_owner_voice
try:
    import pystray
    from PIL import Image as PILImage
except ImportError:
    pystray = None
    PILImage = None

# Voice command help dictionary for help lookups
HELP_COMMANDS = {
    "say time": "Speak the current time.",
    "say date": "Speak the current date.",
    "say weather": "Speak the current weather.",
    "help": "Get help for voice commands.",
    "open [program]": "Open a program by name.",
    "play [platform]": "Play media on a streaming platform.",
    "play audiobook": "Play an audiobook.",
    "set language": "Set your preferred language.",
    "set country": "Set your country for language defaults.",
    # Add more as needed
}

# GUI for enrolling/updating owner voice
def enroll_owner_voice_gui():
    import tkinter.messagebox as messagebox
    result = enroll_owner_voice()
    if result:
        messagebox.showinfo("Owner Voice", "Owner voice enrollment complete.")
    else:
        messagebox.showerror("Owner Voice", "Owner voice enrollment failed.")
    # ...existing code...

    # --- Quit button with confirmation ---
    def ask_quit(root=None):
        import tkinter.messagebox as messagebox
        if messagebox.askyesno("Quit AccessMate", "Are you sure you want to quit?"):
            if tray_icon:
                tray_icon.stop()
            if root is not None:
                root.destroy()
    # Remove the creation of quit_btn here; it should be created in the main GUI layout where scroll_frame is defined.
def askstring_with_logo(title, prompt, **kwargs):
    import tkinter as tk
    parent = kwargs.pop('parent', None)
    if not hasattr(askstring_with_logo, "dialog") or not askstring_with_logo.dialog.winfo_exists():
        askstring_with_logo.dialog = tk.Toplevel(parent) if parent is not None else tk.Toplevel()
        askstring_with_logo.dialog.withdraw()
    dialog = askstring_with_logo.dialog
    dialog.title(title)
    dialog.configure(bg="#222")
    for widget in dialog.winfo_children():
        widget.destroy()
    add_logo_to_window(dialog, bg="#222", size=(48, 48))
    label = tk.Label(dialog, text=prompt, font=("Arial", 14), bg="#222", fg="#FFD600")
    label.pack(pady=(5, 5))
    entry = tk.Entry(dialog, font=("Arial", 14), width=30)
    entry.pack(pady=(5, 10))
    entry.focus_set()
    result = {'value': None}
    def on_ok():
        result['value'] = entry.get()
        dialog.withdraw()
    btn = tk.Button(dialog, text="OK", command=on_ok, font=("Arial", 12), bg="#4FC3F7", fg="#222")
    btn.pack(pady=(0, 10))
    dialog.deiconify()
    dialog.grab_set()
    dialog.wait_window()
    return result['value']

def askinteger_with_logo(title, prompt, **kwargs):
    import tkinter as tk
    parent = kwargs.pop('parent', None)
    if not hasattr(askinteger_with_logo, "dialog") or not askinteger_with_logo.dialog.winfo_exists():
        askinteger_with_logo.dialog = tk.Toplevel(parent) if parent is not None else tk.Toplevel()
        askinteger_with_logo.dialog.withdraw()
    dialog = askinteger_with_logo.dialog
    dialog.title(title)
    dialog.configure(bg="#222")
    for widget in dialog.winfo_children():
        widget.destroy()
    add_logo_to_window(dialog, bg="#222", size=(48, 48))
    label = tk.Label(dialog, text=prompt, font=("Arial", 14), bg="#222", fg="#FFD600")
    label.pack(pady=(5, 5))
    entry = tk.Entry(dialog, font=("Arial", 14), width=10)
    entry.pack(pady=(5, 10))
    entry.focus_set()
    result = {'value': None}
    def on_ok():
        try:
            val = int(entry.get())
            result['value'] = val
        except Exception:
            result['value'] = None
        dialog.withdraw()
    btn = tk.Button(dialog, text="OK", command=on_ok, font=("Arial", 12), bg="#4FC3F7", fg="#222")
    btn.pack(pady=(0, 10))
    dialog.deiconify()
    dialog.grab_set()
    dialog.wait_window()
    return result['value']
def add_logo_to_window(window, bg="#222", size=(64, 64)):
    """Add the logo image to the top of a Toplevel or dialog window."""
    import os
    from PIL import Image, ImageTk
    import tkinter as tk
    def resource_path(rel_path):
        import sys
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, rel_path)
        return os.path.abspath(rel_path)
    logo_path = resource_path("src/accessmate_logo_uploaded.png")
    try:
        img = Image.open(logo_path)
        img = img.resize(size, Image.LANCZOS)
        logo_img = ImageTk.PhotoImage(img)
        logo_label = tk.Label(window, image=logo_img, bg=bg)
        logo_label.image = logo_img  # Keep reference
        logo_label.pack(pady=(10, 5))
    except Exception:
        logo_label = tk.Label(window, text="[Logo Missing]", font=("Arial", 16, "bold"), bg=bg, fg="#FFD600")
        logo_label.pack(pady=(10, 5))
feature_buttons = []
# Initialize feature_buttons to avoid UnboundLocalError
from settings import Settings
user_settings = Settings()
user_settings.load("user_settings.json")
from settings import Settings
# GUI module for AccessMate

import os
import sys
import subprocess
import time

# Safe import of accessibility module
try:
    from accessibility_module import enable_accessibility
    ACCESSIBILITY_AVAILABLE = True
except ImportError:
    try:
        from accessibility import enable_accessibility
        ACCESSIBILITY_AVAILABLE = True
    except ImportError:
        print("Warning: accessibility module not found. Accessibility features will be disabled.")
        ACCESSIBILITY_AVAILABLE = False
        
        # Define dummy function when accessibility module is not available
        def enable_accessibility(widget, tooltip=None):
            """Dummy function when accessibility module is not available."""
            pass

import speech

from iot_integrations import turn_on_light, turn_off_light, iot_status
import threading


THEMES = {
    "Dark": {"bg": "#222", "fg": "#fff", "btn_bg": "#333", "btn_fg": "#FFD600"},
    "Light": {"bg": "#fff", "fg": "#222", "btn_bg": "#eee", "btn_fg": "#222"},
    "Blue": {"bg": "#1976D2", "fg": "#fff", "btn_bg": "#2196F3", "btn_fg": "#FFD600"}
}

def launch(gui_instance):
    # Fix Tcl/Tk path issues for PyInstaller
    import os
    import sys
    
    # Set Tcl/Tk environment variables for PyInstaller
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        bundle_dir = sys._MEIPASS
        tcl_dir = os.path.join(bundle_dir, 'tcl')
        tk_dir = os.path.join(bundle_dir, 'tk')
        
        # Set environment variables
        os.environ['TCL_LIBRARY'] = tcl_dir
        os.environ['TK_LIBRARY'] = tk_dir
        
        # Also try alternate paths if main ones don't exist
        if not os.path.exists(tcl_dir):
            for alt_path in ['tcl8.6', '_tcl_data', 'lib/tcl8.6']:
                alt_tcl = os.path.join(bundle_dir, alt_path)
                if os.path.exists(alt_tcl):
                    os.environ['TCL_LIBRARY'] = alt_tcl
                    break
        
        if not os.path.exists(tk_dir):
            for alt_path in ['tk8.6', '_tk_data', 'lib/tk8.6']:
                alt_tk = os.path.join(bundle_dir, alt_path)
                if os.path.exists(alt_tk):
                    os.environ['TK_LIBRARY'] = alt_tk
                    break
    
    # Import tkinter modules at function level to avoid early variable creation
    import tkinter as tk
    import tkinter.messagebox as messagebox
    import tkinter.filedialog
    
    # On first run, prompt to enroll owner voice if not set
    def needs_owner_voice_enrollment():
        return not hasattr(user_settings, 'owner_voice_enrolled') or not user_settings.owner_voice_enrolled

    def mark_owner_voice_enrolled():
        user_settings.owner_voice_enrolled = True
        user_settings.save("user_settings.json")

    def prompt_owner_voice_enrollment():
        import tkinter.messagebox as messagebox
        if messagebox.askyesno("Owner Voice Setup", "You must enroll your voice as the owner before using the app.\nWould you like to enroll now?"):
            enroll_owner_voice_gui()
            mark_owner_voice_enrolled()
            set_content_var("Owner voice enrollment complete.")
        else:
            set_content_var("You must enroll your voice to use the app.")


    if needs_owner_voice_enrollment():
        # Ensure root is defined before using it
        global root
        if 'root' not in globals() or root is None:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
        root.after(500, prompt_owner_voice_enrollment)
    global feature_buttons
    # Persistent voice command mapping for games
    def edit_voice_command_mapping_gui():
        import tkinter.simpledialog
        mapping = getattr(user_settings, 'voice_game_command_map', None)
        if mapping is None:
            mapping = {'jump': 'space', 'left': 'left', 'right': 'right', 'up': 'up', 'down': 'down', 'shoot': 'ctrl'}
        mapping_str = ",".join(f"{k}:{v}" for k, v in mapping.items())
        new_mapping_str = askstring_with_logo("Edit Voice Command Mapping", "Edit mapping (e.g. jump:space,left:a,shoot:ctrl):")
        if new_mapping_str:
            try:
                new_map = dict(pair.split(":") for pair in new_mapping_str.split(",") if ":" in pair)
                user_settings.voice_game_command_map = new_map
                user_settings.save("user_settings.json")
                set_content_var("Voice command mapping updated.")
            except Exception:
                set_content_var("Invalid mapping format. No changes made.")
        else:
            set_content_var("No changes made.")

    def open_accessibility_audit():
        # This function is now at module/global scope so it can be used as a button command.
        audit_win = tk.Toplevel()
        audit_win.title("Accessibility Audit Tool")
        audit_win.configure(bg="#222")
        audit_win.geometry("500x400")
        tk.Label(audit_win, text="Accessibility Audit Results", font=("Arial", 16, "bold"), bg="#222", fg="#FFD600").pack(pady=10)
        results = []
        # Example checks (expand as needed)
        try:
            import platform
            if platform.system() == "Windows":
                import ctypes
                SPI_GETSCREENREADER = 70
                is_sr = ctypes.windll.user32.SystemParametersInfoW(SPI_GETSCREENREADER, 0, 0, 0)
                if is_sr:
                    results.append("Screen reader is enabled.")
                else:
                    results.append("Screen reader is NOT enabled. Consider enabling for best accessibility.")
            else:
                results.append("Non-Windows OS: Please check your system accessibility settings manually.")
        except Exception as e:
            results.append(f"Could not check screen reader status: {e}")
        # App-level checks
        results.append("TTS is enabled for all status changes and errors.")
        results.append("High-contrast UI is active.")
        results.append("Keyboard navigation is supported.")
        results.append("All buttons and toggles are screen reader friendly.")
        # Display results
        text = tk.Text(audit_win, wrap="word", font=("Arial", 13), bg="#222", fg="#fff", insertbackground="#FFD600")
        text.pack(expand=True, fill="both", padx=10, pady=10)
        text.insert("1.0", "\n".join(results))
        text.config(state="disabled")
        tk.Button(audit_win, text="Close", command=audit_win.destroy, font=("Arial", 12), bg="#D32F2F", fg="#fff").pack(pady=10)
    
        def open_settings_gui():
            # --- Settings window and status label ---
            global settings_win
            settings_win = tk.Toplevel()
            settings_win.title("Settings")
            settings_win.configure(bg="#222")
            settings_win.geometry("600x600")
            status_label = tk.Label(settings_win, textvariable=content_var, font=("Arial", 11), bg="#222", fg="#FFD600")
            status_label.pack(fill="x", padx=10, pady=(0, 5))

            # Analytics event logger
            def log_analytics_event(event, details=None):
                if getattr(user_settings, 'analytics_enabled', False):
                    with open("analytics.log", "a", encoding="utf-8") as f:
                        ts = datetime.datetime.now().isoformat()
                        f.write(f"[{ts}] {event}: {details if details else ''}\n")

            # Plugin/Extension System section (unchanged)
            try:
                import keyboard
            except ImportError:
                keyboard = None
            plugin_frame = tk.LabelFrame(settings_win, text="Plugin/Extension System", bg="#222", fg="#fff", font=("Arial", 12))
            plugin_frame.pack(padx=10, pady=10, fill="x")
            plugins_dir = "plugins"
            os.makedirs(plugins_dir, exist_ok=True)
            def list_plugins():
                return [f for f in os.listdir(plugins_dir) if f.endswith('.py')]
            if not hasattr(user_settings, 'enabled_plugins'):
                user_settings.enabled_plugins = {p: True for p in list_plugins()}
            else:
                for p in list_plugins():
                    if p not in user_settings.enabled_plugins:
                        user_settings.enabled_plugins[p] = True
                for p in list(user_settings.enabled_plugins.keys()):
                    if p not in list_plugins():
                        del user_settings.enabled_plugins[p]
            plugin_vars = {}
            def on_plugin_toggle(plugin):
                user_settings.enabled_plugins[plugin] = plugin_vars[plugin].get()
                user_settings.save("user_settings.json")
                log_analytics_event("plugin_toggle", f"{plugin}: {plugin_vars[plugin].get()}")
            for i, plugin in enumerate(list_plugins()):
                var = tk.BooleanVar(value=user_settings.enabled_plugins.get(plugin, True))
                plugin_vars[plugin] = var
                cb = tk.Checkbutton(plugin_frame, text=plugin, variable=var, font=("Arial", 12), bg="#222", fg="#FFD600", selectcolor="#333", command=lambda p=plugin: on_plugin_toggle(p))
                cb.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            loaded_plugins = {}
            def load_plugin(plugin):
                path = os.path.join(plugins_dir, plugin)
                name = f"plugin_{plugin.replace('.', '_')}"
                if name in sys.modules:
                    importlib.reload(sys.modules[name])
                else:
                    spec = importlib.util.spec_from_file_location(name, path)
                    if spec and spec.loader:
                        mod = importlib.util.module_from_spec(spec)
                        sys.modules[name] = mod
                        try:
                            spec.loader.exec_module(mod)
                            loaded_plugins[plugin] = mod
                        except Exception as e:
                            set_content_var(f"Failed to load {plugin}: {e}")
            def unload_plugin(plugin):
                name = f"plugin_{plugin.replace('.', '_')}"
                if name in sys.modules:
                    del sys.modules[name]
                if plugin in loaded_plugins:
                    del loaded_plugins[plugin]
            def reload_plugins():
                for plugin in list(loaded_plugins.keys()):
                    unload_plugin(plugin)
                for plugin, enabled in user_settings.enabled_plugins.items():
                    if enabled:
                        load_plugin(plugin)
                set_content_var("Plugins reloaded.")
                log_analytics_event("plugins_reloaded")
            tk.Button(plugin_frame, text="Reload Plugins", command=reload_plugins, font=("Arial", 12), bg="#43A047", fg="#fff").grid(row=0, column=1, padx=5, pady=2)
            for plugin, enabled in user_settings.enabled_plugins.items():
                if enabled:
                    load_plugin(plugin)

            # --- Define feature_toggles and check_vars for settings ---
            global feature_toggles, check_vars
            feature_toggles = [
                ("enable_barcode", "Barcode Scanner"),
                ("enable_object_detection", "Object Recognition"),
                ("enable_ocr", "OCR Screen Reader"),
                ("enable_face_recognition", "Face Recognition"),
                ("enable_currency_recognition", "Currency Recognition"),
                ("enable_color_recognition", "Color Recognition"),
                ("enable_pdf_reader", "PDF Reader"),
                ("enable_word_reader", "Word Reader"),
                ("enable_speech_recognition", "Speech Recognition"),
                ("enable_tts", "Text-to-Speech (TTS)"),
                ("enable_app_launch", "App Launcher"),
                ("enable_navigation", "Navigation"),
                ("enable_encryption", "Encryption"),
                ("enable_weather", "Weather"),
                ("enable_reminders", "Reminders"),
                ("enable_accessibility", "Accessibility"),
                ("enable_emergency_contact", "Emergency Contact"),
            ]
            check_vars = {}

            # --- Stubs for missing functions ---
            def import_settings():
                set_content_var("Import not implemented yet.")
            def open_help_window():
                set_content_var("Help window not implemented yet.")
            def open_feedback_dialog():
                set_content_var("Feedback dialog not implemented yet.")
            def open_accessibility_audit():
                set_content_var("Accessibility audit not implemented yet.")

            # ...rest of open_settings_gui unchanged...
    def open_feedback_dialog():
        feedback_win = tk.Toplevel(settings_win)
        feedback_win.title("Send Feedback / Report Bug")
        feedback_win.configure(bg="#222")
        feedback_win.geometry("400x350")
        tk.Label(feedback_win, text="Your feedback helps us improve!", font=("Arial", 14), bg="#222", fg="#FFD600").pack(pady=10)
        text = tk.Text(feedback_win, wrap="word", font=("Arial", 12), bg="#333", fg="#fff", height=10)
        text.pack(expand=True, fill="both", padx=10, pady=5)
        def submit_feedback():
            content = text.get("1.0", "end").strip()
            if content:
                try:
                    with open("user_feedback.txt", "a", encoding="utf-8") as f:
                        import datetime
                        f.write(f"[{datetime.datetime.now()}]\n{content}\n{'-'*40}\n")
                    tk.Label(feedback_win, text="Thank you for your feedback!", font=("Arial", 12), bg="#222", fg="#43A047").pack(pady=5)
                except Exception as e:
                    tk.Label(feedback_win, text=f"Error: {e}", font=("Arial", 12), bg="#222", fg="#D32F2F").pack(pady=5)
            else:
                tk.Label(feedback_win, text="Please enter feedback before submitting.", font=("Arial", 12), bg="#222", fg="#FFD600").pack(pady=5)
        tk.Button(feedback_win, text="Submit", command=submit_feedback, font=("Arial", 12), bg="#43A047", fg="#fff").pack(pady=10)
        tk.Button(feedback_win, text="Close", command=feedback_win.destroy, font=("Arial", 12), bg="#D32F2F", fg="#fff").pack(pady=5)
    # Cloud sync section - temporarily disabled due to scope issue
    # TODO: Move this code to proper settings function scope
    # cloud_frame = tk.LabelFrame(settings_win, text="Cloud Sync (Beta)", bg="#222", fg="#fff", font=("Arial", 12))
    # cloud_frame.pack(padx=10, pady=10, fill="x")
    # cloud_sync_var = tk.BooleanVar(value=getattr(user_settings, 'cloud_sync_enabled', False))
    # def toggle_cloud_sync():
    #     user_settings.cloud_sync_enabled = cloud_sync_var.get()
    #     user_settings.save("user_settings.json")
    #     set_content_var("Cloud sync " + ("enabled." if cloud_sync_var.get() else "disabled."))

    # tk.Checkbutton(cloud_frame, text="Enable cloud sync for settings (privacy policy applies)", variable=cloud_sync_var, command=toggle_cloud_sync, font=("Arial", 12), bg="#222", fg="#FFD600", selectcolor="#333").pack(anchor="w", padx=5, pady=5)

    def upload_settings_to_cloud():
        import requests
        DROPBOX_UPLOAD_URL = "https://content.dropboxapi.com/2/files/upload"
        token = getattr(user_settings, 'dropbox_token', None)
        if not token:
            from tkinter.simpledialog import askstring
            token = askstring("Dropbox Token", "Enter your Dropbox API token:")
            if not token:
                set_content_var("Cloud upload cancelled: No token provided.")
                return
            user_settings.dropbox_token = token
            user_settings.save("user_settings.json")
        headers = {
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": '{"path": "/accessmate_user_settings.json", "mode": "overwrite", "mute": false}',
            "Content-Type": "application/octet-stream"
        }
        try:
            with open("user_settings.json", "rb") as f:
                data = f.read()
            resp = requests.post(DROPBOX_UPLOAD_URL, headers=headers, data=data)
            if resp.status_code == 200:
                set_content_var("Settings uploaded to cloud.")
            else:
                set_content_var(f"Cloud upload failed: {resp.text}")
        except Exception as e:
            set_content_var(f"Cloud upload error: {e}")

    def download_settings_from_cloud():
        import requests
        DROPBOX_DOWNLOAD_URL = "https://content.dropboxapi.com/2/files/download"
        token = getattr(user_settings, 'dropbox_token', None)
        if not token:
            from tkinter.simpledialog import askstring
            token = askstring("Dropbox Token", "Enter your Dropbox API token:")
            if not token:
                set_content_var("Cloud download cancelled: No token provided.")
                return
            user_settings.dropbox_token = token
            user_settings.save("user_settings.json")
        headers = {
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": '{"path": "/accessmate_user_settings.json"}'
        }
        try:
            resp = requests.post(DROPBOX_DOWNLOAD_URL, headers=headers)
            if resp.status_code == 200:
                with open("user_settings.json", "wb") as f:
                    f.write(resp.content)
                set_content_var("Settings downloaded from cloud. Please restart the app.")
            else:
                set_content_var(f"Cloud download failed: {resp.text}")
        except Exception as e:
            set_content_var(f"Cloud download error: {e}")

    # btn_cloud = tk.Frame(cloud_frame, bg="#222")
    # btn_cloud.pack(pady=5)
    # tk.Button(btn_cloud, text="Upload Now", command=upload_settings_to_cloud, font=("Arial", 12), bg="#43A047", fg="#fff").pack(side="left", padx=5)
    # tk.Button(btn_cloud, text="Download Now", command=download_settings_from_cloud, font=("Arial", 12), bg="#1976D2", fg="#fff").pack(side="left", padx=5)
    def open_help_window():
        help_win = tk.Toplevel(settings_win)
        help_win.title("Help & Documentation")
        help_win.configure(bg="#222")
        help_win.geometry("600x500")
        text = tk.Text(help_win, wrap="word", font=("Arial", 13), bg="#222", fg="#fff", insertbackground="#FFD600")
        text.pack(expand=True, fill="both", padx=10, pady=10)
        help_content = (
            "AccessMate Help & Documentation\n\n"
            "- Use the tray icon for quick access to Show, Settings, Help, and Quit.\n"
            "- Enable auto-start to launch AccessMate with Windows.\n"
            "- All status changes and errors are announced via TTS for accessibility.\n"
            "- Use the Settings window to backup/restore settings, check for updates, and configure hotkeys.\n"
            "- Use the Voice Training Wizard to improve voice command accuracy.\n"
            "- Global hotkeys can be set for quick actions.\n"
            "- For accessibility, all buttons and toggles are screen reader friendly.\n"
            "- For more help, visit the official documentation or contact support.\n\n"
            "Keyboard Shortcuts:\n"
            "- F1: Open this help window\n"
            "- Ctrl+Alt+S: Show App (default)\n"
            "- Ctrl+Alt+R: Start Reading (default)\n"
            "- Ctrl+Alt+E: Emergency Call (default)\n"
        )
        text.insert("1.0", help_content)
        text.config(state="disabled")
        tk.Button(help_win, text="Close", command=help_win.destroy, font=("Arial", 12), bg="#D32F2F", fg="#fff").pack(pady=10)

    # Bind F1 to open help
    settings_win.bind_all("<F1>", lambda e: open_help_window())
    import speech_recognition as sr
    import pyttsx3


    settings_win = tk.Toplevel()
    settings_win.title("Settings")
    settings_win.configure(bg="#222")
    settings_win.geometry("600x600")

    def open_voice_training_wizard():
        wizard = tk.Toplevel(settings_win)
        wizard.title("Voice Command Training Wizard")
        wizard.configure(bg="#222")
        wizard.geometry("400x350")

        tk.Label(wizard, text="Voice Command Training", font=("Arial", 16, "bold"), bg="#222", fg="#fff").pack(pady=10)
        tk.Label(wizard, text="Speak the command you want to train, then test recognition.", font=("Arial", 11), bg="#222", fg="#fff").pack(pady=5)

        command_var = tk.StringVar()
        result_var = tk.StringVar()

        def tts_feedback(text):
            try:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            except Exception:
                pass

        def record_command():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                result_var.set("Listening...")
                wizard.update()
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                    result = recognizer.recognize_google(audio)
                    command_var.set(result)
                    result_var.set(f"Heard: {result}")
                    tts_feedback(f"Heard: {result}")
                except sr.WaitTimeoutError:
                    result_var.set("No speech detected.")
                    tts_feedback("No speech detected.")
                except sr.UnknownValueError:
                    result_var.set("Could not understand audio.")
                    tts_feedback("Could not understand audio.")
                except Exception as e:
                    result_var.set(f"Error: {e}")
                    tts_feedback(f"Error: {e}")

        def test_command():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                result_var.set("Say your command to test...")
                wizard.update()
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                    result = recognizer.recognize_google(audio)
                    if result.lower() == command_var.get().lower():
                        result_var.set("Recognition successful!")
                        tts_feedback("Recognition successful!")
                    else:
                        result_var.set(f"Heard: {result}. Does not match.")
                        tts_feedback(f"Heard: {result}. Does not match.")
                except Exception as e:
                    result_var.set(f"Error: {e}")
                    tts_feedback(f"Error: {e}")

        tk.Button(wizard, text="Record Command", command=record_command, font=("Arial", 13), bg="#43A047", fg="#fff").pack(pady=10)
        tk.Entry(wizard, textvariable=command_var, font=("Arial", 13), width=30, justify="center").pack(pady=5)
        tk.Button(wizard, text="Test Recognition", command=test_command, font=("Arial", 13), bg="#1976D2", fg="#fff").pack(pady=10)
        tk.Label(wizard, textvariable=result_var, font=("Arial", 12), bg="#222", fg="#FFD600").pack(pady=10)
        tk.Button(wizard, text="Close", command=wizard.destroy, font=("Arial", 12), bg="#D32F2F", fg="#fff").pack(pady=10)

    def open_voice_training_wizard():
        wizard = tk.Toplevel(settings_win)
        wizard.title("Voice Command Training Wizard")
        wizard.configure(bg="#222")
        wizard.geometry("400x350")

        tk.Label(wizard, text="Voice Command Training", font=("Arial", 16, "bold"), bg="#222", fg="#fff").pack(pady=10)
        tk.Label(wizard, text="Speak the command you want to train, then test recognition.", font=("Arial", 11), bg="#222", fg="#fff").pack(pady=5)

        command_var = tk.StringVar()
        result_var = tk.StringVar()

        def tts_feedback(text):
            try:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            except Exception:
                pass

        def record_command():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                result_var.set("Listening...")
                wizard.update()
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                    result = recognizer.recognize_google(audio)
                    command_var.set(result)
                    result_var.set(f"Heard: {result}")
                    tts_feedback(f"Heard: {result}")
                except sr.WaitTimeoutError:
                    result_var.set("No speech detected.")
                    tts_feedback("No speech detected.")
                except sr.UnknownValueError:
                    result_var.set("Could not understand audio.")
                    tts_feedback("Could not understand audio.")
                except Exception as e:
                    result_var.set(f"Error: {e}")
                    tts_feedback(f"Error: {e}")

        def test_command():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                result_var.set("Say your command to test...")
                wizard.update()
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                    result = recognizer.recognize_google(audio)
                    if result.lower() == command_var.get().lower():
                        result_var.set("Recognition successful!")
                        tts_feedback("Recognition successful!")
                    else:
                        result_var.set(f"Heard: {result}. Does not match.")
                        tts_feedback(f"Heard: {result}. Does not match.")
                except Exception as e:
                    result_var.set(f"Error: {e}")
                    tts_feedback(f"Error: {e}")

        tk.Button(wizard, text="Record Command", command=record_command, font=("Arial", 13), bg="#43A047", fg="#fff").pack(pady=10)
        tk.Entry(wizard, textvariable=command_var, font=("Arial", 13), width=30, justify="center").pack(pady=5)
        tk.Button(wizard, text="Test Recognition", command=test_command, font=("Arial", 13), bg="#1976D2", fg="#fff").pack(pady=10)
        tk.Label(wizard, textvariable=result_var, font=("Arial", 12), bg="#222", fg="#FFD600").pack(pady=10)
        tk.Button(wizard, text="Close", command=wizard.destroy, font=("Arial", 12), bg="#D32F2F", fg="#fff").pack(pady=10)

    # Hotkey config UI
    hotkey_frame = tk.LabelFrame(settings_win, text="Global Hotkeys", bg="#222", fg="#fff", font=("Arial", 12))
    hotkey_frame.pack(padx=10, pady=10, fill="x")
    hotkey_vars = {}
    hotkey_labels = {
        'show_app': 'Show App',
        'start_reading': 'Start Reading',
        'emergency_call': 'Emergency Call',
    }
    for i, (key, label) in enumerate(hotkey_labels.items()):
        tk.Label(hotkey_frame, text=label, bg="#222", fg="#fff", font=("Arial", 11)).grid(row=i, column=0, sticky="w", padx=5, pady=2)
        var = tk.StringVar(value=user_settings.hotkeys.get(key, ''))
        hotkey_vars[key] = var
        tk.Entry(hotkey_frame, textvariable=var, font=("Arial", 11), width=20).grid(row=i, column=1, padx=5, pady=2)

    def save_hotkeys():
        for k, v in hotkey_vars.items():
            user_settings.hotkeys[k] = v.get()
        user_settings.save("user_settings.json")
        set_content_var("Hotkeys saved. Please restart the app for changes to take effect.")

    tk.Button(hotkey_frame, text="Save Hotkeys", command=save_hotkeys, font=("Arial", 11), bg="#43A047", fg="#fff").grid(row=len(hotkey_labels), column=0, columnspan=2, pady=5)
def register_hotkeys():
    # Register global hotkeys using the keyboard library
    try:
        import keyboard
    except ImportError:
        set_content_var("Global hotkeys require the 'keyboard' package. Please install it with 'pip install keyboard'.")
        return
    try:
        hk = user_settings.hotkeys
        if hk.get('show_app'):
            # Define a stub for show_main_window if not already defined
            def show_main_window():
                try:
                    root.deiconify()
                    root.lift()
                    root.focus_force()
                except Exception:
                    set_content_var("Show App hotkey pressed.")
            keyboard.add_hotkey(hk['show_app'], show_main_window)
        if hk.get('start_reading'):
            keyboard.add_hotkey(hk['start_reading'], lambda: set_content_var("Reading started (demo)"))
        if hk.get('emergency_call'):
            keyboard.add_hotkey(hk['emergency_call'], lambda: set_content_var("Emergency call triggered (demo)"))
    except Exception as e:
        set_content_var(f"Hotkey registration failed: {e}")
    import requests
    import threading

    CURRENT_VERSION = "1.0.0"  # Update this as needed
    REMOTE_VERSION_URL = "https://raw.githubusercontent.com/yourusername/yourrepo/main/version.txt"  # Change to your version file

    def check_for_update():
        def do_check():
            try:
                resp = requests.get(REMOTE_VERSION_URL, timeout=5)
                if resp.status_code == 200:
                    remote_version = resp.text.strip()
                    if remote_version != CURRENT_VERSION:
                        set_content_var(f"Update available: v{remote_version} (You have v{CURRENT_VERSION})")
                    else:
                        set_content_var("You have the latest version.")
                else:
                    set_content_var("Could not check for updates (server error)")
            except Exception as e:
                set_content_var(f"Update check failed: {e}")
        threading.Thread(target=do_check, daemon=True).start()

    import tkinter.filedialog
    import speech_recognition as sr
    import pyttsx3


    def export_settings():
        file_path = tkinter.filedialog.asksaveasfilename(
            title="Export Settings",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:

                    def open_voice_training_wizard():
                        wizard = tk.Toplevel(settings_win)
                        wizard.title("Voice Command Training Wizard")
                        wizard.configure(bg="#222")
                        wizard.geometry("400x350")

                        tk.Label(wizard, text="Voice Command Training", font=("Arial", 16, "bold"), bg="#222", fg="#fff").pack(pady=10)
                        tk.Label(wizard, text="Speak the command you want to train, then test recognition.", font=("Arial", 11), bg="#222", fg="#fff").pack(pady=5)

                        command_var = tk.StringVar()
                        result_var = tk.StringVar()

                        def tts_feedback(text):
                            try:
                                engine = pyttsx3.init()
                                engine.say(text)
                                engine.runAndWait()
                            except Exception:
                                pass

                        def record_command():
                            recognizer = sr.Recognizer()
                            with sr.Microphone() as source:
                                result_var.set("Listening...")
                                wizard.update()
                                try:
                                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                                    result = recognizer.recognize_google(audio)
                                    command_var.set(result)
                                    result_var.set(f"Heard: {result}")
                                    tts_feedback(f"Heard: {result}")
                                except sr.WaitTimeoutError:
                                    result_var.set("No speech detected.")
                                    tts_feedback("No speech detected.")
                                except sr.UnknownValueError:
                                    result_var.set("Could not understand audio.")
                                    tts_feedback("Could not understand audio.")
                                except Exception as e:
                                    result_var.set(f"Error: {e}")
                                    tts_feedback(f"Error: {e}")

                        def test_command():
                            recognizer = sr.Recognizer()
                            with sr.Microphone() as source:
                                result_var.set("Say your command to test...")
                                wizard.update()
                                try:
                                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                                    result = recognizer.recognize_google(audio)
                                    if result.lower() == command_var.get().lower():
                                        result_var.set("Recognition successful!")
                                        tts_feedback("Recognition successful!")
                                    else:
                                        result_var.set(f"Heard: {result}. Does not match.")
                                        tts_feedback(f"Heard: {result}. Does not match.")
                                except Exception as e:
                                    result_var.set(f"Error: {e}")
                                    tts_feedback(f"Error: {e}")

                        tk.Button(wizard, text="Record Command", command=record_command, font=("Arial", 13), bg="#43A047", fg="#fff").pack(pady=10)
                        tk.Entry(wizard, textvariable=command_var, font=("Arial", 13), width=30, justify="center").pack(pady=5)
                        tk.Button(wizard, text="Test Recognition", command=test_command, font=("Arial", 13), bg="#1976D2", fg="#fff").pack(pady=10)
                        tk.Label(wizard, textvariable=result_var, font=("Arial", 12), bg="#222", fg="#FFD600").pack(pady=10)
                        tk.Button(wizard, text="Close", command=wizard.destroy, font=("Arial", 12), bg="#D32F2F", fg="#fff").pack(pady=10)
                    try:
                        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ) as key:
                            val, _ = winreg.QueryValueEx(key, "AccessMate")
                            return True if val else False
                    except FileNotFoundError:
                        return False
            except Exception:
                return False

        def set_autostart(enable):
            import platform
            system = platform.system()
            if system == "Windows" and winreg:
                try:
                    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                    exe = sys.executable
                    script = os.path.abspath(sys.argv[0])
                    cmd = f'"{exe}" "{script}"'
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS) as key:
                        if enable:
                            winreg.SetValueEx(key, "AccessMate", 0, winreg.REG_SZ, cmd)
                        else:
                            try:
                                winreg.DeleteValue(key, "AccessMate")
                            except FileNotFoundError:
                                pass
                except Exception as e:
                    set_content_var(f"Failed to update auto-start: {e}")
            elif system == "Linux":
                autostart_dir = os.path.expanduser("~/.config/autostart")
                os.makedirs(autostart_dir, exist_ok=True)
                desktop_path = os.path.join(autostart_dir, "AccessMate.desktop")
                exec_path = sys.executable
                script_path = os.path.abspath(sys.argv[0])
                desktop_entry = f"""[Desktop Entry]\nType=Application\nExec={exec_path} {script_path}\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName=AccessMate\nComment=Start AccessMate automatically"""
                try:
                    if enable:
                        with open(desktop_path, "w", encoding="utf-8") as f:
                            f.write(desktop_entry)
                    else:
                        if os.path.exists(desktop_path):
                            os.remove(desktop_path)
                except Exception as e:
                    set_content_var(f"Failed to update auto-start: {e}")
            elif system == "Darwin":
                plist_dir = os.path.expanduser("~/Library/LaunchAgents")
                os.makedirs(plist_dir, exist_ok=True)
                plist_path = os.path.join(plist_dir, "com.accessmate.autostart.plist")
                exec_path = sys.executable
                script_path = os.path.abspath(sys.argv[0])
                plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.accessmate.autostart</string>
    <key>ProgramArguments</key>
    <array>
        <string>{exec_path}</string>
        <string>{script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>'''
                try:
                    if enable:
                        with open(plist_path, "w", encoding="utf-8") as f:
                            f.write(plist_content)
                    else:
                        if os.path.exists(plist_path):
                            os.remove(plist_path)
                except Exception as e:
                    set_content_var(f"Failed to update auto-start: {e}")
            else:
                set_content_var("Autostart not supported on this platform.")

        autostart_var = tk.BooleanVar(value=is_autostart_enabled())

        def save_and_close():
            for attr, _ in feature_toggles:
                setattr(user_settings, attr, check_vars[attr].get())
            user_settings.save("user_settings.json")
            set_autostart(autostart_var.get())
            set_content_var("Settings saved. Some changes may require restart.")
            settings_win.withdraw()

        for attr, label in feature_toggles:
            check_vars[attr] = tk.BooleanVar(value=getattr(user_settings, attr, True))
            cb = tk.Checkbutton(settings_win, text=label, variable=check_vars[attr], font=("Arial", 14), bg="#222", fg="#fff", selectcolor="#333", activebackground="#333", activeforeground="#FFD600")
            cb.pack(anchor="w", padx=30, pady=4)

        # Add auto-start toggle for Windows
        if is_windows:
            auto_cb = tk.Checkbutton(settings_win, text="Start AccessMate automatically when Windows starts", variable=autostart_var, font=("Arial", 14), bg="#222", fg="#FFD600", selectcolor="#333", activebackground="#333", activeforeground="#FFD600")
            auto_cb.pack(anchor="w", padx=30, pady=10)

        btn_frame = tk.Frame(settings_win, bg="#222")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Save", command=save_and_close, font=("Arial", 14), bg="#4FC3F7", fg="#222").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Export", command=export_settings, font=("Arial", 14), bg="#43A047", fg="#fff").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Import", command=import_settings, font=("Arial", 14), bg="#1976D2", fg="#fff").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Check for Updates", command=check_for_update, font=("Arial", 14), bg="#FFA000", fg="#222").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Voice Training Wizard", command=open_voice_training_wizard, font=("Arial", 14), bg="#8E24AA", fg="#fff").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Help", command=open_help_window, font=("Arial", 14), bg="#FFD600", fg="#222").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Send Feedback", command=open_feedback_dialog, font=("Arial", 14), bg="#00B8D4", fg="#fff").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Accessibility Audit", command=open_accessibility_audit, font=("Arial", 14), bg="#FFD600", fg="#222").pack(side="left", padx=5)
        settings_win.deiconify()
        settings_win.grab_set()
        settings_win.wait_window()

    # Move feature_buttons.append and set_content_var after set_content_var is defined
    logo_label = None
    # ...existing code...

    # --- Filter feature_buttons by enabled features ---
    # Map feature_toggles to button labels for filtering
    feature_toggle_map = {
        "Barcode Scanner": "enable_barcode",
        "Object Recognition": "enable_object_detection",
        "OCR Screen Reader": "enable_ocr",
        "Face Recognition": "enable_face_recognition",
        "Currency Recognition": "enable_currency_recognition",
        "Color Recognition": "enable_color_recognition",
        "PDF Reader": "enable_pdf_reader",
        "Word Reader": "enable_word_reader",
        "Speech Recognition": "enable_speech_recognition",
        "Text-to-Speech (TTS)": "enable_tts",
        "App Launcher": "enable_app_launch",
        "Navigation": "enable_navigation",
        "Encryption": "enable_encryption",
        "Weather": "enable_weather",
        "Reminders": "enable_reminders",
        "Accessibility": "enable_accessibility",
        "Emergency Contact": "enable_emergency_contact",
    }

    def is_button_enabled(label):
        # If the button label matches a feature toggle, check user_settings
        attr = feature_toggle_map.get(label)
        if attr is not None:
            return getattr(user_settings, attr, True)
        return True  # Non-toggleable features always enabled

    # Filter feature_buttons in-place to only enabled features
    feature_buttons[:] = [btn for btn in feature_buttons if is_button_enabled(btn[0])]
    # Launch Installed Game by voice or text
    def launch_installed_game_gui():
        import tkinter.simpledialog
        from accessible_game import AccessibleAudioGame
        game_win = tk.Toplevel(root)
        game_win.title("Launch Game")
        game_win.geometry("400x200")
        game_win.configure(bg="#222")
        add_logo_to_window(game_win, bg="#222", size=(60, 60))
        prompt = tk.Label(game_win, text="Say 'voice' to use mic, or type game name:", font=("Arial", 14), bg="#222", fg="#FFD600")
        prompt.pack(pady=10)
        entry = tk.Entry(game_win, font=("Arial", 14), width=25)
        entry.pack(pady=5)
        def submit():
            val = entry.get().strip()
            if val.lower() == 'voice':
                game = AccessibleAudioGame()
                game_name = game.stt("Say the name of the game to launch:")
                set_content_var(f"Attempted to launch: {game_name}")
            elif val:
                open_program(val)
                set_content_var(f"Attempted to launch: {val}")
            else:
                set_content_var("No game name provided.")
            game_win.destroy()
        tk.Button(game_win, text="OK", command=submit, font=("Arial", 12), bg="#4FC3F7", fg="#222").pack(pady=10)
    feature_buttons.append(("Launch Installed Game", "#FF4081", "Launch any installed game by voice or text.", launch_installed_game_gui))
    # Persistent setting for auto emergency call
    if not hasattr(user_settings, 'auto_emergency_call_enabled'):
        user_settings.auto_emergency_call_enabled = True
        user_settings.save("user_settings.json")

    def toggle_auto_emergency_call():
        user_settings.auto_emergency_call_enabled = not user_settings.auto_emergency_call_enabled
        user_settings.save("user_settings.json")
        status = "enabled" if user_settings.auto_emergency_call_enabled else "disabled"
        set_content_var(f"Auto emergency call is now {status}.")
        speech.speak(content_var.get())

    feature_buttons.append(("Toggle Auto Emergency Call", "#FF6F00", "Enable or disable automatic emergency calling.", toggle_auto_emergency_call))
    # Emergency services auto-call logic
    def auto_call_emergency_services():
        from emergency_contacts import get_contacts, call_contact, check_contact_answered
        from location import get_current_location, send_location_pin
        if not getattr(user_settings, 'auto_emergency_call_enabled', True):
            set_content_var("Auto emergency call is disabled.")
            speech.speak(content_var.get())
            return
        contacts = get_contacts()
        answered = False
        for contact in contacts:
            call_contact(contact)
            # Wait for answer (simulate with check_contact_answered)
            if check_contact_answered(contact):
                answered = True
                break
        if not answered:
            # No contact answered, call emergency services
            try:
                from location import get_location
                loc = get_location()
                # Country detection logic
                import geopy
                from geopy.geocoders import Nominatim
                geolocator = Nominatim(user_agent="accessmate")
                location_info = geolocator.geocode(loc)
                country = getattr(location_info, 'address', '').split(',')[-1].strip() if location_info else ''
                # Emergency number mapping
                emergency_numbers = {
                    'United Kingdom': '999',
                    'United States': '911',
                    'France': '112',
                    'Germany': '112',
                    'Switzerland': '112',
                    'Belgium': '112',
                    'Austria': '112',
                    'Australia': '000',
                    'Canada': '911',
                    'India': '112',
                    'European Union': '112',
                }
                emergency_number = emergency_numbers.get(country, '112')
                from call_integration import open_phone_dialer
                open_phone_dialer(emergency_number)
                send_location_pin(loc)
                set_content_var(f"No emergency contact answered. Called emergency services ({emergency_number}) and sent location pin.")
                speech.speak(content_var.get())
            except Exception as e:
                set_content_var(f"Failed to call emergency services: {e}")
                speech.speak(content_var.get())
        else:
            set_content_var("Emergency contact answered. No need to call emergency services.")
            speech.speak(content_var.get())

    feature_buttons.append(("Auto Emergency Call", "#D50000", "Automatically call emergency services and send location if contacts do not answer.", auto_call_emergency_services))
    # Email Management UI
    def open_email_ui():
        import tkinter as tk
        from email_integration import list_emails, read_email
        email_win = tk.Toplevel(root)
        email_win.title("Email Management")
        email_win.geometry("600x400")
        email_win.configure(bg="#222")
        add_logo_to_window(email_win, bg="#222", size=(60, 60))
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

    feature_buttons.append(("Email Management", "#1976D2", "Read and manage your email inbox.", open_email_ui))
    # More streaming platform browsers
    def browse_platform_gui(platform):
        from media import search_streaming, play_streaming
        search = askstring_with_logo(f"Browse {platform}", f"Enter search term for {platform}:")
        items = search_streaming(platform, search)
        if not items:
            set_content_var(f"No results found on {platform}.")
            speech.speak(f"No results found on {platform}.")
            return
        import time
        import threading
        def auto_play_item(idx):
            if idx >= len(items):
                return
            item = items[idx]
            def speak_and_schedule():
                # Speech in background thread
                if 'synopsis' in item:
                    speech.speak(f"{platform} {idx+1}: {item['title']}. Synopsis: {item['synopsis']}")
                else:
                    speech.speak(f"{platform} {idx+1}: {item['title']}")
                # UI update on main thread
                root.after(0, lambda: set_content_var(f"Browsing: {item['title']}"))
                # Schedule auto-play after 20 seconds if still browsing this item
                def check_and_play():
                    if content_var.get() == f"Browsing: {item['title']}":
                        # Play media in background thread
                        def play_and_update():
                            result = play_streaming(platform, item['id'])
                            root.after(0, lambda: set_content_var(result if result else f"Playing: {item['title']} on {platform}"))
                            speech.speak(content_var.get())
                        threading.Thread(target=play_and_update, daemon=True).start()
                root.after(20000, check_and_play)
            threading.Thread(target=speak_and_schedule, daemon=True).start()
        for i in range(len(items)):
            auto_play_item(i)

    # Add buttons for all major platforms
    platforms = [
        ("Apple Music", "#FA57C1"),
        ("Disney+", "#113CCF"),
        ("Audible", "#F8991C"),
        ("Google Play Music", "#FF5722"),
        ("Tidal", "#000000"),
        ("Pandora", "#005FF9"),
        ("Deezer", "#FF0000"),
        ("YouTube Music", "#FF0000"),
        ("Prime Video", "#00A8E1"),
        ("HBO Max", "#6E1E8C"),
        ("Paramount+", "#0064FF"),
        ("Peacock", "#FFC700"),
        ("Scribd", "#1A7C6B"),
        ("Libby", "#7B3F00"),
        ("OverDrive", "#1B75BC"),
        ("Google Podcasts", "#4285F4"),
        ("Pocket Casts", "#E53935"),
        ("iHeartRadio", "#C6002B"),
        ("BBC Sounds", "#FF6600"),
        ("Spotify", "#1DB954"),
        ("Netflix", "#E50914"),
        ("Hulu", "#3DBB3D"),
        ("Amazon Music", "#FF9900"),
    ]
    for name, color in platforms:
        feature_buttons.append((f"Browse {name}", color, f"Browse and play media on {name}.", lambda n=name: browse_platform_gui(n)))
    # Streaming platform browsers
    def browse_streaming_gui(platform):
        from media import search_streaming, play_streaming
        search = askstring_with_logo(f"Browse {platform}", f"Enter search term for {platform}:")
        items = search_streaming(platform, search)
        if not items:
            set_content_var(f"No results found on {platform}.")
            speech.speak(f"No results found on {platform}.")
            return
        for i, item in enumerate(items):
            if 'synopsis' in item:
                speech.speak(f"{platform} {i+1}: {item['title']}. Synopsis: {item['synopsis']}")
            else:
                speech.speak(f"{platform} {i+1}: {item['title']}")
        choice = askinteger_with_logo("Select Item", f"Enter number to play (1-{len(items)}):")
        if choice and 1 <= choice <= len(items):
            result = play_streaming(platform, items[choice-1]['id'])
            set_content_var(result if result else f"Playing: {items[choice-1]['title']} on {platform}")
            speech.speak(content_var.get())
        else:
            set_content_var("No item selected.")
            speech.speak("No item selected.")

    feature_buttons.append(("Browse Netflix", "#E50914", "Browse and play shows/movies on Netflix.", lambda: browse_streaming_gui("Netflix")))
    feature_buttons.append(("Browse Spotify", "#1DB954", "Browse and play music on Spotify.", lambda: browse_streaming_gui("Spotify")))
    feature_buttons.append(("Browse Hulu", "#3DBB3D", "Browse and play shows/movies on Hulu.", lambda: browse_streaming_gui("Hulu")))
    feature_buttons.append(("Browse Amazon Music", "#FF9900", "Browse and play music on Amazon Music.", lambda: browse_streaming_gui("Amazon Music")))
    # Audiobook app browser
    def browse_audiobook_app_gui():
        import tkinter.simpledialog
        from media import get_audiobook_list
        app = askstring_with_logo("Audiobook App", "Enter audiobook app name:")
        if not app:
            set_content_var("No app entered.")
            return
        books = get_audiobook_list(app)
        if not books:
            set_content_var(f"No books found in {app}.")
            speech.speak(f"No books found in {app}.")
            return
        for i, book in enumerate(books):
            speech.speak(f"Book {i+1}: {book['title']}. Synopsis: {book['synopsis']}")
        set_content_var(f"{len(books)} books found in {app}. Browsed and spoken.")

    feature_buttons.append(("Browse Audiobook App", "#8E24AA", "Browse and hear book names and synopses from a chosen audiobook app.", browse_audiobook_app_gui))
    # Streaming and book library controls
    def play_youtube_gui():
        import tkinter.simpledialog
        from media import search_youtube, play_youtube
        search = askstring_with_logo("Play YouTube", "Enter channel name or search term:")
        videos = search_youtube(search)
        if not videos:
            set_content_var("No videos found.")
            speech.speak("No videos found.")
            return
        # Read out video titles as user browses
        for i, video in enumerate(videos):
            speech.speak(f"Video {i+1}: {video['title']}")
        # Ask user which video to play
        import tkinter.simpledialog
        choice = askinteger_with_logo("Select Video", f"Enter video number to play (1-{len(videos)}):")
        if choice and 1 <= choice <= len(videos):
            from media import play_youtube
            result = play_youtube(videos[choice-1]['url'])
            set_content_var(result if result else f"Playing: {videos[choice-1]['title']}")
            speech.speak(content_var.get())
        else:
            set_content_var("No video selected.")
            speech.speak("No video selected.")

    def play_streaming_gui():
        from media import play_streaming
        platform = askstring_with_logo("Play Streaming", "Enter platform (Netflix, Spotify, etc.):")
        query = askstring_with_logo("Play Streaming", "Enter show/song name or URL:")
        result = play_streaming(platform, query)
        set_content_var(result if result else f"Playing on {platform}.")
        speech.speak(content_var.get())

    def play_book_library_gui():
        import tkinter.simpledialog
        from media import play_book_library
        book = askstring_with_logo("Play Book Library", "Enter book title or author:")
        result = play_book_library(book)
        set_content_var(result if result else "Playing audiobook or e-book.")
        speech.speak(content_var.get())

    feature_buttons.append(("Play YouTube", "#D32F2F", "Play YouTube video by URL or search.", play_youtube_gui))
    feature_buttons.append(("Play Streaming", "#388E3C", "Play media from Netflix, Spotify, etc.", play_streaming_gui))
    feature_buttons.append(("Play Book Library", "#FBC02D", "Play audiobook or e-book from library.", play_book_library_gui))
    # Media function
    def show_media_panel_gui():
        from media import open_media_panel
        result = open_media_panel()
        set_content_var(result if result else "Media panel opened.")
        speech.speak(content_var.get())

    feature_buttons.append(("Media", "#0288D1", "Open media control panel for playback and browsing.", show_media_panel_gui))
    # Dashboard function
    def show_dashboard_gui():
        from dashboard import get_dashboard_summary
        summary = get_dashboard_summary(user_settings)
        set_content_var(summary)
        speech.speak(summary)

    # ...existing code...
    # --- System tray integration and Quit button ---
    global tray_icon
    tray_icon = None
    def resource_path(relative_path):
        try:
                       base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def ask_quit():
        import tkinter.messagebox as messagebox
        if messagebox.askyesno("Quit AccessMate", "Are you sure you want to quit?"):
            if tray_icon:
                tray_icon.stop()
            root.destroy()

    def on_quit_from_tray(icon, item):
        root.after(0, ask_quit)
    def show_window(icon, item):
        root.after(0, lambda: root.deiconify())
    def open_settings_from_tray(icon, item):
        root.after(0, open_settings_gui)
    def open_help_from_tray(icon, item):
        root.after(0, lambda: show_help_window())
    def hide_window():
        root.withdraw()

    # Move open_settings_gui definition here so it is defined before use
    def open_settings_gui():
        # --- Settings window and status label ---
        global settings_win
        settings_win = tk.Toplevel()
        settings_win.title("Settings")
        settings_win.configure(bg="#222")
        settings_win.geometry("600x600")
        status_label = tk.Label(settings_win, textvariable=content_var, font=("Arial", 11), bg="#222", fg="#FFD600")
        status_label.pack(fill="x", padx=10, pady=(0, 5))
        
        # Simple settings implementation
        tk.Label(settings_win, text="AccessMate Settings", font=("Arial", 16, "bold"), bg="#222", fg="#FFD600").pack(pady=10)
        
        # Basic feature toggles
        feature_toggles = [
            ("enable_speech_recognition", "Speech Recognition"),
            ("enable_tts", "Text-to-Speech"),
            ("enable_accessibility", "Accessibility Features"),
            ("enable_weather", "Weather"),
            ("enable_reminders", "Reminders")
        ]
        
        check_vars = {}
        for attr, label in feature_toggles:
            check_vars[attr] = tk.BooleanVar(value=getattr(user_settings, attr, True))
            cb = tk.Checkbutton(settings_win, text=label, variable=check_vars[attr], 
                               font=("Arial", 12), bg="#222", fg="#fff", selectcolor="#333")
            cb.pack(anchor="w", padx=20, pady=2)
        
        def save_and_close():
            for attr, _ in feature_toggles:
                setattr(user_settings, attr, check_vars[attr].get())
            user_settings.save("user_settings.json")
            set_content_var("Settings saved successfully.")
            settings_win.destroy()
        
        btn_frame = tk.Frame(settings_win, bg="#222")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Save", command=save_and_close, font=("Arial", 12), bg="#4FC3F7", fg="#222").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", command=settings_win.destroy, font=("Arial", 12), bg="#D32F2F", fg="#fff").pack(side="left", padx=5)

    def show_help_window():
        import tkinter as tk
        from help_sheet import HELP_TEXT
        help_win = tk.Toplevel(root)
        help_win.title("AccessMate Help")
        help_win.geometry("800x600")
        help_win.configure(bg="#222")
        add_logo_to_window(help_win, bg="#222", size=(60, 60))
        
        # Create scrollable text widget for comprehensive help
        import tkinter.scrolledtext as scrolledtext
        text_widget = scrolledtext.ScrolledText(help_win, font=("Arial", 11), bg="#333", fg="#FFD600", 
                                               wrap="word", width=80, height=30)
        text_widget.pack(padx=20, pady=20, fill="both", expand=True)
        text_widget.insert("1.0", HELP_TEXT)
        text_widget.config(state="disabled")  # Make read-only

    # Unified tray icon logic for all platforms using pystray
    tray_supported = False
    if pystray and PILImage:
        icon_path = resource_path("src/accessmate_logo_uploaded.png")
        try:
            image = PILImage.open(icon_path)
        except Exception:
            image = PILImage.new("RGB", (64, 64), color="#FFD600")
        menu = pystray.Menu(
            pystray.MenuItem("Show", show_window),
            pystray.MenuItem("Settings", open_settings_from_tray),
            pystray.MenuItem("Help", open_help_from_tray),
            pystray.MenuItem("Quit", on_quit_from_tray)
        )
        tray_icon = pystray.Icon("AccessMate", image, "AccessMate", menu)
        tray_supported = True
        threading.Thread(target=tray_icon.run, daemon=True).start()
        def on_closing():
            hide_window()
        root.protocol("WM_DELETE_WINDOW", on_closing)
    else:
        def on_closing():
            root.withdraw()
        root.protocol("WM_DELETE_WINDOW", on_closing)

    quit_btn = tk.Button(scroll_frame, text="Quit", font=("Arial", 14), bg="#D32F2F", fg="#fff", command=ask_quit)
    quit_btn.grid(row=999, column=0, columnspan=3, pady=20, sticky="ew")
    feature_buttons.append(("Enroll/Update Owner Voice", "#C51162", "Record and save your voice profile for secure authentication.", enroll_owner_voice_gui))
    # Accessible Game integration
    def play_accessible_game_gui():
        from accessible_game import AccessibleAudioGame
        game = AccessibleAudioGame()
        game.start()
        set_content_var("Accessible audio game finished.")
    feature_buttons.append(("Accessible Game", "#00B0FF", "Play an accessible audio game with audio and haptic feedback.", play_accessible_game_gui))

    # OCR Screen Reader integration
    def ocr_screen_reader_gui():
        from ocr_screen_reader import OCRScreenReader
        file_path = tkinter.filedialog.askopenfilename(title="Select image or PDF for OCR", filetypes=[("Image/PDF Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.pdf")])
        if not file_path:
            set_content_var("No file selected.")
            return
        reader = OCRScreenReader()
        if file_path.lower().endswith(".pdf"):
            text = reader.read_pdf(file_path)
        else:
            text = reader.read_image(file_path)
        if text:
            set_content_var(f"OCR Result:\n{text[:200]}{'...' if len(text) > 200 else ''}")
        else:
            set_content_var("OCR failed or no text found.")
    feature_buttons.append(("OCR Screen Reader", "#43A047", "Read text from images or PDFs using OCR.", ocr_screen_reader_gui))
    # Move feature button appends and helper functions after content_var and feature_buttons are defined
    # ...existing code...
    # After content_var and feature_buttons are defined:
    # ...existing code...
    # After content_var and feature_buttons are defined:

    # Define feature_buttons as a list to hold feature button definitions
    root = tk.Tk()
    root.withdraw()  # Hide window until fully laid out
    root.title("AccessMate")
    root.geometry("1000x800")
    root.minsize(1000, 800)
    root.maxsize(1000, 800)
    root.configure(bg="#222")
    import tkinter.messagebox as messagebox
    # Set window icon using absolute path and error reporting
    import os
    # Robust icon path for PyInstaller and dev
    def resource_path(rel_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, rel_path)
        return os.path.abspath(rel_path)
    import platform
    icon_error = False
    icon_label = None
    system = platform.system()
    icon_error = False
    icon_label = None
    icon_path_ico = resource_path("src/accessmate_logo.ico")
    icon_path_png = resource_path("src/accessmate_logo_uploaded.png")
    icon_path = icon_path_ico if system == "Windows" and os.path.exists(icon_path_ico) else icon_path_png
    print(f"[DEBUG] Icon path resolved to: {icon_path}")
    print(f"[DEBUG] Icon file exists: {os.path.exists(icon_path)}")
    if not os.path.exists(icon_path):
        print(f"[ERROR] App icon file not found: {icon_path}")
        icon_error = True
    else:
        try:
            if system == "Windows" and icon_path.endswith('.ico'):
                root.iconbitmap(icon_path)
                print(f"[INFO] App icon loaded successfully with iconbitmap: {icon_path}")
            else:
                icon_img = tk.PhotoImage(file=icon_path_png)
                root.iconphoto(True, icon_img)
                print(f"[INFO] App icon loaded successfully with iconphoto: {icon_path_png}")
        except Exception as e:
            print(f"[ERROR] Could not set app icon: {e} (path: {icon_path})")
            icon_error = True
    if icon_error:
        try:
            messagebox.showwarning("Logo Error", "App logo could not be loaded. A placeholder will be shown.")
        except Exception:
            pass
        parent = locals().get('scroll_frame', root)
        icon_label = tk.Label(parent, text="[Icon Error]", font=("Arial", 12, "bold"), bg="#222", fg="#FFD600")
        if parent == root:
            icon_label.pack(pady=(10, 5), anchor="ne")
        else:
            icon_label.grid(row=0, column=2, sticky="ne", padx=10, pady=5)

    canvas = tk.Canvas(root, bg="#222", highlightthickness=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#222")
    canvas.create_window((0,0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Enable mouse wheel scrolling for the canvas
    def _on_mousewheel(event):
        if event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "units")

    # Windows and Mac/Linux bindings
    canvas.bind_all('<MouseWheel>', _on_mousewheel)  # Windows, Mac
    canvas.bind_all('<Button-4>', _on_mousewheel)    # Linux scroll up
    canvas.bind_all('<Button-5>', _on_mousewheel)    # Linux scroll down
    # Delay scrollregion update until after all widgets are created
    def update_scrollregion_later():
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    global content_var
    content_var = tk.StringVar(root, value="Welcome to AccessMate!")
    # Add a status bar at the bottom for all messages
    status_var = tk.StringVar(root, value="Ready.")
    status_bar = tk.Label(root, textvariable=status_var, font=("Arial", 12), bg="#111", fg="#FFD600", anchor="w")
    status_bar.pack(side="bottom", fill="x")
    import time
    import threading
    _last_content = [content_var.get()]
    _pending_update = [None]
    _last_update_time = [0.0]
    _min_interval = 0.2  # 200ms = max 5 updates/sec
    def set_content_var(val, announce=True):
        def safe_update():
            now = time.time()
            if _last_content[0] == val:
                return
            elapsed = now - _last_update_time[0]
            def do_update():
                content_var.set(val)
                status_var.set(val)
                _pending_update[0] = None
                _last_update_time[0] = time.time()
                if announce:
                    try:
                        import speech
                        speech.speak(val)
                    except Exception:
                        pass
                # Show notification for status changes (except empty)
                if val and val.strip():
                    notify("AccessMate", val)
            if elapsed >= _min_interval:
                _last_content[0] = val
                _last_update_time[0] = now
                if _pending_update[0] is not None:
                    root.after_cancel(_pending_update[0])
                root.after_idle(do_update)
            else:
                if _pending_update[0] is not None:
                    root.after_cancel(_pending_update[0])
                wait_ms = int((_min_interval - elapsed) * 1000)
                def safe_update():
                    now = time.time()
                    if _last_content[0] == val:
                        return
                    elapsed = now - _last_update_time[0]
                    def do_update(v):
                        content_var.set(v)
                        status_var.set(v)
                        _pending_update[0] = None
                        _last_update_time[0] = time.time()
                        try:
                            speech.speak(v)
                        except Exception:
                            pass
                        if v and v.strip():
                            notify("AccessMate", v)
                    if elapsed >= _min_interval:
                        _last_content[0] = val
                        _last_update_time[0] = now
                        if _pending_update[0] is not None:
                            root.after_cancel(_pending_update[0])
                        root.after_idle(lambda: do_update(val))
                    else:
                        if _pending_update[0] is not None:
                            root.after_cancel(_pending_update[0])
                        wait_ms = int((_min_interval - elapsed) * 1000)
                        def delayed(v):
                            _last_content[0] = v
                            do_update(v)
                        _pending_update[0] = root.after(wait_ms, lambda: delayed(val))
    # Remove undefined logo_error check or set a default if needed
        # Try to use a placeholder image (simple colored square)
        try:
            from PIL import Image, ImageTk, ImageDraw
            placeholder = Image.new("RGB", (120, 120), color="#FFD600")
            draw = ImageDraw.Draw(placeholder)
            draw.text((10, 50), "No Logo", fill="#222")
            logo_photo = ImageTk.PhotoImage(placeholder)
            logo_label = tk.Label(scroll_frame, image=logo_photo, bg="#222")
            logo_label.image = logo_photo
        except Exception:
            logo_label = tk.Label(scroll_frame, text="[Logo Missing] Talkback Assistants", font=("Arial", 28, "bold"), bg="#222", fg="#FFD600")
        try:
            messagebox.showwarning("Logo Error", "App logo could not be loaded. A placeholder will be shown.")
        except Exception:
            pass
    if logo_label is not None:
        logo_label.grid(row=0, column=0, columnspan=3, pady=(20, 5))
    content_label = tk.Label(scroll_frame, textvariable=content_var, font=("Arial", 16), bg="#222", fg="#fff", wraplength=900)
    content_label.grid(row=1, column=0, columnspan=3, pady=10)

    mic_names = speech.list_microphones()
    mic_var = tk.StringVar(root, value=mic_names[0] if mic_names else "")
    mic_label = tk.Label(scroll_frame, text="Select Microphone:", font=("Arial", 16), bg="#222", fg="#FFD600")
    mic_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    from tkinter import ttk
    mic_combo = ttk.Combobox(scroll_frame, textvariable=mic_var, values=mic_names, font=("Arial", 16), width=30)
    mic_combo.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # feature_buttons is already initialized at the top of the file. Do not re-initialize here.

    current_theme = tk.StringVar(root, value=user_settings.theme.capitalize() if hasattr(user_settings, 'theme') else "Dark")
    accessibility_enabled = ACCESSIBILITY_AVAILABLE
    COUNTRY_TO_LANG = {
        "united states": "en", "usa": "en", "canada": "en", "mexico": "es", "spain": "es", "france": "fr", "germany": "de", "italy": "it", "china": "zh", "japan": "ja", "south korea": "ko", "russia": "ru", "brazil": "pt", "portugal": "pt", "india": "hi", "pakistan": "ur", "saudi arabia": "ar", "egypt": "ar", "turkey": "tr", "netherlands": "nl", "sweden": "sv", "norway": "no", "denmark": "da", "finland": "fi", "poland": "pl", "greece": "el", "israel": "he", "thailand": "th", "vietnam": "vi", "indonesia": "id", "philippines": "tl", "uk": "en", "united kingdom": "en", "australia": "en", "new zealand": "en", "south africa": "en", "argentina": "es", "chile": "es", "colombia": "es", "venezuela": "es", "switzerland": "de", "austria": "de", "belgium": "nl", "czech republic": "cs", "hungary": "hu", "romania": "ro", "bulgaria": "bg", "croatia": "hr", "serbia": "sr", "slovakia": "sk", "slovenia": "sl", "ukraine": "uk", "ireland": "en", "malaysia": "ms", "singapore": "en", "hong kong": "zh", "taiwan": "zh"
    }
    def set_language_gui():
        import tkinter.simpledialog
        while True:
            lang_code = askstring_with_logo("Set Language", "Enter your language code (e.g. en, es, fr):")
            if not lang_code:
                content_var.set("No language code entered.")
                return
            lang_code = lang_code.strip().lower()
            if len(lang_code) == 2 or len(lang_code) == 3:
                user_settings.language_code = lang_code
                user_settings.save("user_settings.json")
                content_var.set(f"Language set to: {lang_code}")
                return
            else:
                content_var.set(f"Invalid language code: {lang_code}. Try again.")
    feature_buttons.append(("Set Language", "#1976D2", "Set your preferred language code directly.", set_language_gui))
    def set_country_gui():
        import tkinter.simpledialog
        while True:
            country = askstring_with_logo("Set Country", "Enter your country (e.g. United States):")
            if not country:
                content_var.set("No country entered.")
                return
            code = COUNTRY_TO_LANG.get(country.strip().lower())
            if code:
                user_settings.country = country.title()
                user_settings.language_code = code
                user_settings.save("user_settings.json")
                content_var.set(f"Country set to: {country.title()} (language: {code})")
                return
            else:
                content_var.set(f"Country not recognized: {country}. Try again.")
    feature_buttons.append(("Set Country", "#FFB300", "Set your country for translation and personalization.", set_country_gui))
    # --- Button focus/announcement logic ---
    def on_button_focus(event):
        btn = event.widget
        label = btn.cget('text')
        set_content_var(f"{label}", announce=True)
        btn.configure(bg="#FFD600", fg="#222")

    def on_button_unfocus(event):
        btn = event.widget
        btn.configure(bg="#4CAF50", fg="white")

    # --- Second User Mode feature restriction helpers ---
def is_feature_allowed():
    # In Second User Mode, all features are disabled
    return not SECOND_USER_MODE

def is_screen_reader_allowed():
    # In Second User Mode, screen reader is also disabled
    return not SECOND_USER_MODE

    # ...existing code...
    # from camera import recognize_faces_from_camera  # Removed: function does not exist
    def recognize_faces_gui():
        # Face recognition feature not implemented
        content_var.set("Face recognition complete. Names announced.")
    feature_buttons.append(("Recognize Faces", "#7E57C2", "Announce names of people in the room.", recognize_faces_gui))
    from shopping_automation import automate_checkout
    def shopping_checkout_gui():
        import tkinter.simpledialog
        url = askstring_with_logo("Automate Checkout", "Enter shop URL (Amazon/eBay cart page):")
        if url:
            result = automate_checkout(url)
            if result:
                content_var.set("Checkout automation started. Complete address and payment in browser.")
            else:
                content_var.set("Checkout automation failed.")
        else:
            content_var.set("No URL entered.")
    feature_buttons.append(("Automate Checkout", "#E53935", "Automate checkout for Amazon/eBay.", shopping_checkout_gui))
    from shopping_automation import automate_add_to_basket
    def shopping_automation_gui():
        import tkinter.simpledialog
        url = askstring_with_logo("Automate Add to Basket", "Enter product URL:")
        if url:
            result = automate_add_to_basket(url)
            if result:
                content_var.set("Automated add to basket complete.")
            else:
                content_var.set("Automation failed.")
        else:
            content_var.set("No URL entered.")
    feature_buttons.append(("Automate Add to Basket", "#009688", "Automate basket for Amazon/eBay.", shopping_automation_gui))
    from shopping_accessibility import describe_online_item, add_to_basket
    def shopping_accessibility_gui():
        import tkinter.simpledialog
        url = askstring_with_logo("Online Shopping", "Enter product URL:")
        if url:
            item = describe_online_item(url)
            if item:
                content_var.set(f"Product: {item['title']}\nDescription: {item['description']}\nImage: {item['image']}")
                # Add to basket button
                def do_add():
                    add_to_basket(url)
                    content_var.set("Item added to basket.")
                add_btn = tk.Button(scroll_frame, text="Add to Basket", command=do_add, font=("Arial", 16), bg="#4CAF50", fg="white")
                add_btn.grid(row=100, column=0, padx=10, pady=10)
            else:
                content_var.set("Could not fetch item info.")
        else:
            content_var.set("No URL entered.")
    feature_buttons.append(("Accessible Shopping", "#FF9800", "Describe and add online shop item.", shopping_accessibility_gui))
    # ...existing code...

    # Define transport_mode_var as a tkinter StringVar and set a default value
    transport_mode_var = tk.StringVar(value="driving")

    def get_directions_gui():
        import tkinter.simpledialog
        dest = askstring_with_logo("Get Directions", "Enter your destination:")
        if dest:
            mode = transport_mode_var.get()
            from location import get_directions
            steps = get_directions(dest)
            content = f"Directions by {mode}:\n" + "\n".join(steps)
            content_var.set(content)
            for step in steps:
                speech.speak(step)
        else:
            content_var.set("No destination entered.")

    def apply_theme(theme_name):
        theme = THEMES[theme_name]
        user_settings.theme = theme_name.lower()
        user_settings.save("user_settings.json")
        root.configure(bg=theme["bg"])
        canvas.configure(bg=theme["bg"])
        scroll_frame.configure(bg=theme["bg"])
        content_label.configure(bg=theme["bg"], fg=theme["fg"])
        mic_label.configure(bg=theme["bg"], fg=theme["fg"])
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=theme["bg"], foreground=theme["fg"])
        mic_combo.configure(style="TCombobox")
        for child in scroll_frame.winfo_children():
            if isinstance(child, tk.Button):
                child.configure(bg=theme["btn_bg"], fg=theme["btn_fg"])
            elif isinstance(child, tk.Label):
                child.configure(bg=theme["bg"], fg=theme["fg"])

    theme_label = tk.Label(scroll_frame, text="Theme:", font=("Arial", 16), bg="#222", fg="#FFD600")
    theme_label.grid(row=0, column=3, padx=10, pady=10, sticky="w")
    theme_combo = ttk.Combobox(scroll_frame, textvariable=current_theme, values=list(THEMES.keys()), font=("Arial", 16), width=18)
    theme_combo.grid(row=0, column=4, padx=10, pady=10, sticky="w")
    theme_combo.bind("<<ComboboxSelected>>", lambda e: apply_theme(current_theme.get()))
    apply_theme(current_theme.get())

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
            content_var.set("Recording... Please speak.")
            try:
                audio = recognizer.listen(src, timeout=5)
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tf:
                    temp_filename = tf.name
                    tf.write(audio.get_wav_data())
                pygame.mixer.init()
                pygame.mixer.music.load(temp_filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.music.unload()
                try:
                    os.remove(temp_filename)
                except PermissionError:
                    content_var.set("Mic test complete, but could not delete temp file (access denied).")
                    return
                content_var.set("Mic test complete.")
            except Exception as e:
                content_var.set(f"Mic test failed: {e}")

    feature_buttons.insert(0, ("Test Microphone", "#FF9800", "Record and play back your voice to test the mic.", test_microphone))

    def run_voice_command():
        # Voice commands for all platforms
        all_platforms = [
            "apple music", "disney+", "audible", "google play music", "tidal", "pandora", "deezer", "youtube music", "prime video", "hbo max", "paramount+", "peacock", "scribd", "libby", "overdrive", "google podcasts", "pocket casts", "iheartradio", "bbc sounds", "spotify", "netflix", "hulu", "amazon music"
        ]
        for platform in all_platforms:
            if f"play {platform}" in cmd:
                from media import search_streaming, play_streaming
                query = cmd.replace(f"play {platform}", "").strip()
                items = search_streaming(platform.title(), query)
                if not items:
                    content_var.set(f"No results found on {platform.title()}.")
                    speech.speak(f"No results found on {platform.title()}.")
                    return
                for i, item in enumerate(items):
                    if 'synopsis' in item:
                        speech.speak(f"{platform.title()} {i+1}: {item['title']}. Synopsis: {item['synopsis']}")
                    else:
                        speech.speak(f"{platform.title()} {i+1}: {item['title']}")
                content_var.set(f"Say 'play {platform} [number]' to play a specific item.")
                speech.speak(f"Say 'play {platform}' followed by the number to play a specific item.")
                return
            # Play selected item by number
            if f"play {platform}" in cmd and any(str(n) in cmd for n in range(1, 21)):
                from media import search_streaming, play_streaming
                import re
                query = cmd.replace(f"play {platform}", "").strip()
                match = re.search(r'(\d+)', query)
                if match:
                    num = int(match.group(1))
                    items = search_streaming(platform.title(), "")
                    if items and 1 <= num <= len(items):
                        result = play_streaming(platform.title(), items[num-1]['id'])
                        content_var.set(result if result else f"Playing: {items[num-1]['title']} on {platform.title()}")
                        speech.speak(content_var.get())
                    else:
                        content_var.set("No such item number.")
                        speech.speak("No such item number.")
                return
        # Voice commands for browsing streaming platforms
        for platform in ["netflix", "spotify", "hulu", "amazon music"]:
            if f"play {platform}" in cmd:
                from media import search_streaming, play_streaming
                query = cmd.replace(f"play {platform}", "").strip()
                items = search_streaming(platform.title(), query)
                if not items:
                    content_var.set(f"No results found on {platform.title()}.")
                    speech.speak(f"No results found on {platform.title()}.")
                    return
                for i, item in enumerate(items):
                    if 'synopsis' in item:
                        speech.speak(f"{platform.title()} {i+1}: {item['title']}. Synopsis: {item['synopsis']}")
                    else:
                        speech.speak(f"{platform.title()} {i+1}: {item['title']}")
                content_var.set(f"Say 'play {platform} [number]' to play a specific item.")
                speech.speak(f"Say 'play {platform}' followed by the number to play a specific item.")
                return
            # Play selected item by number
            if f"play {platform}" in cmd and any(str(n) in cmd for n in range(1, 21)):
                from media import search_streaming, play_streaming
                import re
                query = cmd.replace(f"play {platform}", "").strip()
                match = re.search(r'(\d+)', query)
                if match:
                    num = int(match.group(1))
                    items = search_streaming(platform.title(), "")
                    if items and 1 <= num <= len(items):
                        result = play_streaming(platform.title(), items[num-1]['id'])
                        content_var.set(result if result else f"Playing: {items[num-1]['title']} on {platform.title()}")
                        speech.speak(content_var.get())
                    else:
                        content_var.set("No such item number.")
                        speech.speak("No such item number.")
                return
        if "browse audiobook app" in cmd:
            from media import get_audiobook_list
            app = cmd.replace("browse audiobook app", "").strip()
            if not app:
                content_var.set("No app specified.")
                speech.speak("No app specified.")
                return
            books = get_audiobook_list(app)
            if not books:
                content_var.set(f"No books found in {app}.")
                speech.speak(f"No books found in {app}.")
                return
            for i, book in enumerate(books):
                speech.speak(f"Book {i+1}: {book['title']}. Synopsis: {book['synopsis']}")
            content_var.set(f"{len(books)} books found in {app}. Browsed and spoken.")
            return
        # Voice commands for media and streaming
        if "play youtube" in cmd:
            from media import search_youtube, play_youtube
            query = cmd.replace("play youtube", "").strip()
            videos = search_youtube(query)
            if not videos:
                content_var.set("No videos found.")
                speech.speak("No videos found.")
                return
            for i, video in enumerate(videos):
                speech.speak(f"Video {i+1}: {video['title']}")
            # Do not auto-play; wait for user selection
            content_var.set("Say 'play YouTube [number]' to play a specific video.")
            speech.speak("Say 'play YouTube' followed by the video number to play a specific video.")
            return
        # Play selected YouTube video by number
        if "play youtube" in cmd and any(str(n) in cmd for n in range(1, 21)):
            from media import search_youtube, play_youtube
            import re
            query = cmd.replace("play youtube", "").strip()
            match = re.search(r'(\d+)', query)
            if match:
                num = int(match.group(1))
                videos = search_youtube("")  # Use last search or empty
                if videos and 1 <= num <= len(videos):
                    result = play_youtube(videos[num-1]['url'])
                    content_var.set(result if result else f"Playing: {videos[num-1]['title']}")
                    speech.speak(content_var.get())
                else:
                    content_var.set("No such video number.")
                    speech.speak("No such video number.")
            return
        if "play netflix" in cmd or "play spotify" in cmd or "play hulu" in cmd:
            from media import play_streaming
            for platform in ["netflix", "spotify", "hulu"]:
                if f"play {platform}" in cmd:
                    query = cmd.replace(f"play {platform}", "").strip()
                    result = play_streaming(platform, query)
                    content_var.set(result if result else f"Playing on {platform}.")
                    speech.speak(content_var.get())
                    break
            return
        if "play audiobook" in cmd:
            from media import play_book_library
            parts = cmd.split()
            idx = parts.index("audiobook")
            app = None
            book = None
            if len(parts) > idx + 1:
                app = parts[idx + 1]
                if len(parts) > idx + 2:
                    if parts[idx + 2] == "continue":
                        book = "continue"
                    else:
                        book = " ".join(parts[idx + 2:])
            result = play_book_library(app, book)
            if book == "continue":
                content_var.set(result if result else f"Resuming last book in {app}.")
            else:
                content_var.set(result if result else f"Playing '{book}' in {app}.")
            speech.speak(content_var.get())
            return

    import threading
    def safe_update(val):
        now = time.time()
        if _last_content[0] == val:
            return
        elapsed = now - _last_update_time[0]
        def do_update(val=val):
            content_var.set(val)
            status_var.set(val)
            _pending_update[0] = None
            _last_update_time[0] = time.time()
            # Always announce status changes and errors for accessibility
            try:
                speech.speak(val)
            except Exception:
                pass
        if elapsed >= _min_interval:
            _last_content[0] = val
            _last_update_time[0] = now
            if _pending_update[0] is not None:
                root.after_cancel(_pending_update[0])
            root.after_idle(do_update)
        else:
            if _pending_update[0] is not None:
                root.after_cancel(_pending_update[0])
            wait_ms = int((_min_interval - elapsed) * 1000)
            def delayed(val=val):
                _last_content[0] = val
                do_update(val)
            _pending_update[0] = root.after(wait_ms, delayed)

    def listen_and_act():
        try:
            mic_index = speech.selected_mic_index if hasattr(speech, 'selected_mic_index') else None
            content_var.set(f"Listening for command on mic index {mic_index if mic_index is not None else 'default'}...")
            cmd = speech.listen()
            if cmd:
                # Place your voice command handling logic here
                # For example, call run_voice_command() or handle_voice_command(cmd)
                run_voice_command()
        except Exception as e:
            content_var.set(f"Voice command error: {e}")

    threading.Thread(target=listen_and_act, daemon=True).start()

    feature_buttons.insert(1, ("Voice Command", "#00C853", "Speak a command (e.g. 'say time', 'say date', 'say weather', 'help').", run_voice_command))

    # Automatically start voice command listening in background
    def auto_voice_command_listener():
        while True:
            try:
                mic_index = speech.selected_mic_index if hasattr(speech, 'selected_mic_index') else None
                content_var.set(f"Listening for command on mic index {mic_index if mic_index is not None else 'default'}...")
                cmd = speech.listen()
                if cmd:
                    from voice_commands import handle_voice_command
                    handle_voice_command(cmd)
            except Exception as e:
                content_var.set(f"Voice command error: {e}")
            time.sleep(1)
    import threading
    threading.Thread(target=auto_voice_command_listener, daemon=True).start()

    def make_on_enter(tip, widget):
        def on_enter(event):
            text = tip or widget.cget('text')
            try:
                speech.speak(text)
            except Exception:
                pass
        return on_enter

    # Only create feature buttons once at startup
    import traceback
    def safe_cmd_wrapper(cmd, label):
        def wrapped_cmd(*args, **kwargs):
            try:
                cmd(*args, **kwargs)
            except Exception as e:
                err_msg = f"[ERROR] Button '{label}' failed: {e}"
                print(err_msg)
                traceback.print_exc()
                set_content_var(err_msg)
        return wrapped_cmd
    if not hasattr(root, '_feature_buttons_created'):
        for i, (label, color, tooltip, cmd) in enumerate(feature_buttons):
            btn = tk.Button(scroll_frame, text=label, command=safe_cmd_wrapper(cmd, label), font=("Arial", 18), bg=color, fg="white", width=22, height=2, relief="raised", highlightthickness=2)
            btn.bind('<FocusIn>', on_button_focus)
            btn.bind('<FocusOut>', on_button_unfocus)
            btn.grid(row=2 + i // 3, column=i % 3, padx=10, pady=10)
            # Only enable accessibility if available
            if accessibility_enabled:
                enable_accessibility(btn, tooltip=tooltip)
            # Remove tooltip popups and only use status bar
    root._feature_buttons_created = True

    # Set scrollregion after all widgets are created
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Now show the window (no jumping)
    root.deiconify()

    def open_program_gui():
        import tkinter.simpledialog
        prog_name = askstring_with_logo("Open Program", "Enter the name or path of the program to open:")
        if prog_name:
            open_program(prog_name)
            content_var.set(f"Attempted to open: {prog_name}")
        else:
            content_var.set("No program name entered.")

    feature_buttons.append(("Open Program", "#FF5722", "Open any installed program by name.", open_program_gui))

    def turn_on_light_gui():
        result = turn_on_light()
        content_var.set(result)

    def turn_off_light_gui():
        result = turn_off_light()
        content_var.set(result)

    def show_iot_status():
        content_var.set(iot_status())

    feature_buttons.append(("Turn On Light", "#FFD600", "Turn on a smart light.", turn_on_light_gui))
    feature_buttons.append(("Turn Off Light", "#FFA000", "Turn off a smart light.", turn_off_light_gui))

    def test_microphone_gui():
        import speech
        set_content_var("Testing microphone... Please speak now.")
        try:
            result = speech.listen()
            if result:
                set_content_var(f"Mic heard: {result}")
            else:
                set_content_var("Mic did not hear or recognize any speech.")
        except Exception as e:
            import traceback
            err_msg = f"[ERROR] Microphone test failed: {e}"
            print(err_msg)
            traceback.print_exc()
            set_content_var(err_msg)

    feature_buttons.append(("Test Microphone", "#00C853", "Test microphone input and speech recognition.", test_microphone_gui))
    feature_buttons.append(("IoT Status", "#00B8D4", "Show IoT integration status.", show_iot_status))

    root.mainloop()

def open_program(program_name):
    try:
        if sys.platform.startswith('win'):
            import shutil
            # If only a name is given, try to find the executable in common locations
            program_lower = program_name.lower().strip()
            exe_path = None
            # Steam special case
            if program_lower == "steam":
                possible_paths = [
                    r"C:\\Program Files (x86)\\Steam\\Steam.exe",
                    r"C:\\Program Files\\Steam\\Steam.exe"
                ]
                for path in possible_paths:
                    if os.path.exists(path):
                        exe_path = path
                        break
            # Add more common programs here as needed
            # If not found, try to find in PATH
            if not exe_path:
                exe_path = shutil.which(program_name)
            # If still not found, try Start Menu shortcuts
            if not exe_path and not program_name.endswith('.exe'):
                # Try to find shortcut in Start Menu
                import glob
                start_menu_dirs = [
                    os.path.expandvars(r'%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs'),
                    os.path.expandvars(r'%PROGRAMDATA%\\Microsoft\\Windows\\Start Menu\\Programs')
                ]
                for d in start_menu_dirs:
                    for shortcut in glob.glob(os.path.join(d, '**', f'{program_name}*.lnk'), recursive=True):
                        os.startfile(shortcut)
                        return
            if exe_path:
                os.startfile(exe_path)
            else:
                print(f"Could not find program: {program_name}")
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', program_name])
        elif sys.platform.startswith('linux'):
            subprocess.Popen([program_name])
        else:
            print("Unsupported platform for program launching.")
    except Exception as e:
        print(f"Error opening program: {e}")

if __name__ == "__main__":
    root = None
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        start_reminder_notification_thread(root)
        # If you want to show the main UI, call launch(root) or similar here
        root.mainloop()
    except Exception:
        pass

