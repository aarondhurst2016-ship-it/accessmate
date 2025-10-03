# Simple admin tool for replying to in-app support messages

import json
import tkinter as tk
from tkinter import simpledialog, messagebox
import datetime

MESSAGE_FILE = "support_messages.json"
PASSWORD = "Esme222024"  # Custom password
ADMIN_EMAIL = "aarondhurst2017@gmail.com"

def load_messages():
    try:
        with open(MESSAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_messages(msgs):
    with open(MESSAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(msgs, f, indent=2)

def main():
    root = tk.Tk()
    root.withdraw()
    # Password protection
    import smtplib
    import random
    from email.message import EmailMessage
    # PASSWORD and ADMIN_EMAIL are now module-level globals
    def send_reset_code(code):
        msg = EmailMessage()
        msg['Subject'] = 'AccessMate Admin Tool Password Reset'
        msg['From'] = ADMIN_EMAIL
        msg['To'] = ADMIN_EMAIL
        msg.set_content(f"Your AccessMate admin tool reset code is: {code}")
        # You must configure your SMTP credentials here
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = ADMIN_EMAIL
        smtp_pass = 'tghy qjtz wnwm rzkk'  # Use an app password for Gmail
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            return True
        except Exception as e:
            tk.messagebox.showerror("Email Error", f"Failed to send reset code: {e}")
            return False
    def prompt_password():
        global PASSWORD
        pw = tk.simpledialog.askstring("Admin Login", "Enter admin password:", show="*")
        if pw == PASSWORD:
            return True
        if pw is None:
            root.destroy()
            return False
        if tk.messagebox.askyesno("Forgot Password?", "Incorrect password. Forgot password?"):
            code = str(random.randint(100000, 999999))
            if send_reset_code(code):
                entered = tk.simpledialog.askstring("Reset Code", "A reset code was sent to your email. Enter it:")
                if entered == code:
                    new_pw = tk.simpledialog.askstring("Set New Password", "Enter new password:", show="*")
                    if new_pw:
                        PASSWORD = new_pw
                        tk.messagebox.showinfo("Password Reset", "Password updated. Please log in again.")
                        return prompt_password()
            root.destroy()
            return False
        else:
            tk.messagebox.showerror("Access Denied", "Incorrect password. Exiting.")
            root.destroy()
            return False
    if not prompt_password():
        return
    root.deiconify()
    root.title("Support Message Admin Tool")
    root.geometry("600x400")
    root.configure(bg="#222")
    tk.Label(root, text="Support Message Admin Tool", font=("Arial", 15, "bold"), bg="#222", fg="#FFD600").pack(pady=10)
    frame = tk.Frame(root, bg="#222")
    frame.pack(fill="both", expand=True, padx=10, pady=5)
    msg_list = tk.Listbox(frame, font=("Arial", 11), bg="#111", fg="#fff", height=12, width=30)
    msg_list.pack(side="left", fill="y", expand=False)
    msg_text = tk.Text(frame, font=("Arial", 11), bg="#333", fg="#fff", width=50, height=12, state="disabled", wrap="word")
    msg_text.pack(side="right", fill="both", expand=True)
    status_var = tk.StringVar()
    tk.Label(root, textvariable=status_var, font=("Arial", 11), bg="#222", fg="#FFD600").pack(pady=2)
    def refresh_messages():
        messages = load_messages()
        msg_list.delete(0, tk.END)
        for i, msg in enumerate(messages):
            who = "User" if msg.get("from") == "user" else "Support"
            preview = msg.get("message", "")[:60].replace("\n", " ")
            msg_list.insert(tk.END, f"[{who}] {preview}")
    def on_select(event):
        idx = msg_list.curselection()
        if not idx:
            return
        messages = load_messages()
        msg = messages[idx[0]]
        who = "User" if msg.get("from") == "user" else "Support"
        msg_text.config(state="normal")
        msg_text.delete("1.0", tk.END)
        msg_text.insert(tk.END, f"{who} ({msg.get('timestamp','')}):\n\n{msg.get('message','')}")
        msg_text.config(state="disabled")
    def reply_to_message():
        idx = msg_list.curselection()
        if not idx:
            status_var.set("Select a user message to reply.")
            return
        messages = load_messages()
        msg = messages[idx[0]]
        if msg.get("from") != "user":
            status_var.set("Select a user message to reply.")
            return
        reply = simpledialog.askstring("Reply to User", "Enter your reply:")
        if not reply:
            return
        messages.append({
            "from": "support",
            "message": reply,
            "timestamp": datetime.datetime.now().isoformat()
        })
        save_messages(messages)
        status_var.set("Reply sent. User will see it in-app.")
        refresh_messages()
    msg_list.bind('<<ListboxSelect>>', on_select)
    tk.Button(root, text="Reply to Selected", command=reply_to_message, font=("Arial", 12), bg="#43A047", fg="#fff").pack(pady=6)
    tk.Button(root, text="Refresh", command=refresh_messages, font=("Arial", 12), bg="#1976D2", fg="#fff").pack(pady=2)
    tk.Button(root, text="Close", command=root.destroy, font=("Arial", 12), bg="#D32F2F", fg="#fff").pack(pady=2)
    refresh_messages()
    root.mainloop()

if __name__ == "__main__":
    main()
