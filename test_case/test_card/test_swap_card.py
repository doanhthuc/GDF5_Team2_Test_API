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
    "test_data\\test_card_2.xls", "SwapCard")


@allure.step("step 1 =>> all chest")
def step_1(username):
    logger.info("step 1 ==> all chest：{}".format(username))


@allure.severity(allure.severity_level.NORMAL)
@allure.epic("single_interface")
@allure.feature("chest_module")
class TestSwapCard:

    @allure.story("use case - all chest")
    @allure.description("test user Lobby chests ok")
    @allure.issue("https://mantistbt.zingplay.com", name="1")
    @allure.testcase("https://mantistbt.zingplay.com", name="2")
    @allure.title("Test data：【 {username}，{card_id_in_deck}, {card_id_in_collection}, {except_result}，{except_code},{except_msg}】")
    # @pytest.mark.single
    @pytest.mark.parametrize("username, card_id_in_deck, card_id_in_collection, , except_result, except_code, except_msg", test_chest_data)
    def test_upgrade_card(self, username, card_id_in_deck, card_id_in_collection, except_result, except_code, except_msg):
        logger.info("*************** start test case ***************")

        logger.info("check {} {} {} {} {} {}".format(
            username, card_id_in_deck, card_id_in_collection, except_result, except_code, except_msg))

        card_id_in_deck = int(card_id_in_deck)
        card_id_in_collection = int(card_id_in_collection)

        game2 = Game()

        game2.login(username, "1")
        step_1(username)
        time.sleep(0.5)

        login_code = game2.get_login_code()
        print("login_code = ", login_code)
        print("except_code = ", except_code)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        assert login_code == error_code.SUCCESS, "invalid error login code"

        player_module = game2.get_player_module()

        player_module.send_swap_card(card_id_in_collection, card_id_in_deck)
        time.sleep(0.5)
        swap_card_code = player_module.get_swap_card_code()
        assert str(swap_card_code) == except_code, "invalid error swap card code"

        player_module.send_get_user_inventory()
        time.sleep(0.5)
        inventory_code = player_module.get_user_inventory_code()
        assert inventory_code == error_code.SUCCESS, "invalid inventory error code"
        battle_deck = player_module.get_battle_deck()
        assert battle_deck is not None, "invalid battle deck"

        # check claim chest success
        assert True, except_msg

        if swap_card_code == error_code.SUCCESS:
            assert card_id_in_collection in battle_deck, "card_id_in_collection not in battle_deck after swap card"
            assert card_id_in_deck == player_module.get_card_id_in_collection(
            ), "card_id_in_deck not in collection after swap card"

        # logout
        game2.logout()
        logger.info("*************** end of test case ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_swap_card.py"])
