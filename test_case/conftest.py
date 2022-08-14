# encoding: utf-8
import pytest
import allure
import yaml
import os
from common.read_data import data
from modules.game import Game

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_data(yaml_file_name):
    try:
        data_file_path = os.path.join(BASE_PATH, "data", yaml_file_name)
        yaml_data = data.load_yaml(data_file_path)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return yaml_data


@pytest.fixture(scope="session", autouse=True)
def env_config(request):
    """
    read config
    """
    project_name = 'api_auto_test'
    root_path = get_root_path(project_name)
    config_path = os.path.abspath(root_path + 'config/env_config.yml')
    with open(config_path) as f:
        env_config = yaml.safe_load(f)
    return env_config


def get_root_path(project_name):
    cur_path = os.path.abspath(os.path.dirname(__file__))
    root_path = cur_path[:cur_path.find(
        project_name+"\\") + len(project_name+"\\")]
    root_path = "D:/VNG/GDF5_Team2_Test_API/"
    return root_path


# init game client
#game = Game()

# print("init_game")
