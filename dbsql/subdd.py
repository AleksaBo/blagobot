import json
import sqlite3

# === НАЛАДЫ ПАД ВАШУ БАЗУ ===
DB_PATH = "/home/sashbo/Progy/prbot/dbsql/sin_fi.sqlt"  # Укажыце шлях да вашага файла SQLite

# Назвы табліц і слупкоў (падпраўце пад вашы, калі адрозніваюцца)
QUOTES_TABLE = "quotes"        # Слупкі: id_book, chapter, quote_num, text
TOPICS_TABLE = "schedule_topics" # Слупкі: day_num, topic_order, title, quotes_json




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


class TopicBuilderTb:
    def __init__(self):
        
        self._init_db_table()
        
    def _connect(self):
        return sqlite3.connect(DB_PATH)

    def _init_db_table(self):
        """Стварае табліцу тэм, калі яе яшчэ няма."""
        with self._connect() as conn:
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {TOPICS_TABLE} (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    day_num     INTEGER NOT NULL,
                    topic_order INTEGER NOT NULL,
                    title       TEXT NOT NULL,
                    quotes_json TEXT NOT NULL,
                    UNIQUE (day_num, topic_order)
                )
            """)
