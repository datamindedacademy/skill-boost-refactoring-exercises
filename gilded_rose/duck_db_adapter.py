import duckdb
import hashlib
from collections.abc import Sequence
from gilded_rose.item import Item


class DuckDBAdapter:
    def __init__(
        self,
        items: Sequence[Item],
        db_path: str | None = None,
        db_conn: duckdb.DuckDBPyConnection | None = None,
    ) -> None:
        if db_conn is not None:
            print("Using provided DuckDB connection.")
            self.conn = db_conn
        elif db_path is not None:
            print(f"Connecting to DuckDB at: {db_path}")
            self.conn = duckdb.connect(db_path)
        else:
            raise ValueError("Either db_conn or db_path must be provided.")

        self.table_name = self._generate_table_name(items)
        self._create_or_replace_table()

    def _generate_table_name(self, items: Sequence[Item]) -> str:
        item_repr = "|".join(
            f"{item.name}:{item.sell_in}:{item.quality}" for item in items
        )
        digest = hashlib.md5(item_repr.encode("utf-8")).hexdigest()
        return f"item_log_{digest[:8]}"

    def _create_or_replace_table(self) -> None:
        self.conn.execute(f"""
            CREATE OR REPLACE TABLE {self.table_name} (
                day INTEGER,
                name VARCHAR,
                sell_in INTEGER,
                quality INTEGER
            )
        """)

    def log_items(self, items: Sequence[Item], day: int) -> None:
        data = [(day, item.name, item.sell_in, item.quality) for item in items]
        print(f"Logging {len(data)} items for day {day} into table {self.table_name}")
        self.conn.executemany(
            f"INSERT INTO {self.table_name} (day, name, sell_in, quality) VALUES (?, ?, ?, ?)",
            data,
        )
