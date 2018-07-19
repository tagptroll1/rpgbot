from random import randint, choice
from time import sleep
from functools import wraps
from datetime import timedelta, datetime

from item import Item, Pickaxe
from character import Character
import activity

class NotEnoughMaterialError(Exception):
    pass


class Player(Character):
    def __init__(self, name, race="human", **kwargs):
        super().__init__(name, race, **kwargs)
        self.items = dict()
        self.mats = kwargs.pop("mats", {
            "wood": 0,
            "stone": 0,
            "coal": 0,
            "iron": 0,
            "copper": 0,
            "tin": 0,
            "bronze": 0,
            "steel": 0,
            "diamond": 0
        })
        self.__worktimer = None
        self.pickaxe = None

    @property
    def wood(self):
        return self.mats["wood"]

    @property
    def stone(self):
        return self.mats["stone"]

    @property
    def coal(self):
        return self.mats["coal"]

    @property
    def iron(self):
        return self.mats["iron"]

    @property
    def copper(self):
        return self.mats["copper"]

    @property
    def tin(self):
        return self.mats["tin"]

    @property
    def bronze(self):
        return self.mats["bronze"]

    @property
    def steel(self):
        return self.mats["steel"]

    @property
    def diamond(self):
        return self.mats["diamond"]

    def add_item(self, item):
        if not isinstance(item, Item):
            raise TypeError

        if item.id in self.items:
            self.items[item.id]["amount"] += 1
        else:
            self.items[item.id] = {"item": item, "amount": 1}

    def get_item(self, item):
        item_to_get = self.items.get(item, None)
        if item_to_get:
            return item_to_get

        for item in self.items.values():
            if item["item"].name == str(item):
                return item
        return None

    def inc_mat(self, mat, amt):
        if amt < 0:
            raise ValueError
        self.mats[mat] += amt

    def dec_mat(self, mat, amt):
        if amt < 0:
            raise ValueError
        if self.mats[mat] < amt:
            raise NotEnoughMaterialError

        self.mats[mat] -= mat

    def time_remaining(self):
        now = datetime.utcnow()
        timeleft = self.__worktimer - now
        total = timeleft.total_seconds()
        m, s = divmod(total, 60)
        h, m = divmod(m, 60)
        return timeleft, h, m, s

    def find_pick(self):
        best = None
        for x in range(7):
            if x in self.items:
                best = x

        if best:
            self.pickaxe = self.items[best]["item"]
            return True
        else:
            return False

    def mine(self):
        if not self.pickaxe:
            if not self.find_pick():
                return
        if self.__worktimer:
            d, h, m, s = self.time_remaining()
            if not d.days < 0:
                return
            else:
                self.__worktimer = None
                
        now = datetime.utcnow()
        self.__worktimer = now + timedelta(seconds=1)
        can_mine = activity.get_minable(self.pickaxe.toughness)
        for x in range(randint(0, self.pickaxe.toughness//25)):
            self.inc_mat(choice(can_mine), randint(0,self.pickaxe.modifier))


    def __repr__(self):
        itemlist = ", ".join(repr(item['item']) for item in self.items.values())
        matlist = ", ".join(f"{k}: {v}" for k, v in self.mats.items())
        return (
            f"<Player({self.name}, {self.race}, "
            f"hp={self.health}, atk={self.attack}, def={self.defense}, "
            f"luck={self.luck}, gold={self.gold}, "
            f"items=[{itemlist}], "
            "mats={"
            f"{matlist}"
            "})>"
        )

    def __str__(self):
        itemlist = "\n\t".join(f"{item['item'].name}, count: {item['amount']}" for item in self.items.values())
        matlist = "\n\t".join(f"{k.title():<10} {v}" for k, v in self.mats.items())
        return (
            f"Player: {self.name}\n"
            f"Race: {self.race}\n"
            f"Health: {self.health}\n"
            f"Attack: {self.attack}\n"
            f"Defense: {self.defense}\n"
            f"Luck: {self.luck}\n"
            f"Gold: {self.gold}\n"
            f"Items: \n\t{itemlist}\n"
            f"Materials: \n\t{matlist}"
        )


