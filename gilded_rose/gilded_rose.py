# -*- coding: utf-8 -*-
from collections.abc import Sequence
from gilded_rose.item import Item
from gilded_rose.duck_db_adapter import DuckDBAdapter
import duckdb
from random import randint


class GildedRose:
    # Add item checks? value over 50 and so on?
    def __init__(
        self,
        items: Sequence[Item],
        db_conn: duckdb.DuckDBPyConnection | None = None,
        db_path: str | None = None,
    ) -> None:
        self.items = items
        if db_conn is None and db_path is None:
            db_path = ":memory:"

        self.logger = DuckDBAdapter(items=items, db_conn=db_conn, db_path=db_path)
        self.current_day = 0
        self._log_current_day()

    def pass_one_day(self) -> None:
        self.update_quality_v2()
        self.current_day += 1
        self._log_current_day()

    def update_quality(self) -> None:
        for item in self.items:
            if (
                item.name != "Aged Brie"
                and item.name != "Backstage passes to a TAFKAL80ETC concert"
            ):
                if item.quality > 0:
                    if item.name != "Sulfuras, Hand of Ragnaros":
                        item.quality = item.quality - 1
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.name == "Backstage passes to a TAFKAL80ETC concert":
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality = item.quality + 1
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert":
                        if item.quality > 0:
                            if item.name != "Sulfuras, Hand of Ragnaros":
                                item.quality = item.quality - 1
                    else:
                        item.quality = item.quality - item.quality
                else:
                    if item.quality < 50:
                        item.quality = item.quality + 1

    def update_quality_v2(self) -> None:
        for item in self.items:
            self._decrease_sell_in_with_exceptions(item)

            match item.name:
                case "Aged Brie":
                    self._increase_quality(item)
                    if item.sell_in < 0:
                        self._increase_quality(item)

                case "Backstage passes to a TAFKAL80ETC concert":
                    if item.sell_in < 0:
                        item.quality = 0
                    elif item.sell_in < 5:
                        self._increase_quality(item, increase_amount=3)
                    elif item.sell_in < 10:
                        self._increase_quality(item, increase_amount=2)
                    else:
                        self._increase_quality(item)

                case "Sulfuras, Hand of Ragnaros":
                    pass

                case "Trump coin":
                    random_quality = randint(0, 50)
                    self._set_quality(item, new_quality=random_quality)

                case _ if "Conjured" in item.name:
                    self._standard_quality_decay(item, decay_rate=2)

                case _:
                    self._standard_quality_decay(item)

    def _increase_quality(self, item: Item, increase_amount: int = 1) -> None:
        """Increase the quality of an item, ensuring it does not exceed 50. 1 by default"""
        item.quality = min(50, item.quality + increase_amount)

    def _standard_quality_decay(self, item: Item, decay_rate: int = 1) -> None:
        """Standard quality decay for items that are not special."""
        self._decrease_quality(item, decrease_amount=decay_rate)
        if item.sell_in < 0:
            self._decrease_quality(item, decrease_amount=decay_rate)

    def _decrease_quality(self, item: Item, decrease_amount: int = 1) -> None:
        """Decrease the quality of an item, ensuring it does not go below 0. 1 by default"""
        item.quality = max(0, item.quality - decrease_amount)

    def _decrease_sell_in_with_exceptions(self, item: Item) -> None:
        """Decrease the sell-in value of an item."""
        if item.name != "Sulfuras, Hand of Ragnaros":
            item.sell_in -= 1

    def _log_current_day(self) -> None:
        """Log the current day and item states."""
        self.logger.log_items(self.items, self.current_day)

    def _set_quality(self, item: Item, new_quality: int) -> None:
        """Set the quality of an item, ensuring it does not exceed 50 or go below 0."""
        if not (0 <= new_quality <= 50):
            raise ValueError("Quality must be between 0 and 50 inclusive.")
        item.quality = new_quality
