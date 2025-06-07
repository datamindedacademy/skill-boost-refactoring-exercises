import duckdb
from gilded_rose.item import Item
from gilded_rose.gilded_rose import GildedRose


def test_gilded_rose_logs_correctly_over_days():
    items = [
        Item("Aged Brie", sell_in=2, quality=0),
        Item("Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=25),
        Item("Conjured Mana Cake", sell_in=3, quality=6),
        Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
    ]

    conn = duckdb.connect(":memory:")
    gr = GildedRose(
        items, db_conn=conn
    )  

    for _ in range(10):
        gr.pass_one_day()

    tables = conn.execute("SHOW TABLES").fetchall()
    assert len(tables) == 1

    table_name = tables[0][0]
    count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

    rows = conn.execute(f"SELECT * FROM {table_name}").fetchall()
    # for row in rows:
    #     print(row)

    assert count == 11 * len(items)
