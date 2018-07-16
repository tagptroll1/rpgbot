

class Character:
    def __init__(self, name, race, **kwargs):
        self.name = name
        self.race = race
        self.health = kwargs.pop("hp", 100)
        self.attack = kwargs.pop("atk", 10)
        self.defense = kwargs.pop("def", 10)
        self.luck = kwargs.pop("luck", 5)
        self.gold = kwargs.pop("gold", 100)
