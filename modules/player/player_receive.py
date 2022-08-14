from typing import Dict
from network.socket.in_packet import InPacket


class CmdReceivePlayerInfo(InPacket):
    def __init__(self):
        super().__init__()

    def read_data(self):
        self.uId = self.get_int()
        self.displayName = self.get_string()
        #self.displayName = self.get_string()
        self.gold = self.get_int()

        self.gem = self.get_int()
        self.trophy = self.get_int()
        self.server_time = self.get_long()

        print("uid = {}".format(self.uId))
        print("displayName = {}".format(self.displayName))
        print("gold = {}".format(self.gold))
        print("gem = {}".format(self.gem))
        print("trophy = {}".format(self.trophy))
        print("server_time = {}".format(self.server_time))


class CmdReceiveOpenChest(InPacket):
    def __init__(self):
        super().__init__()

    def read_data(self):
        print("error = {}".format(self.get_error()))
        error_code = self.get_error()
        if error_code == 0:
            self.chest_id = self.get_int()
            self.state = self.get_int()
            self.claim_time = self.get_long()
            print("chest_id = {}".format(self.chest_id))
            print("state = {}".format(self.state))
            print("claim_time = {}".format(self.claim_time))


class CmdReceiveSpeedUpChest(InPacket):
    def __init__(self):
        super().__init__()

    def read_data(self):
        print("error = {}".format(self.get_error()))
        error_code = self.get_error()
        if error_code == 0:
            self.chest_id = self.get_int()
            self.state = self.get_int()
            self.gem_change = self.get_int()
            self.reward_size = self.get_int()
            self.reward_list = dict()
            for _ in range(self.reward_size):
                itemType = self.get_int()
                itemQuantity = self.get_int()
                self.reward_list[itemType] = self.reward_list.get(
                    itemType, 0) + itemQuantity

            print("chest_id = {}".format(self.chest_id))
            print("state = {}".format(self.state))
            print("gem_change = {}".format(self.gem_change))
            print("reward_list = {}".format(self.reward_list))


class CmdReceiveClaimChest(InPacket):
    def __init__(self):
        super().__init__()

    def read_data(self):
        print("error = {}".format(self.get_error()))
        error_code = self.get_error()
        if error_code == 0:
            self.chest_id = self.get_int()
            self.state = self.get_int()
            self.gem_change = self.get_int()
            self.reward_size = self.get_int()
            self.reward_list = dict()
            for _ in range(self.reward_size):
                itemType = self.get_int()
                itemQuantity = self.get_int()
                self.reward_list[itemType] = self.reward_list.get(
                    itemType, 0) + itemQuantity

            print("chest_id = {}".format(self.chest_id))
            print("state = {}".format(self.state))
            print("gem_change = {}".format(self.gem_change))
            print("reward_list = {}".format(self.reward_list))


class CmdReceiveUserInventory(InPacket):
    def __init__(self):
        super().__init__()

    def read_data(self):
        print("error = {}".format(self.get_error()))
        error_code = self.get_error()
        if error_code == 0:
            self.card_inventory_size = self.get_int()
            self.card_inventory = dict()
            for _ in range(self.card_inventory_size):
                card_type = self.get_int()
                card_level = self.get_int()
                card_quantity = self.get_int()
                self.card_inventory[card_type] = {
                    "card_level": card_level,
                    "card_quantity": card_quantity
                }
            print("card_inventory = {}".format(self.card_inventory))
            self.battle_deck_size = self.get_int()
            self.battle_deck = []
            for _ in range(self.battle_deck_size):
                self.battle_deck.append(self.get_int())


class CmdReceiveUpgradeCard(InPacket):
    def __init__(self):
        super().__init__()

    def read_data(self):
        print("error = {}".format(self.get_error()))
        error_code = self.get_error()
        if error_code == 0:
            self.card_id = self.get_int()
            self.card_level = self.get_int()
            self.card_quantity = self.get_int()


class CmdReceiveSwapCard(InPacket):
    def __init__(self):
        super().__init__()

    def read_data(self):
        print("error = {}".format(self.get_error()))
        error_code = self.get_error()
        if error_code == 0:
            self.card_id_in_deck = self.get_int()
            self.card_id_in_collection = self.get_int()
