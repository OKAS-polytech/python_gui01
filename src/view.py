import tkinter as tk
from tkinter import messagebox
from typing import Callable
from src.memo import Memo

class View:
    """Handles the GUI of the memo application."""

    def __init__(self, window: tk.Tk):
        """Initializes the View and creates all UI widgets."""
        self.window = window
        self.window.title("簡易メモアプリ (MVC)")
        self.window.geometry("600x400")

        # To store the ID of the memo currently in the detail view
        self._detail_view_memo_id = None

        self._create_widgets()

    def _create_widgets(self):
        """Creates and places all widgets in the main window."""
        # Main frame
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left frame for input
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        tk.Label(left_frame, text="タイトル").pack(anchor=tk.W)
        self.title_entry = tk.Entry(left_frame)
        self.title_entry.pack(fill=tk.X)

        tk.Label(left_frame, text="本文").pack(anchor=tk.W, pady=(10, 0))
        self.content_text = tk.Text(left_frame, height=10)
        self.content_text.pack(fill=tk.BOTH, expand=True)

        self.save_button = tk.Button(left_frame, text="保存")
        self.save_button.pack(pady=5)

        # Right frame for the list
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        tk.Label(right_frame, text="メモ一覧").pack(anchor=tk.W)
        self.memo_listbox = tk.Listbox(right_frame)
        self.memo_listbox.pack(fill=tk.BOTH, expand=True)

    # --- Methods for Controller to bind events ---
    def bind_save_button(self, handler: Callable[[], None]):
        """Binds the save button's click event to a handler."""
        self.save_button.config(command=handler)

    def bind_memo_selection(self, handler: Callable[[tk.Event], None]):
        """Binds the listbox selection event to a handler."""
        self.memo_listbox.bind('<<ListboxSelect>>', handler)

    # --- Methods for Controller to update the view ---
    def update_memo_list(self, memos: list[Memo]):
        """Clears and repopulates the memo listbox."""
        self.memo_listbox.delete(0, tk.END)
        for memo in memos:
            # Store the ID in a way that can be retrieved, e.g., by associating with the list item
            self.memo_listbox.insert(tk.END, f"{memo.title} - {memo.timestamp}")

    def clear_input_fields(self):
        """Clears the title and content entry fields."""
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)

    # --- Methods for Controller to get data from the view ---
    def get_title(self) -> str:
        """Returns the current text in the title entry."""
        return self.title_entry.get()

    def get_content(self) -> str:
        """Returns the current text in the content text area."""
        return self.content_text.get("1.0", tk.END).strip()

    def get_selected_memo_timestamp(self) -> str | None:
        """Returns the timestamp part of the selected item in the listbox."""
        selected_indices = self.memo_listbox.curselection()
        if not selected_indices:
            return None

        selected_string = self.memo_listbox.get(selected_indices[0])
        try:
            # Assumes format "Title - YYYY-MM-DD HH:MM:SS"
            return selected_string.split(" - ", 1)[1]
        except IndexError:
            return None

    # --- Detail Window ---
    def show_detail_window(self, memo: Memo, update_handler: Callable, delete_handler: Callable):
        """Creates and displays the memo detail window."""
        detail_window = tk.Toplevel(self.window)
        detail_window.title("メモ詳細")
        detail_window.geometry("400x300")
        detail_window.transient(self.window) # Keep it on top of the main window

        content_text = tk.Text(detail_window)
        content_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        content_text.insert(tk.END, memo.content)

        button_frame = tk.Frame(detail_window)
        button_frame.pack(pady=5)

        # The handlers passed here are already configured by the Controller
        # to know which memo they are operating on.
        update_button = tk.Button(button_frame, text="更新",
                                  command=lambda: [update_handler(content_text.get("1.0", tk.END).strip()), detail_window.destroy()])
        update_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, text="削除",
                                  command=lambda: [delete_handler(), detail_window.destroy()])
        delete_button.pack(side=tk.LEFT, padx=5)
