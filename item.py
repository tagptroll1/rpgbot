import json
from pathlib import Path
from pprint import pprint

SCRIPT = Path.cwd()
print(SCRIPT)
DATA_PATH = Path("data/itemlib.json")
with DATA_PATH.open() as dat:
    print(json.load(dat))
class Item:
    def __init__(self, _id):
        with DATA_PATH.open() as data:
            item = json.load(data)
            item = item[str(_id)]
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
    def __init__(self, _id):
        super().__init__(_id)
        with DATA_PATH.open() as data:
            item = json.load(data)
            item = item[str(_id)]
            self.modifier = item.get("modifier", 0.5)
            self.toughness = item.get("toughness", 49)
            self.durability = item.get("durability", 100)
            self.recipe = item.get("recipe", [])

        
