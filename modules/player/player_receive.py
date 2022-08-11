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
        self.timeServer = self.get_long()

        print("uid = {}".format(self.uId))
        print("displayName = {}".format(self.displayName))
        print("gold = {}".format(self.gold))
        print("gem = {}".format(self.gem))
        print("trophy = {}".format(self.trophy))
        print("timeServer = {}".format(self.timeServer))


class CmdReceiveOpenChest(InPacket):
    def __init__(self):
        super().__init__()

    def read_data(self):
        print("error = {}".format(self.get_error()))
        error_code = self.get_error()
        if error_code == 0:
            self.chestId = self.get_int()
            self.state = self.get_int()
            self.claimTime = self.get_long()
            print("chestId = {}".format(self.chestId))
            print("state = {}".format(self.state))
            print("claimTime = {}".format(self.claimTime))


class CmdReceiveSpeedUpChest(InPacket):
    def __init__(self):
        super().__init__()

    def read_data(self):
        print("error = {}".format(self.get_error()))
        error_code = self.get_error()
        if error_code == 0:
            self.chestId = self.get_int()
            self.state = self.get_int()
            self.claimTime = self.get_long()
            print("chestId = {}".format(self.chestId))
            print("state = {}".format(self.state))
            print("claimTime = {}".format(self.claimTime))

class CmdReceiveClaimChest(InPacket):
    def __init__(self):
        super().__init__()

    def read_data(self):
        print("error = {}".format(self.get_error()))
        error_code = self.get_error()
        if error_code == 0:
            self.chestId = self.get_int()
            self.state = self.get_int()
            self.claimTime = self.get_long()
            print("chestId = {}".format(self.chestId))
            print("state = {}".format(self.state))
            print("claimTime = {}".format(self.claimTime))
