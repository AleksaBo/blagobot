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
        self.root.geometry("520x320")

        self.blocks: list[dict] = []
        # self._init_db_table()
        self._build_ui()

    # def _connect(self):
    #     return sqlite3.connect(DB_PATH)

    # def _init_db_table(self):
    #     """Стварае табліцу тэм, калі яе яшчэ няма."""
    #     with self._connect() as conn:
    #         conn.execute(f"""
    #             CREATE TABLE IF NOT EXISTS {TOPICS_TABLE} (
    #                 id          INTEGER PRIMARY KEY AUTOINCREMENT,
    #                 day_num     INTEGER NOT NULL,
    #                 topic_order INTEGER NOT NULL,
    #                 title       TEXT NOT NULL,
    #                 quotes_json TEXT NOT NULL,
    #                 UNIQUE (day_num, topic_order)
    #             )
    #         """)

    def prnt(self):
        tu = (self.day_var.get(), self.c_var.get())

        print(f"День - {tu[0]}, а тема - {tu[1]} - дадайце цытаты...")

    def _build_ui(self):
        # --- Верхняя панэль: Дзень, Нумар тэмы, Назва ---
        top_frame = ttk.LabelFrame(self.root, text="1. Параметры тэмы", padding=10)
        top_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(top_frame, text="Дзень (1-90):").grid(row=0, column=0, sticky="w")
        self.day_var = tk.IntVar(value=1)
        ttk.Spinbox(top_frame, from_=1, to=90, textvariable=self.day_var, width=5).grid(row=0, column=1, padx=5)

        ttk.Label(top_frame, text="Тема (1-8):").grid(row=0, column=2, sticky="w")
        self.c_var = tk.IntVar(value=1)
        ttk.Spinbox(top_frame, from_=1, to=8, textvariable=self.c_var, width=5).grid(row=0, column=3, padx=5)

        ttk.Button(top_frame,text="💾 print", command=self.prnt).grid(row=0, column=4, sticky="w")



        ###кнопка выход 
        ttk.Button(self.root,text=">>Выхад...", command=root.destroy).pack(anchor="e", padx = 20, pady=25)

        

           

        
        

    #     ttk.Label(top_frame, text="Тэма № (1-8):").grid(row=0, column=2, sticky="w", padx=(10, 0))
    #     self.order_var = tk.IntVar(value=1)
    #     ttk.Spinbox(top_frame, from_=1, to=8, textvariable=self.order_var, width=5).grid(row=0, column=3, padx=5)

    #     ttk.Label(top_frame, text="Назва тэмы:").grid(row=0, column=4, sticky="w", padx=(10, 0))
    #     self.title_var = tk.StringVar()
    #     ttk.Entry(top_frame, textvariable=self.title_var, width=30).grid(row=0, column=5, padx=5, sticky="ew")
    #     ttk.Label(top_frame, text="/    ").grid(row=0, column=9)
    #     ttk.Label(top_frame, text="/    ").grid(row=0, column=10)
        
    #     # ttk.Button(top_frame, text="Загрузіць з БД", command=self.load_existing).grid(row=0, column=6, padx=5)

    #     # --- Панэль дадання блока цытат ---
    #     block_frame = ttk.LabelFrame(self.root, text="2. Дадаць спасылку на цытаты", padding=10)
    #     block_frame.pack(fill="x", padx=10, pady=5)

    #     ttk.Label(block_frame, text="Пазіція у тэме:").grid(row=0, column=0)
    #     self.book_var = tk.StringVar(value="1")
    #     ttk.Entry(block_frame, textvariable=self.book_var, width=6).grid(row=0, column=1, padx=5)
        

    #     ttk.Label(block_frame, text="Кніга (ID):").grid(row=0, column=2)
    #     self.book_var = tk.StringVar(value="1")
    #     ttk.Entry(block_frame, textvariable=self.book_var, width=6).grid(row=0, column=3, padx=5)

    #     ttk.Label(block_frame, text="Глава:").grid(row=0, column=5)
    #     self.chap_var = tk.StringVar(value="1")
    #     ttk.Entry(block_frame, textvariable=self.chap_var, width=6).grid(row=0, column=6, padx=5)

    #     ttk.Label(block_frame, text="/    ").grid(row=0, column=7)
    #     ttk.Label(block_frame, text="/    ").grid(row=0, column=8)
    #     ttk.Label(block_frame, text="/    ").grid(row=0, column=9)
    #     ttk.Label(block_frame, text="/    ").grid(row=0, column=10)

    #     ttk.Label(block_frame, text="Цытаты (напр. 1-4 або 2, 5):").grid(row=1, column=0, columnspan=3, padx=5)
    #     self.quotes_var = tk.StringVar()
    #     q_entry = ttk.Entry(block_frame, textvariable=self.quotes_var, width=20)
    #     q_entry.grid(row=1, column=3, columnspan=8, sticky="WE", padx=5)
    #     q_entry.bind("<Return>", lambda e: self.add_block())  # Даданне па Enter!

    #     ttk.Button(block_frame, text="➕ Дадаць блок", command=self.add_block).grid(row=0, column=10,  pady=5, padx=5)
    #     ttk.Button(block_frame, text="🗑 Ачысціць усе", command=self.clear_blocks).grid(row=0, column=9, padx=5)

    #     # --- Сярэдняя частка: Спіс блокаў + Перадпрагляд тэксту з БД ---
    #     mid_frame = ttk.Frame(self.root)
    #     mid_frame.pack(fill="both", expand=True, padx=10, pady=5)

    #     left_box = ttk.LabelFrame(mid_frame, text="Склад тэмы (JSON)", padding=5)
    #     left_box.pack(side="left", fill="both", expand=False)

    #     self.blocks_listbox = tk.Listbox(left_box, width=32, font=("Consolas", 10))
    #     self.blocks_listbox.pack(fill="both", expand=True)
    #     ttk.Button(left_box, text="Выдаліць выбраны блок", command=self.remove_selected_block).pack(fill="x", pady=(5, 0))

    #     right_box = ttk.LabelFrame(mid_frame, text="Перадпрагляд тэксту з вашай базы SQLite", padding=5)
    #     right_box.pack(side="right", fill="both", expand=True, padx=(10, 0))

    #     self.preview_text = tk.Text(right_box, wrap="word", font=("Sans", 10), state="disabled", bg="#f8f9fa")
    #     self.preview_text.pack(fill="both", expand=True)

    #     # --- Ніжняя панэль: Захаванне ---
    #     bot_frame = ttk.Frame(self.root, padding=10)
    #     bot_frame.pack(fill="x")

    #     self.status_lbl = ttk.Label(bot_frame, text="Гатова да працы", foreground="gray")
    #     self.status_lbl.pack(side="left")

    #     ttk.Button(
    #         bot_frame,
    #         text="💾 Захаваць у БД і перайсці да наступнай тэмы",
    #         #command=self.save_and_next,
    #     ).pack(side="right")

    # def add_block(self):
    #     try:
    #         book_id = int(self.book_var.get().strip())
    #         chapter = int(self.chap_var.get().strip())
    #         raw_q = self.quotes_var.get().strip()
    #         if not raw_q:
    #             return

    #         # Правяраем, што дыяпазон карэктны
    #         q_nums = expand_spec(raw_q)
    #         if not q_nums:
    #             return

    #         # Калі ўведзены адзін дыяпазон накшталт "1-4", захоўваем радком, інакш спісам лікаў
    #         q_val = raw_q if ("-" in raw_q and "," not in raw_q) else q_nums
    #         block = {"b": book_id, "c": chapter, "q": q_val}

    #         self.blocks.append(block)
    #         self.quotes_var.set("")  # Ачышчаем поле цытат для хуткага ўводу наступных
    #         self._refresh_ui()
    #     except Exception as e:
    #         messagebox.showerror("Памылка ўводу", f"Праверце лічбы:\n{e}")

    # def remove_selected_block(self):
    #     sel = self.blocks_listbox.curselection()
    #     if sel:
    #         del self.blocks[sel[0]]
    #         self._refresh_ui()

    # def clear_blocks(self):
    #     self.blocks.clear()
    #     self._refresh_ui()

    # def _refresh_ui(self):
    #     # Абнаўляем спіс блокаў злева
    #     self.blocks_listbox.delete(0, tk.END)
    #     for b in self.blocks:
    #         self.blocks_listbox.insert(tk.END, json.dumps(b, ensure_ascii=False))

        # Падцягваем рэальныя цытаты з базы для перадпрагляду справа
        # lines = []
        # with self._connect() as conn:
        #     for b in self.blocks:
        #         q_nums = expand_spec(str(b["q"])) if not isinstance(b["q"], list) else b["q"]
        #         placeholders = ",".join("?" for _ in q_nums)
        #         cur = conn.execute(
        #             f"""
        #             SELECT quote_num, text FROM {QUOTES_TABLE}
        #             WHERE id_book = ? AND chapter = ? AND quote_num IN ({placeholders})
        #             ORDER BY quote_num ASC
        #             """,
        #             [b["b"], b["c"], *q_nums],
        #         )
        #         found = cur.fetchall()
        #         found_map = {r: r for r in found}

        #         lines.append(f"--- Кніга {b['b']}, глава {b['c']} ---")
        #         for num in q_nums:
        #             if num in found_map:
        #                 lines.append(f"[{num}] {found_map[num]}")
        #             else:
        #                 lines.append(f"[{num}] ⚠️ НЕ ЗНОЙДЗЕНА Ў БАЗЕ!")
        #         lines.append("")

        # self.preview_text.config(state="normal")
        # self.preview_text.delete("1.0", tk.END)
        # # self.preview_text.insert("1.0", "\n".join(lines))
        # self.preview_text.config(state="disabled")

    # def load_existing(self):
    #     """Загружае ўжо захаваную тэму з базы для рэдагавання."""
    #     day = self.day_var.get()
    #     order = self.order_var.get()
    #     with self._connect() as conn:
    #         cur = conn.execute(
    #             f"SELECT title, quotes_json FROM {TOPICS_TABLE} WHERE day_num = ? AND topic_order = ?",
    #             (day, order),
    #         )
    #         row = cur.fetchone()
    #         if row:
    #             self.title_var.set(row)
    #             self.blocks = json.loads(row)
    #             self._refresh_ui()
    #             self.status_lbl.config(text=f"Загружана: Дзень {day}, Тэма {order}", foreground="blue")
    #         else:
    #             messagebox.showinfo("Інфармацыя", "Гэтая тэма яшчэ не запоўнена ў базе.")

    # def save_and_next(self):
    #     title = self.title_var.get().strip()
    #     if not title or not self.blocks:
    #         messagebox.showwarning("Увага", "Увядзіце назву тэмы і дадайце хаця б адзін блок цытат.")
    #         return

    #     day = self.day_var.get()
    #     order = self.order_var.get()
    #     json_str = json.dumps(self.blocks, ensure_ascii=False)

    #     with self._connect() as conn:
    #         conn.execute(
    #             f"""
    #             INSERT INTO {TOPICS_TABLE} (day_num, topic_order, title, quotes_json)
    #             VALUES (?, ?, ?, ?)
    #             ON CONFLICT(day_num, topic_order) DO UPDATE SET
    #                 title=excluded.title,
    #                 quotes_json=excluded.quotes_json
    #             """,
    #             (day, order, title, json_str),
    #         )

    #     self.status_lbl.config(text=f"✅ Захавана: Дзень {day}, Тэма {order} ({title})", foreground="green")

        # # Аўтаматычны пераход да наступнай тэмы / дня
        # self.title_var.set("")
        # self.clear_blocks()
        # if order < 8:
        #     self.order_var.set(order + 1)
        # else:
        #     self.order_var.set(1)
        # if day < 90:
        #     self.day_var.set(day + 1)
if __name__ == "__main__":
    root = tk.Tk()
    app = TopicBuilderApp(root)
    root.mainloop()
