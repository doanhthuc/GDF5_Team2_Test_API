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
