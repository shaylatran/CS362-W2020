from unittest import TestCase
import Dominion
import testUtility


class TestAction_card(TestCase):
    def set_up(self):
        self.player = Dominion.Player("Ben")
        self.player.deck = []
        self.player.hand = []
        self.player.played = []
        self.player.discard = []
        self.player.aside = []
        self.player.hold = []
        self.player.actions = 0
        self.player.buys = 0
        self.player.purse = 0
        self.player.cards = 0
        return self.player

    def test_use(self):
        self.player = self.set_up()
        self.player.hand.append(Dominion.Action_card("Smithy", 4, 0, 3, 0, 0))
        self.assertEqual(len(self.player.hand), 1)
        Dominion.Action_card.use(self.player.hand[0], self.player, testUtility.get_trash())
        self.assertEqual(len(self.player.hand), 0)
        self.assertEqual(len(self.player.played), 1)

        # self.fail()

    def test_augment(self):
        self.player = self.set_up()
        self.assertEqual(self.player.actions, 0)
        self.player.hand.append(Dominion.Action_card("Laboratory", 5, 1, 2, 0, 0))
        self.player.hand.append(Dominion.Action_card("Village", 3, 2, 1, 0, 0))
        self.player.hand.append(Dominion.Action_card("Woodcutter", 3, 0, 0, 1, 2))

        self.player.deck.append(Dominion.Coin_card("Copper", 0, 1))

        for x in range(3):
            Dominion.Action_card.augment(self.player.hand[x], self.player)

        self.assertEqual(self.player.actions, 3)
        self.assertEqual(self.player.buys, 1)
        self.assertEqual(self.player.purse, 2)
        self.assertEqual(len(self.player.stack()), 4)

        # self.fail()


class TestPlayer(TestCase):
    def set_Up_Player(self):
        self.player = Dominion.Player("Ben")
        self.player.deck = []
        self.player.hand = []
        self.player.played = []
        self.player.discard = []
        self.player.aside = []
        self.player.hold = []
        self.summary = {}
        return self.player

    def test_draw(self):
        self.player = self.set_Up_Player()
        self.player.discard.append(Dominion.Coin_card("Silver", 3, 2))
        self.player.discard.append(Dominion.Coin_card("Copper", 0, 1))
        self.assertEqual((len(self.player.discard)), 2)
        Dominion.Player.draw(self.player, dest=None)
        self.assertEqual((len(self.player.deck)), 1)
        self.assertEqual((len(self.player.discard)), 0)
        self.assertEqual((len(self.player.hand)), 1)
        # self.fail()

    def test_action_balance(self):
        self.player = self.set_Up_Player()

        self.player.discard.append(Dominion.Action_card("Village", 3, 2, 1, 0, 0))
        self.player.discard.append(Dominion.Action_card("Festival", 5, 2, 0, 1, 2))
        self.assertEqual(self.player.discard[0].category, "action")
        self.assertEqual(self.player.discard[1].category, "action")
        self.actions = self.player.discard[0].actions + self.player.discard[1].actions
        self.assertEqual(self.actions, 4)
        self.balance = 0-1+2-1+2
        self.assertEqual(self.balance, 2)
        self.assertEqual((len(self.player.discard)), 2)
        Dominion.Player.draw(self.player, dest=None)
        self.assertEqual((len(self.player.stack())), 2)
        self.assertEqual(Dominion.Player.action_balance(self.player), 70*self.balance / len(self.player.stack()))

    # self.fail()

    def test_cardsummary(self):
        self.player = self.set_Up_Player()
        for x in range(2):
            self.player.hand.append(Dominion.Action_card("Village", 3, 2, 1, 0, 0))

        self.player.hand.append(Dominion.Victory_card("Estate", 2, 1))

        self.assertEqual(len(self.player.hand), 3)
        self.summary = Dominion.Player.cardsummary(self.player)

        self.assertEqual(self.summary['Village'], 2)
        self.assertEqual(self.summary['Estate'], 1)
        self.assertEqual(self.summary['VICTORY POINTS'], 1)

        # self.fail()

    def test_calcpoints(self):
        self.player = self.set_Up_Player()

        self.player.discard.append(Dominion.Victory_card("Estate", 2, 1))
        self.player.discard.append(Dominion.Victory_card("Duchy", 5, 3))
        self.player.discard.append(Dominion.Victory_card("Gardens", 4, 0))

        for x in range(7):
            self.player.discard.append(Dominion.Coin_card("Gold", 6, 3))

        self.assertEqual((len(self.player.stack())), 10)
        self.assertEqual((Dominion.Player.calcpoints(self.player)), 5)  # n = 10, gardens = 2, tally = 4

        # self.fail()

class Test(TestCase):
    def set_up(self, nV, nC):
        self.names = testUtility.get_player_names()
        self.nV = testUtility.victory_cards(self.names)
        self.nC = testUtility.curse_cards(self.names)
        self.box = testUtility.getBox(nV)
        self.supplies = testUtility.ten_cards(self.box)
        self.supply = testUtility.getSupply(0, 0, self.supplies, self.names)
        return self.supply

    def test_gameover(self):
        self.supply = { "Province": [Dominion.Victory_card("Province", 8, 6)]}
        self.assertFalse(Dominion.gameover(self.supply))

        self.supply2 = self.set_up(0, 0)
        self.assertTrue(Dominion.gameover(self.supply2))

        self.supply2["Province"] = [Dominion.Victory_card("Province", 8, 6)]
        self.assertTrue(Dominion.gameover(self.supply2))



        #self.supply.append(Dominion.Victory_card("Province", 8, 6))



        #self.fail()