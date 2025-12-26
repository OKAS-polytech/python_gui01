import tkinter as tk
from datetime import datetime

class MemoApp:
    def __init__(self, window):
        self.window = window
        self.window.title("簡易メモアプリ")
        self.window.geometry("600x400")
        self.memos = []
        self.create_widgets()

    def save_memo(self):
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()

        if not title:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        memo_id = int(datetime.now().timestamp())

        memo = {
            "id": memo_id,
            "title": title,
            "content": content,
            "timestamp": timestamp
        }
        self.memos.append(memo)
        self.update_memo_list()

        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)

    def update_memo_list(self):
        self.memo_listbox.delete(0, tk.END)
        for memo in self.memos:
            self.memo_listbox.insert(tk.END, f"{memo['title']} - {memo['timestamp']}")

    def on_memo_select(self, event):
        selected_indices = self.memo_listbox.curselection()
        if not selected_indices:
            return

        selected_string = self.memo_listbox.get(selected_indices[0])
        timestamp_str = selected_string.split(" - ")[-1]

        selected_memo = None
        for memo in self.memos:
            if memo['timestamp'] == timestamp_str:
                selected_memo = memo
                break

        if selected_memo:
            self.show_detail_window(selected_memo)

    def show_detail_window(self, memo):
        detail_window = tk.Toplevel(self.window)
        detail_window.title("メモ詳細")
        detail_window.geometry("400x300")

        content_text = tk.Text(detail_window)
        content_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        content_text.insert(tk.END, memo['content'])

        button_frame = tk.Frame(detail_window)
        button_frame.pack(pady=5)

        update_button = tk.Button(button_frame, text="更新", command=lambda: self.update_memo(memo['id'], content_text.get("1.0", tk.END).strip(), detail_window))
        update_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, text="削除", command=lambda: self.delete_memo(memo['id'], detail_window))
        delete_button.pack(side=tk.LEFT, padx=5)

    def update_memo(self, memo_id, new_content, detail_window):
        for memo in self.memos:
            if memo['id'] == memo_id:
                memo['content'] = new_content
                memo['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break

        detail_window.destroy()
        self.update_memo_list()

    def delete_memo(self, memo_id, detail_window):
        self.memos = [memo for memo in self.memos if memo['id'] != memo_id]
        detail_window.destroy()
        self.update_memo_list()

    def create_widgets(self):
        # メインフレーム
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左フレーム
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        tk.Label(left_frame, text="タイトル").pack(anchor=tk.W)
        self.title_entry = tk.Entry(left_frame)
        self.title_entry.pack(fill=tk.X)

        tk.Label(left_frame, text="本文").pack(anchor=tk.W, pady=(10, 0))
        self.content_text = tk.Text(left_frame, height=10)
        self.content_text.pack(fill=tk.BOTH, expand=True)

        self.save_button = tk.Button(left_frame, text="保存", command=self.save_memo)
        self.save_button.pack(pady=5)

        # 右フレーム
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        tk.Label(right_frame, text="メモ一覧").pack(anchor=tk.W)
        self.memo_listbox = tk.Listbox(right_frame)
        self.memo_listbox.pack(fill=tk.BOTH, expand=True)
        self.memo_listbox.bind('<<ListboxSelect>>', self.on_memo_select)

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoApp(root)
    root.mainloop()
