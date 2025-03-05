from Foundation.Manager import Manager
from Foundation.DemonManager import DemonManager


class GameManager(Manager):
    _current_game_params = None

    # - Manager --------------------------------------------------------------------------------------------------------

    @classmethod
    def _onInitialize(cls, *args):
        pass

    @classmethod
    def _onFinalize(cls):
        GameManager._current_game_params = None

    @classmethod
    def _onSave(cls):
        save_data = {}
        return save_data

    @classmethod
    def _onLoad(cls, saved_data):
        pass

    # - Game -----------------------------------------------------------------------------------------------------------

    @staticmethod
    def prepareGame(game_type, level_name):
        game = DemonManager.getDemon("GameArea")

        game.setGameType(game_type)
        game.setLevelName(level_name)

        # params_orm = GameManager.getGameLevelParams(game_type, level_name)
        # GameManager._current_game_params = params_orm

    @staticmethod
    def endGame():
        pass

    @staticmethod
    def getCurrentGameParams():
        return GameManager._current_game_params

    @staticmethod
    def getCurrentGameParam(param):
        game = DemonManager.getDemon("GameArea")
        game_param = game.getParam(param)
        return game_param
