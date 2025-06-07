# -*- coding: utf-8 -*-
import pytest
from gilded_rose.item import Item
from gilded_rose.gilded_rose import GildedRose


@pytest.mark.parametrize(
    "item_name, sell_in, quality, expected_sell_in, expected_quality",
    [
        ("foo", 0, 0, -1, 0),
        ("foo", 5, 10, 4, 9),
        ("Aged Brie", 2, 0, 1, 1),
        ("Aged Brie", -1, 0, -2, 2),
        ("Aged Brie", 0, 50, -1, 50),  # Should not go above 50
        ("Sulfuras, Hand of Ragnaros", 0, 40, 0, 40),
        ("Backstage passes to a TAFKAL80ETC concert", 15, 20, 14, 21),
        ("Backstage passes to a TAFKAL80ETC concert", 10, 20, 9, 22),
        ("Backstage passes to a TAFKAL80ETC concert", 5, 20, 4, 23),
        ("Backstage passes to a TAFKAL80ETC concert", 1, 49, 0, 50),
        ("Backstage passes to a TAFKAL80ETC concert", 0, 20, -1, 0),
        ("Backstage passes to a TAFKAL80ETC concert", -1, 20, -2, 0),
        ("Max value", 3, 50, 2, 49),  # Generic item, quality can't increase
    ],
)
def test_item_update_both_versions(
    item_name: str,
    sell_in: int,
    quality: int,
    expected_sell_in: int,
    expected_quality: int,
) -> None:
    # v1
    items_v1 = [Item(item_name, sell_in, quality)]
    GildedRose(items_v1).update_quality()
    item_v1 = items_v1[0]

    # v2
    items_v2 = [Item(item_name, sell_in, quality)]
    GildedRose(items_v2).update_quality_v2()
    item_v2 = items_v2[0]

    # Assertions for v1
    assert item_v1.name == item_name
    assert item_v1.sell_in == expected_sell_in
    assert item_v1.quality == expected_quality

    # Assertions for v2
    assert item_v2.name == item_name
    assert item_v2.sell_in == expected_sell_in
    assert item_v2.quality == expected_quality


def test_order_preserved():
    original_items = [
        Item("Aged Brie", 2, 0),
        Item("foo", 5, 10),
        Item("Sulfuras, Hand of Ragnaros", 0, 40),
        Item("Backstage passes to a TAFKAL80ETC concert", 10, 20),
    ]

    # Copy the item names to compare after mutation
    original_names = [item.name for item in original_items]

    # Run both update functions
    items_v1 = [Item(item.name, item.sell_in, item.quality) for item in original_items]
    items_v2 = [Item(item.name, item.sell_in, item.quality) for item in original_items]

    GildedRose(items_v1).update_quality()
    GildedRose(items_v2).update_quality_v2()

    assert [item.name for item in items_v1] == original_names
    assert [item.name for item in items_v2] == original_names


@pytest.mark.parametrize(
    "sell_in, quality, expected_sell_in, expected_quality",
    [
        (5, 10, 4, 8),  # Degrade by 2 before sell date
        (0, 10, -1, 6),  # Degrade by 4 on sell date
        (-1, 10, -2, 6),  # Degrade by 4 after sell date
        (3, 1, 2, 0),  # Cannot go below 0
        (-1, 1, -2, 0),  # Cannot go below 0 post-expiry
        (2, 0, 1, 0),  # Already 0
        (2, 49, 1, 47),  # Just under max
        (2, 50, 1, 48),  # At max value
    ],
)
def test_conjured_item_update_quality_v2(
    sell_in: int,
    quality: int,
    expected_sell_in: int,
    expected_quality: int,
) -> None:
    item = Item("Conjured Magic Stick", sell_in, quality)
    items = [item]
    GildedRose(items).update_quality_v2()
    updated = items[0]

    assert updated.name == "Conjured Magic Stick"
    assert updated.sell_in == expected_sell_in
    assert updated.quality == expected_quality
