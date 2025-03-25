from Foundation.Manager import Manager
from Foundation.DemonManager import DemonManager
from Foundation.SystemManager import SystemManager
from Foundation.DatabaseManager import DatabaseManager

from Game.Managers.GameData import PlayerGameData


class GameManager(Manager):
    s_db_module = "Database"
    s_db_name_chapters = "Chapters"
    s_db_name_levels = "Levels"

    _player_data = {}
    _current_game_params = None

    semaphore_offline_mode = Semaphore(False, "OfflineMode")

    # - Manager --------------------------------------------------------------------------------------------------------

    @classmethod
    def _onInitialize(cls, *args):
        if Mengine.hasOption("offline") is True:
            GameManager.setInternetConnection(False)

        cls.resetPlayerData()

    @classmethod
    def _onFinalize(cls):
        GameManager._player_data = {}
        GameManager._current_game_params = None

    @classmethod
    def _onSave(cls):
        save_data = {}
        return save_data

    @classmethod
    def _onLoad(cls, saved_data):
        pass

    # - PlayerData -----------------------------------------------------------------------------------------------------

    @staticmethod
    def resetPlayerData():
        new_player_data = {
            "GameData": PlayerGameData(),
            "Revision": 0,
        }
        GameManager._player_data = new_player_data

    @staticmethod
    def setDummyPlayerData():
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
    def removeGame():
        """ Finally removes current game """
        # GameManager._current_game_params = None

        game = DemonManager.getDemon("GameArea")
        game.setGameType(None)
        game.setLevelName(None)
        game.setFoundItems([])

    @staticmethod
    def getCurrentGame():
        game = DemonManager.getDemon("GameArea")
        return game

    @staticmethod
    def getCurrentGameParams():
        return GameManager._current_game_params

    @staticmethod
    def getCurrentGameParam(param):
        game = DemonManager.getDemon("GameArea")
        game_param = game.getParam(param)
        return game_param

    @staticmethod
    def getChapterLevels(chapter_name):
        pass

    @staticmethod
    def getChapterLevelParams(chapter_name, level_name):
        # chapter =
        pass

    # - Advertising ----------------------------------------------------------------------------------------------------

    @staticmethod
    def runLevelStartAdvertisement():
        """ Do not forget to call setupLevelStartAdvertisement() before. """
        system_advertising = SystemManager.getSystem("SystemAdvertising")
        game_type = GameManager.getCurrentGameParam("GameType")
        system_advertising.tryInterstitial("GameArea", "{}_level_start".format(game_type.lower()))

        # INTERNET HANDLING

    # - Internet Connection --------------------------------------------------------------------------------------------

    @staticmethod
    def hasInternetConnection():
        return GameManager.semaphore_offline_mode.getValue() is False

    @staticmethod
    def setInternetConnection(value):
        if value is True:  # has internet - off offline mode
            if GameManager.semaphore_offline_mode.getValue() is True:
                Trace.msg_dev("* Internet connection restored")
            GameManager.semaphore_offline_mode.setValue(False)
        else:
            if GameManager.semaphore_offline_mode.getValue() is False:
                Trace.msg_dev("* Internet connection lost")
            Notification.notify(Notificator.onInternetConnectionLost)
            GameManager.semaphore_offline_mode.setValue(True)
