import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from media_sort.core import run_media_sort, base_dir, show_splash_screen #core.pyをインポート
import sys
import os

#スプラッシュ画像のパス
if getattr(sys, 'frozen', False):  # EXE起動時
    splash_path = Path(sys._MEIPASS) / "assets" / "MediaSort_splash.png"
else:  # 通常Python実行時
    splash_path = Path(__file__).resolve().parent.parent / "assets" / "MediaSort_splash.png"

#splash_path = Path(__file__).resolve().parent.parent / "assets" / "MediaSort_splash.png"
show_splash_screen(splash_path)

class MediaSortApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MediaSort")

        #入出力パス初期値
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()

        # 追加（レイアウト拡張）
        # 幅と高さ方向の追従設定
        root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

        #GUI構築
        tk.Label(root, text="入力フォルダ：").grid(row=0, column=0, sticky="e")
        tk.Entry(root, textvariable= self.input_path, width=40).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(root, text="参照", command=self.browse_input).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(root, text="出力フォルダ：").grid(row=1, column=0, sticky="e")
        tk.Entry(root, textvariable= self.output_path, width=40).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(root, text="参照", command=self.browse_output).grid(row=1, column=2, padx=5, pady=5)
        
        tk.Button(root, text="実行", command=self.run_sort).grid(row=2, column=1, pady=15)
            
    def browse_input(self):
        path = filedialog.askdirectory()
        if path:
            self.input_path.set(path)

    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def run_sort(self):
        input_folder = Path(self.input_path.get())
        output_folder = Path(self.output_path.get())

        if not input_folder or not output_folder:
            messagebox.showwarning("警告", "入力または出力フォルダが無効です。")
            return
        
        try:
            run_media_sort(input_folder, output_folder, splash=True,splash_path=splash_path)
            messagebox.showinfo("完了", "メディアの整理が完了しました。")
        except Exception as e:
            messagebox.showerror("エラー", f"処理中に問題が発生しました:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaSortApp(root)
    root.mainloop()

"""
# GUI画面の構築
root = tk.Tk()
root.title("MediaSort - フォルダ選択")
root.geometry("400x200")

tk.Label(root, text="入力フォルダ").pack(pady=5)
input_entry = tk.Entry(root, width=40)
input_entry.pack()
tk.Button(root, text="参照...", command=browse_input).pack()

tk.Label(root, text="出力フォルダ").pack(pady=5)
output_entry = tk.Entry(root, width=40)
output_entry.pack()
tk.Button(root, text="参照...", command=browse_output).pack()

tk.Button(root, text="実行", command=run_mediasort, bg="lightblue").pack(pady=10)

root.mainloop()
"""