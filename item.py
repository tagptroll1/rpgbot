import json
from textwrap import dedent
from collections import Counter
from pathlib import Path
from pprint import pprint

SCRIPT = Path.cwd()
DATA_PATH = Path("data/itemlib.json")


class Item:
    def __init__(self, item):
        self.id = item["id"]
        self.name = item["name"]
        self.value = item.get("value", 0)
        self.desc = item.get("desc", "")
        self.type = item.get("type", "none")

    def __repr__(self):
        return f"<Item({self.id}, {self.name}, value={self.value})>"

    def __str__(self):
        return f"Item (id={self.id}) named {self.name}, value: {self.value}"

class Pickaxe(Item):
    def __init__(self, item):
        super().__init__(item)
        self.json = item
        self.modifier = item.get("modifier", 0)
        self.toughness = item.get("toughness", 0)
        self.durability = item.get("durability", 1)
        self.recipe = item.get("recipe", [])

    def __repr__(self):
        return f"""<Item({self.json})>"""

    def __str__(self):
        recipe = Counter(self.recipe)
        return dedent(f"""
            Pickaxe (id={self.id}) named {self.name}, value: {self.value} 
            Mining modifier of {self.modifier}
            Toughness of {self.toughness} 
            Durability of {self.durability}
            Crafted with repice:
                {', '.join(f"{v}x {k}" for k,v in recipe.items())}
        """)

def add_item(__id = None, **kwargs):
    _type = kwargs.get("type")
    _name = kwargs.get("name")
    _desc = kwargs.get("desc", "")
    _value = kwargs.get("value", None)
    item_dict = {
        "name": _name,
        "type": _type,
        "desc": _desc,
        "value": _value
    }
    if _type == "pickaxe":
        _modifier = kwargs.get("modifier")
        _toughness = kwargs.get("toughness")
        _durability = kwargs.get("durability")
        _recipe = kwargs.get("recipe")
        item_dict["modifier"] = _modifier
        item_dict["toughness"] = _toughness
        item_dict["durability"] = _durability
        item_dict["recipe"] = _recipe

    if not all(item_dict.values()):
        raise ValueError

    with DATA_PATH.open(mode="r") as data:
        items = json.load(data)

    if __id:
        new_id = __id
    elif items:
        new_id = int(max(items)) + 1
    else:
        new_id = 1

    item_dict["id"] = new_id
    items[str(new_id)] = item_dict
    with DATA_PATH.open(mode="w") as data:
        if items:
            json.dump(items, data, sort_keys=True,
                  indent=4, separators=(',', ': '))
        else:
            json.dump({}, data)

def del_item(_id):
    with DATA_PATH.open(mode="r") as data:
        items = json.load(data)

    passed = items.pop(str(_id), False)

    if passed:
        with DATA_PATH.open(mode="w") as data:
            if items:
                json.dump(items, data, sort_keys=True,
                      indent=4, separators=(',', ': '))
            else:
                json.dump({}, data)

def get_item(_id):
    with DATA_PATH.open() as data:
        item = json.load(data)
        item = item.get(str(_id))
    if not item:
        return None

    elif item["type"] == "pickaxe":
        return Pickaxe(item)

    else:
        return Item(item)
