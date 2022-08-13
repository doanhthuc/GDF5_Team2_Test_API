import re
from cheat.cheat_receive import CmdReceiveCheatCard
from cheat.cheat_send import CmdSendCheatUserCard
from modules.base_module import BaseModule
from modules.player.player_send import *
from network.base_packet import *
from network import cmd_code, error_code
from modules.player.player_receive import *

from common.logger import logger


class PlayerModule(BaseModule):

    def __init__(self, connector):
        super().__init__(connector)

        self.set_range_cmd(1001, 4999)

        self.__player_name = ""
        self.__uId = -1

    def on_listener(self, cmd_id, raw_pkg):
        pkg = None
        if cmd_id == cmd_code.PLAYER_GET_INFO:
            pkg = CmdReceivePlayerInfo()
            pkg.init(raw_pkg)
            self.on_process_player_info(pkg)
        if cmd_id == cmd_code.GET_USER_INVENTORY:
            pkg = CmdReceiveUserInventory()
            pkg.init(raw_pkg)
            self.on_process_user_inventory(pkg)
        if cmd_id == cmd_code.OPEN_CHEST:
            pkg = CmdReceiveOpenChest()
            pkg.init(raw_pkg)
            self.on_process_open_chest(pkg)
        if cmd_id == cmd_code.SPEED_UP_CHEST:
            pkg = CmdReceiveSpeedUpChest()
            pkg.init(raw_pkg)
            self.on_process_speed_up_chest(pkg)
        if cmd_id == cmd_code.CLAIM_CHEST:
            pkg = CmdReceiveClaimChest()
            pkg.init(raw_pkg)
            self.on_process_claim_chest(pkg)
        if cmd_id == cmd_code.CHEAT_USER_CARD:
            pkg = CmdReceiveCheatCard()
            pkg.init(raw_pkg)
            self.on_process_cheat_card(pkg)
        if cmd_id == cmd_code.UPGRADE_CARD:
            pkg = CmdReceiveUpgradeCard()
            pkg.init(raw_pkg)
            self.on_process_upgrade_card(pkg)


    def send_get_player_info(self):
        pk = CmdCommonPacket(cmd_code.PLAYER_GET_INFO)
        self.send(pk)

    def on_process_player_info(self, pkg):
        self.__player_info_code = pkg.get_error()
        self.__player_name = pkg.displayName
        self.__uId = pkg.uId
        self.__gold = pkg.gold
        self.__gem = pkg.gem
        self.__trophy = pkg.trophy
        self.__server_time = pkg.server_time

    def get_player_info_code(self):
        return self.__player_info_code

    def get_player_name(self):
        return self.__player_name

    def get_uId(self):
        return self.__uId

    def get_user_gold(self):
        return self.__gold

    def get_user_gem(self):
        return self.__gem

    def send_open_chest(self, chestId):
        pkg = CmdSendOpenChest()
        pkg.set_data(chestId)
        self.send(pkg)

    def on_process_open_chest(self, pkg):
        error = pkg.get_error()
        print("check open chest ok {}".format(error))
        self.__chest_code = error

        if error == error_code.SUCCESS:
            logger.info("connect success")

    def get_open_chest_code(self):
        return self.__chest_code

    def send_speed_up_chest(self, chestId):
        pkg = CmdSendSpeedUpChest()
        pkg.set_data(chestId)
        self.send(pkg)

    def on_process_speed_up_chest(self, pkg):
        error = pkg.get_error()
        print("check speed up chest ok {}".format(error))
        self.__chest_code = error
        if error == error_code.SUCCESS:
            self.__chest_id = pkg.chest_id
            self.__state = pkg.state
            self.__gem_change = pkg.gem_change
            self.__reward_list = pkg.reward_list

        if error == error_code.SUCCESS:
            logger.info("speed up chest success")

    def get_speed_up_chest_code(self):
        return self.__chest_code

    def send_claim_chest(self, chestId):
        pkg = CmdSendClaimChest()
        pkg.set_data(chestId)
        self.send(pkg)

    def on_process_claim_chest(self, pkg):
        error = pkg.get_error()
        print("check claim chest ok {}".format(error))
        self.__chest_code = error
        if error == error_code.SUCCESS:
            self.__chest_id = pkg.chest_id
            self.__state = pkg.state
            self.__gem_change = pkg.gem_change
            self.__reward_list = pkg.reward_list

        if error == error_code.SUCCESS:
            logger.info("claim chest success")

    def send_get_user_inventory(self):
        pk = CmdCommonPacket(cmd_code.GET_USER_INVENTORY)
        self.send(pk)

    def on_process_user_inventory(self, pkg):
        error = pkg.get_error()
        print("check user inventory ok {}".format(error))
        self.__user_inventory_code = error
        if error == error_code.SUCCESS:
            self.__card_inventory = pkg.card_inventory

    def send_cheat_card(self, card_id, card_level, card_quantity):
        pk = CmdSendCheatUserCard()
        pk.set_data(card_id, card_level, card_quantity)
        self.send(pk)

    def on_process_cheat_card(self, pkg):
        error = pkg.get_error()
        self.__cheat_card_code = error
        if error == error_code.SUCCESS:
            self.__card_id = pkg.card_id
            self.__card_level = pkg.card_level
            self.__card_quantity = pkg.card_quantity
        

    def send_upgrade_card(self, cardId):
        pk = cmdSendUpgradeCard()
        pk.set_data(cardId)
        self.send(pk)

    def on_process_upgrade_card(self, pkg):
        error = pkg.get_error()
        print("upgrade card ok {}".format(error))
        self.__upgrade_card_code = error
        if error == error_code.SUCCESS:
            self.__card_id = pkg.card_id
            self.__card_level = pkg.card_level
            self.__card_quantity = pkg.card_quantity

    def get_user_inventory_code(self):
        return self.__user_inventory_code

    def get_card_inventory(self):
        return self.__card_inventory

    def get_claim_chest_code(self):
        return self.__chest_code

    def get_chest_id(self):
        return self.__chest_id

    def get_chest_state(self):
        return self.__state

    def get_gem_change(self):
        return self.__gem_change

    def get_reward_list(self):
        return self.__reward_list

    def get_chest_code(self):
        return self.__chest_code

    def get_card_id(self):
        return self.__card_id

    def get_card_level(self):
        return self.__card_level

    def get_card_quantity(self):
        return self.__card_quantity

    def get_upgrade_card_code(self):
        return self.__upgrade_card_code

    def get_cheat_card_code(self):
        return self.__cheat_card_code
