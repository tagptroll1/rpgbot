import unittest

from player import Player, NotEnoughMaterialError
from character import Character
import item

class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("Bob")
        self.player2 = Player("Knut")

    def test_create_player(self):
        player3 = Player("Tom", race="Elf",
                         hp=200, attack=20, defense=5, 
                         luck=10, gold=200,
                         mats={
                             "wood": 5,
                             "stone": 4,
                             "coal": 3,
                             "iron": 6,
                             "copper": 8,
                             "tin": 1,
                             "bronze": 7,
                             "steel": 0,
                             "diamond": 2
                         })
        self.assertIsInstance(self.player1, Player)
        self.assertIsInstance(self.player2, Player)
        self.assertIsInstance(player3, Player)
        self.assertIsInstance(self.player1, Character)
        self.assertIsInstance(self.player2, Character)
        self.assertIsInstance(player3, Character)
        self.assertEqual(self.player1.name, "Bob")
        self.assertEqual(self.player2.name, "Knut")
        self.assertEqual(player3.name, "Tom")
        self.assertEqual(player3.race, "Elf")
        self.assertEqual(player3.health, 200)
        self.assertEqual(player3.attack, 20)
        self.assertEqual(player3.defense, 5)
        self.assertEqual(player3.luck, 10)
        self.assertEqual(player3.gold, 200)
        self.assertEqual(player3.wood, 5)
        self.assertEqual(player3.stone, 4)
        self.assertEqual(player3.coal, 3)
        self.assertEqual(player3.iron, 6)
        self.assertEqual(player3.copper, 8)
        self.assertEqual(player3.tin, 1)
        self.assertEqual(player3.bronze, 7)
        self.assertEqual(player3.steel, 0)
        self.assertEqual(player3.diamond, 2)

    def test_create_character(self):
        params = {
            "name": "bob the slayer",
            "race": "human",
            "hp": 150,
            "attack": 20,
            "gold": 200
        }
        char1 = Character(**params)
        char2 = Character("Knut", "elf")
        
        self.assertIsInstance(char1, Character)
        self.assertIsInstance(char2, Character)
        self.assertNotIsInstance(char1, Player)
        self.assertNotIsInstance(char2, Player)
        self.assertEqual(char1.name, "Bob The Slayer")
        self.assertEqual(char1.race, "Human")
        self.assertEqual(char1.health, 150)
        self.assertEqual(char1.attack, 20)
        self.assertEqual(char1.defense, 10)
        self.assertEqual(char1.luck, 5)
        self.assertEqual(char1.gold, 200)

    def test_item(self):
        item1 = item.get_item(2)
        self.assertIsInstance(item1, item.Item)
        self.assertIsInstance(item1, item.Pickaxe)
        self.assertEqual(item1.id, 2)
        self.assertEqual(item1.name, "Stone Pickaxe")
        self.assertEqual(item1.value, 50)
        self.assertEqual(item1.desc, "A Pickaxe of the finest cryptocrystalline rocks.")
        self.assertEqual(item1.type, "pickaxe")
        self.assertEqual(item1.modifier, 1) 
        self.assertEqual(item1.toughness, 150) 
        self.assertEqual(item1.durability, 1000)
        self.assertListEqual(item1.recipe, ["wood", "stone", "stone"])

    def test_add_item(self):
        item9999 = item.get_item(9999)
        if item9999:
            item.del_item(9999)

        item_to_add = {
            "type": "Key", 
            "name": "Secret key", 
            "desc": "This key has secret properties", 
            "value": 500
        }
        item.add_item(__id=9999, **item_to_add)
        new_i = item.get_item(9999)
        self.assertIsInstance(new_i, item.Item)
        self.assertEqual(new_i.name, "Secret key")
        self.assertEqual(new_i.type, "Key")
        self.assertEqual(new_i.desc, "This key has secret properties")
        self.assertEqual(new_i.value, 500)
        item.del_item(9999)
        if item9999:
            item.add_item(__id=9999, **item9999.__dict__)

    def test_add_item_to_player(self):
        p = self.player1

        self.assertIsInstance(p.items, dict)
        self.assertFalse(p.items)

        # stone pickaxe, id 2
        pick = item.get_item(2)
        p.add_item(pick)

        self.assertIsInstance(p.items, dict)
        self.assertTrue(p.items)
        self.assertEqual(len(p.items), 1)
        self.assertDictEqual(p.items, {2:{"item": pick, "amount": 1}})
        self.assertIs(p.items[2]["item"], pick)

        # copper pickaxe, id 3
        pick2 = item.get_item(3)
        p.add_item(pick2)

        self.assertIsInstance(p.items, dict)
        self.assertTrue(p.items)
        self.assertEqual(len(p.items), 2)
        self.assertDictEqual(p.items, {
            2: {
                "item": pick,
                "amount": 1
            },
            3: {
                "item": pick2,
                "amount": 1
            }
        })
        self.assertIs(p.items[2]["item"], pick)
        self.assertIs(p.items[3]["item"], pick2)

        p.add_item(pick2)

        self.assertIsInstance(p.items, dict)
        self.assertTrue(p.items)
        self.assertEqual(len(p.items), 2)
        self.assertDictEqual(p.items, {
            2: {
                "item": pick,
                "amount": 1
            },
            3: {
                "item": pick2,
                "amount": 2
            }
        })
        self.assertIs(p.items[2]["item"], pick)
        self.assertIs(p.items[3]["item"], pick2)

    def test_player_get_item(self):
        p = self.player1
        self.assertIsNone(p.get_item(2))

        i = item.get_item(2)
        p.add_item(i)
        self.assertEqual(i, p.get_item(2)["item"])

        del p.items[2]
        self.assertIsNone(p.get_item(2))


    def test_player_mats(self):
        """Test incrementing and derementing materials"""
        p = self.player1
        for mat in p.mats.values():
            self.assertEqual(mat, 0)

        for mat in p.mats:
            p.inc_mat(mat, 5)
            self.assertEqual(getattr(p, mat), 5)
            p.dec_mat(mat, 3)
            self.assertEqual(getattr(p, mat), 2)
            p.dec_mat(mat, 2)
            self.assertEqual(getattr(p, mat), 0)

            self.assertRaises(ValueError, p.dec_mat, mat, -1)
            self.assertRaises(ValueError, p.inc_mat, mat, -1)
            self.assertRaises(NotEnoughMaterialError, p.dec_mat, mat, 5)
            self.assertEqual(getattr(p, mat), 0)


if __name__ == "__main__":
    unittest.main()
