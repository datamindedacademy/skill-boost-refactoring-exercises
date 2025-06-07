# -*- coding: utf-8 -*-
from collections.abc import Sequence
from gilded_rose.item import Item


class GildedRose:
    def __init__(self, items: Sequence[Item]) -> None:
        # Add item checks? value over 50 and so on?
        self.items = items

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
