# file_manager.py
# File management feature


def search_files(query):
    # Mobile-friendly file search using Kivy FileChooser
    try:
        from kivy.uix.filechooser import FileChooserListView
        chooser = FileChooserListView()
        # Filter files by query
        files = [f for f in chooser.files if query.lower() in f.lower()]
        return files
    except Exception:
        return []


def open_file(path):
    # Mobile-friendly file open using Kivy
    try:
        import os
        if os.path.exists(path):
            # On mobile, opening a file may mean displaying or sharing
            from kivy.core.window import Window
            Window.open_file(path)
            return True
        return False
    except Exception:
        return False
