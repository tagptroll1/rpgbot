

class Character:
    def __init__(self, name, race, **kwargs):
        self.name = name.title()
        self.race = race.title()
        self.health = kwargs.pop("hp", 100)
        self.attack = kwargs.pop("attack", 10)
        self.defense = kwargs.pop("defense", 10)
        self.luck = kwargs.pop("luck", 5)
        self.gold = kwargs.pop("gold", 100)
