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


