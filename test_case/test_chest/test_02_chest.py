import pytest
import allure
import time

from common.logger import logger
from modules import game
from network import error_code

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
    def test_login_user(self, username, chestId, userGem, except_result, except_code, except_msg):
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
        time.sleep(0.5)
        cheat_code = cheat_module.get_cheat_user_info_code()
        assert cheat_code == error_code.SUCCESS, "invalid error cheat code"

        player_module.send_speed_up_chest(int(chestId))
        step_1(chestId)
        time.sleep(0.5)

        speed_up_chest_code = player_module.get_speed_up_chest_code()

        assert str(speed_up_chest_code) == except_code, "invalid error chest code"

        #assert except_code

        # check login success
        assert True, except_msg

        # logout
        game2.logout()
        logger.info("*************** end of test case ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_01_chest.py"])
