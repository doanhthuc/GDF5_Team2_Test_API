import pytest
import allure
import time

from common.logger import logger
from modules import game
from network import chest_code, error_code

from utils.read_excel import *
from modules.game import Game

# get test data
test_chest_data = get_data_from_xls(
    "test_data\\test_chest.xls", "SpeedUpChest")


@allure.step("step 1 =>> speed up chest")
def step_1(username):
    logger.info("step 1 ==> speed up chest：{}".format(username))


@allure.severity(allure.severity_level.NORMAL)
@allure.epic("single_interface")
@allure.feature("login_module")
class TestSpeedUpChest:

    @allure.story("use case - speed up chest")
    @allure.description("test user opn chest ok")
    @allure.issue("https://mantistbt.zingplay.com", name="1")
    @allure.testcase("https://mantistbt.zingplay.com", name="2")
    @allure.title("Test data：【 {username}，{chestId}，{except_result}，{except_code},{except_msg}】")
    # @pytest.mark.single
    @pytest.mark.parametrize("username, chestId, userGem, except_result, except_code, except_msg", test_chest_data)
    def test_speed_up_chest(self, username, chestId, userGem, except_result, except_code, except_msg):
        logger.info("*************** start test case ***************")

        logger.info("check {} {} {} {} {} {}".format(
            username, chestId, userGem, except_result, except_code, except_msg))

        game2 = Game()

        game2.login(username, "1")
        step_1(username)
        time.sleep(0.5)

        login_code = game2.get_login_code()
        print("login_code = ", login_code)
        print("except_code = ", except_code)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        assert login_code == error_code.SUCCESS, "invalid error login code"

        cheat_module = game2.get_cheat_module()
        player_module = game2.get_player_module()

        cheat_module.send_cheat_gem(int(userGem))
        cheat_module.send_cheat_lobby_chest(
            int(1), chest_code.OPENING_STATE, 60 * 60 * 1000)
        time.sleep(0.5)
        cheat_code = cheat_module.get_cheat_user_info_code()
        assert cheat_code == error_code.SUCCESS, "invalid error cheat code"

        player_module.send_get_player_info()
        time.sleep(0.5)
        player_info_code = player_module.get_player_info_code()
        assert player_info_code == error_code.SUCCESS, "invalid player_info error_code"
        user_gem = player_module.get_user_gem()
        user_gold = player_module.get_user_gold()

        player_module.send_get_user_inventory()
        time.sleep(0.5)
        inventory_code = player_module.get_user_inventory_code()
        assert inventory_code == error_code.SUCCESS, "invalid inventory error code"
        card_inventory = player_module.get_card_inventory()

        player_module.send_speed_up_chest(int(chestId))
        step_1(chestId)
        time.sleep(0.5)

        speed_up_chest_code = player_module.get_speed_up_chest_code()

        #assert except_code
        assert str(speed_up_chest_code) == except_code, "invalid error chest code"

        if (speed_up_chest_code == error_code.SUCCESS):
            player_module.send_get_player_info()
            time.sleep(0.5)
            player_info_code = player_module.get_player_info_code()
            assert player_info_code == error_code.SUCCESS, "invalid player_info error_code"

            player_module.send_get_user_inventory()
            time.sleep(0.5)
            inventory_code = player_module.get_user_inventory_code()
            assert inventory_code == error_code.SUCCESS, "invalid inventory error code"

            # Check update item quantity after received from chest
            for type, quantity in player_module.get_reward_list().items():
                if type == chest_code.GOLD_TYPE:
                    assert user_gold + quantity == player_module.get_user_gold(), "invalid user_gold update"
                else:
                    assert card_inventory[type].get(
                        "card_quantity") + quantity == player_module.get_card_inventory()[type].get(
                            "card_quantity"), "invalid card_quantity update"

            gem_change = player_module.get_gem_change()

            # check speed up chest success
            assert True, except_msg

            assert user_gem + gem_change == player_module.get_user_gem(), "invalid update user gem"

        # logout
        game2.logout()
        logger.info("*************** end of test case ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_02_chest.py"])
