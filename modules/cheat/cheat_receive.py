from network.socket.in_packet import InPacket


class CmdReceiveCheatUserInfo(InPacket):
    def __init__(self):
        super().__init__()

    def read_data(self):
        print("error = {}".format(self.get_error()))
        error_code = self.get_error()
        if error_code == 0:
            self.gold = self.get_int()
            self.gem = self.get_int()
            self.trophy = self.get_int()
            print("gold = {}".format(self.gold))
            print("gem = {}".format(self.gem))
            print("trophy = {}".format(self.trophy))


class CmdReceiveCheatLobbyChest(InPacket):
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


class CmdReceiveCheatCard(InPacket):
    def __init__(self):
        super().__init__()

    def read_data(self):
        print("error = {}".format(self.get_error()))
        error_code = self.get_error()
        if error_code == 0:
            self.card_id = self.get_int()
            self.card_level = self.get_int()
            self.card_quantity = self.get_int()
            print("card_id = {}".format(self.card_id))
            print("card_level = {}".format(self.card_level))
            print("card_quantity = {}".format(self.card_quantity))
