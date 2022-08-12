from network.socket.out_packet import OutPacket
from network import cmd_code


class CmdCheatUserInfo(OutPacket):
    def __init__(self):
        super().__init__()
        self.init_data(2)
        self.set_cmd_id(cmd_code.CHEAT_USER_INFO)

    def set_data(self, gem, gold, trophy):
        self.__gem = gem
        self.__gold = gold
        self.__trophy = trophy

    def put_data(self):
        self.put_int(self.__gem)
        self.put_int(self.__gold)
        self.put_int(self.__trophy)


class CmdSendCheatLobbyChest(OutPacket):
    def __init__(self):
        super().__init__()
        self.init_data(2)
        self.set_cmd_id(cmd_code.CHEAT_LOBBY_CHEST)

    def set_data(self, chestId, chestState, chestRemainingTime):
        self.__chestId = chestId
        self.__chestState = chestState
        self.__chestRemainingTime = chestRemainingTime

    def put_data(self):
        self.put_int(self.__chestId)
        self.put_int(self.__chestState)
        self.put_int(self.__chestRemainingTime)


class CmdSendGetUserInventory(OutPacket):
    def __init__(self):
        super().__init__()
        self.init_data(2)
        self.set_cmd_id(cmd_code.GET_USER_INVENTORY)

    def set_data(self, userId, inventoryId):
        self.__userId = userId
        self.__inventoryId = inventoryId


