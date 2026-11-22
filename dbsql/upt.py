import json
import tkinter as tk
from tkinter import ttk, messagebox


def expand_spec(spec: str) -> list[int]:
    """Ператварае '1-4, 7, 9-10' у дакладны спіс лікаў."""
    result = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = map(int, part.split("-", 1))
            if start > end:
                raise ValueError(f"Няправільны дыяпазон: {part}")
            result.extend(range(start, end + 1))
        else:
            result.append(int(part))
    return result


class TopicBuilderApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Канструктар тэм і JSON для Blagobot")
        self.root.geometry("820x620")

        self.blocks: list[dict] = []
        # self._init_db_table()
        self._build_ui()

    
    def _build_ui(self):
        # --- Верхняя панэль: Дзень, Нумар тэмы, Назва ---
        top_frame = ttk.LabelFrame(self.root, text="1. Параметры тэмы", padding=10)
        top_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(top_frame, text="Дзень (1-90):").grid(row=0, column=0, sticky="w")
        self.day_var = tk.IntVar(value=1)
        ttk.Spinbox(top_frame, from_=1, to=90, textvariable=self.day_var, width=5).grid(row=0, column=1, padx=5)

        ttk.Label(top_frame, text="Тэма № (1-8):").grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.order_var = tk.IntVar(value=1)
        ttk.Spinbox(top_frame, from_=1, to=8, textvariable=self.order_var, width=5).grid(row=0, column=3, padx=5)

        ttk.Label(top_frame, text="Назва тэмы:").grid(row=0, column=4, sticky="w", padx=(10, 0))
        self.title_var = tk.StringVar()
        ttk.Entry(top_frame, textvariable=self.title_var, width=30).grid(row=0, column=5, padx=5, sticky="ew")
        ttk.Label(top_frame, text="/    ").grid(row=0, column=9)
        ttk.Label(top_frame, text="/    ").grid(row=0, column=10)
    
        # --- Панэль дадання блока цытат ---
        block_frame = ttk.LabelFrame(self.root, text="2. Дадаць спасылку на цытаты", padding=10)
        block_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(block_frame, text="Пазіція у тэме:").grid(row=0, column=0)
        self.book_var = tk.StringVar(value="1")
        ttk.Entry(block_frame, textvariable=self.book_var, width=6).grid(row=0, column=1, padx=5)
        

        ttk.Label(block_frame, text="Кніга (ID):").grid(row=0, column=2)
        self.book_var = tk.StringVar(value="1")
        ttk.Entry(block_frame, textvariable=self.book_var, width=6).grid(row=0, column=3, padx=5)

        ttk.Label(block_frame, text="Глава:").grid(row=0, column=5)
        self.chap_var = tk.StringVar(value="1")
        ttk.Entry(block_frame, textvariable=self.chap_var, width=6).grid(row=0, column=6, padx=5)

        ttk.Label(block_frame, text="/    ").grid(row=0, column=7)
        ttk.Label(block_frame, text="/    ").grid(row=0, column=8)
        ttk.Label(block_frame, text="/    ").grid(row=0, column=9)
        ttk.Label(block_frame, text="/    ").grid(row=0, column=10)

        ttk.Label(block_frame, text="Цытаты (напр. 1-4 або 2, 5):").grid(row=1, column=0, columnspan=3, padx=5)
        self.quotes_var = tk.StringVar()
        q_entry = ttk.Entry(block_frame, textvariable=self.quotes_var, width=20)
        q_entry.grid(row=1, column=3, columnspan=8, sticky="WE", padx=5)
        q_entry.bind("<Return>", lambda e: self.add_block())  # Даданне па Enter!

        ttk.Button(block_frame, text="➕ Дадаць блок", command=self.add_block).grid(row=0, column=10,  pady=5, padx=5)
        ttk.Button(block_frame, text="🗑 Ачысціць усе", command=self.clear_blocks).grid(row=0, column=9, padx=5)

        # --- Сярэдняя частка: Спіс блокаў + Перадпрагляд тэксту з БД ---
        mid_frame = ttk.Frame(self.root)
        mid_frame.pack(fill="both", expand=True, padx=10, pady=5)

        left_box = ttk.LabelFrame(mid_frame, text="Склад тэмы (JSON)", padding=5)
        left_box.pack(side="left", fill="both", expand=False)

        self.blocks_listbox = tk.Listbox(left_box, width=32, font=("Consolas", 10))
        self.blocks_listbox.pack(fill="both", expand=True)
        ttk.Button(left_box, text="Выдаліць выбраны блок", command=self.remove_selected_block).pack(fill="x", pady=(5, 0))

        right_box = ttk.LabelFrame(mid_frame, text="Перадпрагляд тэксту з вашай базы SQLite", padding=5)
        right_box.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.preview_text = tk.Text(right_box, wrap="word", font=("Sans", 10), state="disabled", bg="#f8f9fa")
        self.preview_text.pack(fill="both", expand=True)

        # --- Ніжняя панэль: Захаванне ---
        bot_frame = ttk.Frame(self.root, padding=10)
        bot_frame.pack(fill="x")

        self.status_lbl = ttk.Label(bot_frame, text="Гатова да працы", foreground="gray")
        self.status_lbl.pack(side="left")

        ttk.Button(
            bot_frame,
            text="💾 Захаваць у БД і перайсці да наступнай тэмы",
            #command=self.save_and_next,
        ).pack(side="right")

    def add_block(self):
        try:
            book_id = int(self.book_var.get().strip())
            chapter = int(self.chap_var.get().strip())
            raw_q = self.quotes_var.get().strip()
            if not raw_q:
                return

            # Правяраем, што дыяпазон карэктны
            q_nums = expand_spec(raw_q)
            if not q_nums:
                return

            # Калі ўведзены адзін дыяпазон накшталт "1-4", захоўваем радком, інакш спісам лікаў
            q_val = raw_q if ("-" in raw_q and "," not in raw_q) else q_nums
            block = {"b": book_id, "c": chapter, "q": q_val}

            self.blocks.append(block)
            self.quotes_var.set("")  # Ачышчаем поле цытат для хуткага ўводу наступных
            self._refresh_ui()
        except Exception as e:
            messagebox.showerror("Памылка ўводу", f"Праверце лічбы:\n{e}")

    def remove_selected_block(self):
        sel = self.blocks_listbox.curselection()
        if sel:
            del self.blocks[sel[0]]
            self._refresh_ui()

    def clear_blocks(self):
        self.blocks.clear()
        self._refresh_ui()

    def _refresh_ui(self):
        # Абнаўляем спіс блокаў злева
        self.blocks_listbox.delete(0, tk.END)
        for b in self.blocks:
            self.blocks_listbox.insert(tk.END, json.dumps(b, ensure_ascii=False))

        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", tk.END)
        # self.preview_text.insert("1.0", "\n".join(lines))
        self.preview_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = TopicBuilderApp(root)
    root.mainloop()
