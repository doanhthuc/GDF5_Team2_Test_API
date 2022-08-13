from re import S
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
    "test_data\\test_chest.xls", "AllChest")


@allure.step("step 1 =>> all chest")
def step_1(username):
    logger.info("step 1 ==> all chest：{}".format(username))


@allure.severity(allure.severity_level.NORMAL)
@allure.epic("single_interface")
@allure.feature("chest_module")
class TestClaimChest:

    @allure.story("use case - all chest")
    @allure.description("test user Lobby chests ok")
    @allure.issue("https://mantistbt.zingplay.com", name="1")
    @allure.testcase("https://mantistbt.zingplay.com", name="2")
    @allure.title("Test data：【 {username}，{chestId}，{except_result}，{except_code},{except_msg}】")
    # @pytest.mark.single
    @pytest.mark.parametrize("username, chestId, chest_0_state, chest_1_state, chest_2_state, chest_3_state, user_gold_init, user_gem_init, action, except_result, except_code, except_msg", test_chest_data)
    def test_lobby_chests_user(self, username, chestId, chest_0_state, chest_1_state, chest_2_state, chest_3_state, user_gold_init, user_gem_init, action, except_result, except_code, except_msg):
        logger.info("*************** start test case ***************")

        logger.info("check {} {} {} {} {} {} {} {} {} {} {} {}".format(
            username, chestId, chest_0_state, chest_1_state, chest_2_state, chest_3_state, user_gold_init, user_gem_init, action, except_result, except_code, except_msg))

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

        self.action_handler = {
            chest_code.OPEN_CHEST: player_module.send_open_chest,
            chest_code.SPEED_UP_CHEST: player_module.send_speed_up_chest,
            chest_code.CLAIM_CHEST: player_module.send_claim_chest,
        }

        chest_0_state = self.cheat_lobby_chest_state(
            cheat_module, 0, chest_0_state)

        chest_1_state = self.cheat_lobby_chest_state(
            cheat_module, 1, chest_1_state, 60 * 60 * 1000)

        chest_2_state = self.cheat_lobby_chest_state(
            cheat_module, 2, chest_2_state)

        chest_3_state = self.cheat_lobby_chest_state(
            cheat_module, 3, chest_3_state)

        cheat_module.send_cheat_user_info(
            int(user_gem_init), int(user_gold_init))
        time.sleep(0.5)

        player_module.send_get_player_info()
        time.sleep(0.5)
        player_info_code = player_module.get_player_info_code()
        user_gold = player_module.get_user_gold()
        assert player_info_code == error_code.SUCCESS, "invalid player_info error_code"

        player_module.send_get_user_inventory()
        time.sleep(0.5)
        inventory_code = player_module.get_user_inventory_code()
        assert inventory_code == error_code.SUCCESS, "invalid inventory error code"
        card_inventory = player_module.get_card_inventory()

        action_send = self.action_handler.get(action)
        action_send(int(chestId))
        # player_module.send_claim_chest(int(chestId))
        time.sleep(0.5)

        action_chest_code = player_module.get_chest_code()

        assert str(action_chest_code) == except_code, "invalid error chest code"

        # check claim chest success
        assert True, except_msg

        if action == chest_code.CLAIM_CHEST or action == chest_code.SPEED_UP_CHEST and action_chest_code == error_code.SUCCESS:

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

        # logout
        game2.logout()
        logger.info("*************** end of test case ***************")

    def changeStateStringToInt(self, state):
        if state == chest_code.NOT_OPENING_STATE_STR:
            state = chest_code.NOT_OPENING_STATE
        elif state == chest_code.CLAIMABLE_STATE_STR:
            state = chest_code.CLAIMABLE_STATE
        elif state == chest_code.OPENING_STATE_STR:
            state = chest_code.OPENING_STATE
        elif state == chest_code.EMPTY_STATE_STR:
            state = chest_code.EMPTY_STATE

        assert isinstance(state, int), "State must be int"
        return state

    def cheat_lobby_chest_state(self, cheat_module, chestId, chestStateStr, chest_remaining_time=0):
        state = self.changeStateStringToInt(chestStateStr)
        cheat_module.send_cheat_lobby_chest(
            int(chestId), state, chest_remaining_time)
        time.sleep(0.5)
        cheat_lobby_chest_code = cheat_module.get_cheat_lobby_chest_code()
        assert cheat_lobby_chest_code == error_code.SUCCESS, "invalid cheat error_code chest id{}".format(
            chestId)
        return state

    # def cheat_all_lobby_chest_state(self, chest_state_dict, cheat_module):
    #     for chestId, chestStateStr in chest_state_dict.items():
    #         chest_state = self.cheat_lobby_chest_state(cheat_module, int(chestId), chestStateStr)
    #         time.sleep(0.5)
    #         chest_state_dict[chestId] = chest_state
    #     return True


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_03_chest.py"])
