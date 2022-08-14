from network.socket.out_packet import OutPacket
from network import cmd_code


class CmdSendOpenChest(OutPacket):
    def __init__(self):
        super().__init__()
        self.init_data(2)
        self.set_cmd_id(cmd_code.OPEN_CHEST)

    def set_data(self, chestId):
        self.__chestId = chestId

    def put_data(self):
        self.put_int(self.__chestId)
        print("chestId: ", self.__chestId)


class CmdSendSpeedUpChest(OutPacket):
    def __init__(self):
        super().__init__()
        self.init_data(2)
        self.set_cmd_id(cmd_code.SPEED_UP_CHEST)

    def set_data(self, chestId):
        self.__chestId = chestId

    def put_data(self):
        self.put_int(self.__chestId)
        print("chestId: ", self.__chestId)


class CmdSendClaimChest(OutPacket):
    def __init__(self):
        super().__init__()
        self.init_data(2)
        self.set_cmd_id(cmd_code.CLAIM_CHEST)

    def set_data(self, chestId):
        self.__chestId = chestId

    def put_data(self):
        self.put_int(self.__chestId)
        print("chestId: ", self.__chestId)


class CmdSendUpgradeCard(OutPacket):
    def __init__(self):
        super().__init__()
        self.init_data(2)
        self.set_cmd_id(cmd_code.UPGRADE_CARD)

    def set_data(self, cardId):
        self.__cardId = cardId

    def put_data(self):
        self.put_int(self.__cardId)
        print("cardId: ", self.__cardId)


class CmdSendSwapCard(OutPacket):
    def __init__(self):
        super().__init__()
        self.init_data(2)
        self.set_cmd_id(cmd_code.SWAP_CARD)

    def set_data(self, card_id_in_collection, card_id_in_deck):
        self.__card_id_in_collection = card_id_in_collection
        self.__card_id_in_deck = card_id_in_deck

    def put_data(self):
        self.put_int(self.__card_id_in_collection)
        self.put_int(self.__card_id_in_deck)
        print("card_id_in_collection: ", self.__card_id_in_collection)
        print("card_id_in_deck: ", self.__card_id_in_deck)
