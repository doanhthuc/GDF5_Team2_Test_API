from modules.base_module import BaseModule
from modules.cheat.cheat_receive import *
from .cheat_send import *
from modules.connection.connection_receive import *
from modules.connection.connection_send import *
from network import cmd_code
from network import error_code

from common.logger import logger

from network.socket.out_packet import OutPacket
from network import cmd_code


class CmdSendCheat(OutPacket):
    def __init__(self, type, params):
        super().__init__()
        self.init_data(2)
        self.set_cmd_id(cmd_code.CHEAT_EVENT)
        self.__type = type
        self.__params = params

    def put_data(self):
        self.put_string(self.__type)
        self.put_byte(len(self.__params))
        for i in range(len(self.__params)):
            self.put_string(str(self.__params[i]))


class CheatModule(BaseModule):
    def __init__(self, connector):
        super().__init__(connector)

        self.set_range_cmd(7000, 7900)

    def on_listener(self, cmd_id, raw_pkg):
        print("cheat::on_listener - cmd = {}".format(cmd_id))
        pkg = None
        if cmd_id == cmd_code.CHEAT_USER_INFO:
            pkg = CmdReceiveCheatUserInfo()
            pkg.init(raw_pkg)
            self.on_process_cheat_user_info(pkg)
        elif cmd_id == cmd_code.CHEAT_LOBBY_CHEST:
            pkg = CmdReceiveCheatLobbyChest()
            pkg.init(raw_pkg)
            self.on_process_cheat_lobby_chest(pkg)

    def send_cheat(self, cheat_type, params):
        self.send(CmdSendCheat(cheat_type, params))

    def send_cheat_user_info(self, gem, gold, trophy):
        pkg = CmdCheatUserInfo()
        pkg.set_data(gem, gold, trophy)
        self.send(pkg)

    def send_cheat_gem(self, gem):
        self.send_cheat_user_info(gem, 0, 0)

    def on_process_cheat_user_info(self, pkg):
        error = pkg.get_error()
        print("check open chest ok {}".format(error))
        self.__cheat_user_info_code = error

        if error == error_code.SUCCESS:
            logger.info("cheat success")

    def get_cheat_user_info_code(self):
        print("get_cheat_user_info_code self {} ".format(
            self.__cheat_user_info_code))
        return self.__cheat_user_info_code

    def send_cheat_lobby_chest(self, chestId, chestState, chestRemainingTime):
        pkg = CmdSendCheatLobbyChest()
        pkg.set_data(chestId, chestState, chestRemainingTime)
        self.send(pkg)

    def on_process_cheat_lobby_chest(self, pkg):
        error = pkg.get_error()
        print("check open chest ok {}".format(error))
        self.__cheat_lobby_chest_code = error

        if error == error_code.SUCCESS:
            logger.info("cheat success")

    def get_cheat_lobby_chest_code(self):
        print("get_cheat_lobby_chest_code self {} ".format(
            self.__cheat_lobby_chest_code))
        return self.__cheat_lobby_chest_code
