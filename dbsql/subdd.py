#import json
import sqlite3

DB_PATH = "/home/sashbo/Progy/prbot/_sin_fi.sqlt"  # Укажыце шлях да вашага файла SQLite
item_tupl = ()

class DBase:
    def __init__(self, db_name = DB_PATH):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

 #Метад для адкрыцця злучэння (працуе пры уваходзе у  with)
    def __enter__(self):
        pass
        self.conn = sqlite3.connect(self. db_name)
        self.cursor = self.conn.cursor()
        return self

    ##захаванне і закрыццё пасля выхада з блока
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
                self.cursor.close()
                self.conn.close()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER
            )
        """)
    # метад для тэставання, а можа калі і спатрэбіцца для уліка карыстальнікаў
    def add_user(self, name, age):
        self.cursor.execute("INSERT INTO user (name, age) VALUES (?, ?)",
        (name, age))
    # метад дадання запісаў у табліцу джэйсонаў
    def add_topic(self, id_day, id_itm, jsn_ref_rem):
            self.cursor.execute("INSERT INTO txtforday (id_day, id_itm, jsn_ref_rem) VALUES (?, ?, ?)",
            (id_day, id_itm, jsn_ref_rem))
    # метад выдалення запісаў з табліцы, на выпадак некарэктнага увода
    def del_topic(self, id_day, id_itm):
        self.cursor.execute("DELETE FROM txtforday WHERE id_day = ? OR id_itm = ?" , (id_day, id_itm))
#""" патрэбны яшчэ метады фармавання json-аў, і перадачы іх у базу, але гэтыя метады трэба стварыць у другім файле 
#там дзе ткінтэр, а сюды імпартаваць іх для выклікаў"""

    def sel_items(self):
        self.cursor.execute("SELECT id, nazv_items FROM ITEMS_DAY")
        items_list = [ row for row in self.cursor.fetchall()]
        print(items_list)

    

if __name__ == "__main__":

    # item_tupl_d = int(input("уведзі дзень)"))
    # item_tupl_i = int(input("уведзі тэму)"))
    with DBase() as db:
        db.sel_items()
