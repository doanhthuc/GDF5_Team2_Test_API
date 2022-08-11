import pytest
import allure
import time

from common.logger import logger
from network import error_code

from utils.read_excel import *
from modules.game import Game

# get test data
test_chest_data = get_data_from_xls(
    "test_data\\test_chest.xls", "ClaimChest")


@allure.step("step 1 =>> claim chest")
def step_1(username):
    logger.info("step 1 ==> claim chest：{}".format(username))


@allure.severity(allure.severity_level.NORMAL)
@allure.epic("single_interface")
@allure.feature("login_module")
class TestClaimChest:

    @allure.story("use case - claim chest")
    @allure.description("test user opn chest ok")
    @allure.issue("https://mantistbt.zingplay.com", name="1")
    @allure.testcase("https://mantistbt.zingplay.com", name="2")
    @allure.title("Test data：【 {username}，{chestId}，{except_result}，{except_code},{except_msg}】")
    # @pytest.mark.single
    @pytest.mark.parametrize("username, chestId, except_result, except_code, except_msg", test_chest_data)
    def test_login_user(self, username, chestId, except_result, except_code, except_msg):
        logger.info("*************** start test case ***************")

        logger.info("check {} {} {} {} {}".format(
            username, chestId, except_result, except_code, except_msg))

        game2 = Game()

        game2.login(username, "1")
        step_1(username)
        time.sleep(0.5)

        login_code = game2.get_login_code()
        print("login_code = ", login_code)
        print("except_code = ", except_code)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        assert str(login_code) == except_code, "invalid error login code"

        player_module = game2.get_player_module()

        player_module.send_claim_chest(int(chestId))
        step_1(chestId)
        time.sleep(0.5)

        open_chest_code = player_module.get_speed_up_chest_code()

        assert str(open_chest_code) == except_code, "invalid error chest code"

        #assert except_code

        # check login success
        assert True, except_msg

        # logout
        game2.logout()
        logger.info("*************** end of test case ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_01_chest.py"])
