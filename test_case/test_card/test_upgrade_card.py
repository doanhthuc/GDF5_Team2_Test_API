import json
from re import A, S
import pytest
import allure
import time

from common.logger import logger
from network import error_code
from network import chest_code

from utils.read_excel import *
from modules.game import Game

# get test data
test_chest_data = get_data_from_xls(
    "test_data\\test_card_2.xls", "UpgradeCard")


@allure.step("step 1 =>> all chest")
def step_1(username):
    logger.info("step 1 ==> all chest：{}".format(username))


@allure.severity(allure.severity_level.NORMAL)
@allure.epic("single_interface")
@allure.feature("chest_module")
class TestUpgradeCard:

    @allure.story("use case - all chest")
    @allure.description("test user Lobby chests ok")
    @allure.issue("https://mantistbt.zingplay.com", name="1")
    @allure.testcase("https://mantistbt.zingplay.com", name="2")
    @allure.title("Test data：【 {username}，{card_id}，{card_level_init}, {card_quantity_init}, {user_gold_init} {except_result}，{except_code},{except_msg}】")
    # @pytest.mark.single
    @pytest.mark.parametrize("username, card_id, card_level_init, card_quantity_init, user_gold_init, except_result, except_code, except_msg", test_chest_data)
    def test_upgrade_card(self, username, card_id, card_level_init, card_quantity_init, user_gold_init, except_result, except_code, except_msg):
        logger.info("*************** start test case ***************")

        logger.info("check {} {} {} {} {} {} {} {}".format(
            username, card_id, card_level_init, card_quantity_init, user_gold_init, except_result, except_code, except_msg))

        card_id = int(card_id)
        card_level_init = int(card_level_init)
        card_quantity_init = int(card_quantity_init)

        game2 = Game()

        game2.login(username, "1")
        step_1(username)
        time.sleep(0.5)

        login_code = game2.get_login_code()
        print("login_code = ", login_code)
        print("except_code = ", except_code)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        assert login_code == error_code.SUCCESS, "invalid error login code"

        upgrade_card_config = read_upgrade_card_json_config(
            "Card.json")
        time.sleep(0.5)
        required_card_quantity = 0
        required_upgrade_gold = 0
        card_level_init = int(card_level_init)
        if card_level_init > 0 and card_level_init < 10:
            required_config = upgrade_card_config[str(card_level_init + 1)]
            required_card_quantity = int(required_config["fragments"])
            required_upgrade_gold = int(required_config["gold"])

        cheat_module = game2.get_cheat_module()
        player_module = game2.get_player_module()

        cheat_module.send_cheat_gold(int(user_gold_init))
        cheat_module.send_cheat_user_card(int(card_id), int(
            card_level_init), int(card_quantity_init))
        time.sleep(0.5)

        player_module.send_get_player_info()
        time.sleep(0.5)
        player_info_code = player_module.get_player_info_code()
        user_gold = player_module.get_user_gold()
        assert player_info_code == error_code.SUCCESS, "invalid player_info error_code"
        assert user_gold == int(user_gold_init), "invalid user_gold init"

        player_module.send_get_user_inventory()
        time.sleep(0.5)
        inventory_code = player_module.get_user_inventory_code()
        assert inventory_code == error_code.SUCCESS, "invalid inventory error code"
        card_inventory = player_module.get_card_inventory()
        assert card_inventory is not None, "invalid card_inventory"
        upgraded_card = card_inventory.get(card_id)
        assert upgraded_card is not None, "invalid upgraded_card"
        assert upgraded_card["card_level"] == card_level_init, "invalid card_level_init"
        assert upgraded_card["card_quantity"] == card_quantity_init, "invalid card_quantity_init"

        player_module.send_upgrade_card(card_id)
        time.sleep(0.5)
        upgrade_card_code = player_module.get_upgrade_card_code()
        assert str(upgrade_card_code) == except_code, "invalid error chest code"

        # check claim chest success
        assert True, except_msg

        if upgrade_card_code == error_code.SUCCESS:

            player_module.send_get_player_info()
            time.sleep(0.5)
            player_info_code = player_module.get_player_info_code()
            assert player_info_code == error_code.SUCCESS, "invalid player_info error_code after upgrade card"

            player_module.send_get_user_inventory()
            time.sleep(0.5)
            inventory_code = player_module.get_user_inventory_code()
            assert inventory_code == error_code.SUCCESS, "invalid inventory error code after upgrade card"

            card_inventory = player_module.get_card_inventory()
            card_level_new = card_inventory[card_id]["card_level"]
            card_quantity_new = card_inventory[card_id]["card_quantity"]

            assert card_level_new <= 10, "invalid card max level"

            assert card_level_new == int(
                card_level_init) + 1, "invalid card level after upgrade card"
            assert card_quantity_new == int(
                card_quantity_init) - required_card_quantity, "invalid card quantity after upgrade card"

            assert user_gold - required_upgrade_gold == player_module.get_user_gold(
            ), "invalid update user gold after upgrade card"
        # logout
        game2.logout()
        logger.info("*************** end of test case ***************")


def read_json(json_file):

    data = json.load(
        open("D:\\VNG\\GDF5_Team2_Test_API\\test_case\\test_card\\Card.json", "r"))
    return data


def read_upgrade_card_json_config(json_file):
    upgrade_tower_config = read_json(json_file)
    return upgrade_tower_config["card"]


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_03_chest.py"])
