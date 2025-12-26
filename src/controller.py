from datetime import datetime
from functools import partial
from src.memo import Memo
from src.model import MemoModel
from src.view import View

class Controller:
    """
    Connects the Model and the View, and handles the application's logic.
    """

    def __init__(self, model: MemoModel, view: View):
        """Initializes the controller, binds events, and loads initial data."""
        self.model = model
        self.view = view
        self._memos_cache: list[Memo] = []  # Cache to hold the current list of memos

        self._bind_events()
        self.load_initial_data()

    def _bind_events(self):
        """Binds view events to controller methods."""
        self.view.bind_save_button(self._handle_save)
        self.view.bind_memo_selection(self._handle_memo_select)

    def load_initial_data(self):
        """Loads all memos from the model and updates the view."""
        self._memos_cache = self.model.get_all_memos()
        self.view.update_memo_list(self._memos_cache)

    def _handle_save(self):
        """Handles the save button click event."""
        title = self.view.get_title()
        content = self.view.get_content()

        if not title:
            # Optionally, show an error message via the view
            return

        # Generate a new memo
        now = datetime.now()
        new_memo = Memo(
            id=str(int(now.timestamp())),
            title=title,
            content=content,
            timestamp=now.strftime("%Y-%m-%d %H:%M:%S")
        )

        # Save it and reload the list
        self.model.save_memo(new_memo)
        self.view.clear_input_fields()
        self.load_initial_data() # Reload all to reflect the new state

    def _handle_memo_select(self, event):
        """Handles the memo selection event in the listbox."""
        selected_timestamp = self.view.get_selected_memo_timestamp()
        if not selected_timestamp:
            return

        # Find the memo in the cache
        selected_memo = None
        for memo in self._memos_cache:
            if memo.timestamp == selected_timestamp:
                selected_memo = memo
                break

        if selected_memo:
            # Create partial functions for the handlers to pass the memo_id
            update_handler = partial(self._handle_update, selected_memo.id)
            delete_handler = partial(self._handle_delete, selected_memo.id)
            self.view.show_detail_window(selected_memo, update_handler, delete_handler)

    def _handle_update(self, memo_id: str, new_content: str):
        """Handles the update button click in the detail window."""
        # Find the memo to update
        memo_to_update = None
        for memo in self._memos_cache:
            if memo.id == memo_id:
                memo_to_update = memo
                break

        if memo_to_update:
            # Update its content and timestamp
            memo_to_update.content = new_content
            memo_to_update.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.model.save_memo(memo_to_update) # Save overwrites the existing file
            self.load_initial_data() # Reload to reflect updated list

    def _handle_delete(self, memo_id: str):
        """Handles the delete button click in the detail window."""
        self.model.delete_memo(memo_id)
        self.load_initial_data() # Reload to reflect updated list
