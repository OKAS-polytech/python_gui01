import os
import glob
from src.memo import Memo

class MemoModel:
    """Handles data persistence for memos by reading from and writing to files."""

    def __init__(self, data_dir="data"):
        """Initializes the model and ensures the data directory exists."""
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def get_all_memos(self) -> list[Memo]:
        """
        Reads all memo files from the data directory and returns them as a list of Memo objects.
        Memos are sorted by timestamp in descending order (most recent first).
        """
        memos = []
        filepaths = glob.glob(os.path.join(self.data_dir, "*.txt"))
        for filepath in filepaths:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) >= 2: # Title and timestamp are required
                        memo_id = os.path.basename(filepath).replace('.txt', '')
                        title = lines[0].strip()
                        timestamp = lines[1].strip()
                        content = "".join(lines[2:])
                        memos.append(Memo(id=memo_id, title=title, content=content, timestamp=timestamp))
            except IOError as e:
                print(f"Error reading file {filepath}: {e}")

        # Sort by timestamp, newest first
        return sorted(memos, key=lambda m: m.timestamp, reverse=True)

    def save_memo(self, memo: Memo):
        """Saves a single memo object to a text file."""
        filepath = os.path.join(self.data_dir, f"{memo.id}.txt")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"{memo.title}\\n")
                f.write(f"{memo.timestamp}\\n")
                f.write(memo.content)
        except IOError as e:
            print(f"Error saving file {filepath}: {e}")

    def delete_memo(self, memo_id: str):
        """Deletes the text file associated with the given memo ID."""
        filepath = os.path.join(self.data_dir, f"{memo_id}.txt")
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError as e:
                print(f"Error deleting file {filepath}: {e}")
        else:
            print(f"File not found for deletion: {filepath}")
