from Foundation.Manager import Manager
from Foundation.DemonManager import DemonManager
from Foundation.SystemManager import SystemManager
from Foundation.DatabaseManager import DatabaseManager
from Foundation.DefaultManager import DefaultManager
from Foundation.TaskManager import TaskManager
from Foundation.Providers.FacebookProvider import FacebookProvider
from PlayFab.PlayFabManager import PlayFabManager
from Game.Managers.GameData import GameDataCompressor, StoryPlayerGameData, GAME_MODE_STORY


# server statuses
SERVER_STATUS_OK = 0
SERVER_STATUS_FAIL = 1
SERVER_STATUS_UPDATING = 2
SERVER_STATUS_SOFT_UPDATE = 3
SERVER_STATUS_HARD_UPDATE = 4


class GameManager(Manager):
    s_db_module = "Database"
    s_db_name_chapters = "Chapters"
    s_db_name_levels = "Levels"
    s_db_name_quests = "Quests"

    _loading_cache = {}  # clears after loading screen
    _cache_data = {}  # always available

    __update_stats_ready = None

    _player_data = {}   # see resetPlayerData
    s_randomizer = None
    _randomizer_seed = None

    semaphore_offline_mode = Semaphore(False, "OfflineMode")

    # - Manager --------------------------------------------------------------------------------------------------------

    @staticmethod
    def _onInitialize(*args):
        if Mengine.hasOption("offline") is True:
            GameManager.setInternetConnection(False)

        GameManager.resetPlayerData()

        GameManager.updateCache()
        GameManager.initRandomizer()

    @staticmethod
    def _onFinalize():
        GameManager._cache_data = {}
        GameManager._loading_cache = {}
        GameManager._player_data = {}
        GameManager.s_randomizer = None

    @staticmethod
    def _onSave():
        save_data = {}

        # Save story data
        story_data = GameManager.getPlayerGameData(GAME_MODE_STORY)
        story_session_save = story_data.saveData()
        save_data[GAME_MODE_STORY] = story_session_save

        # Save player revision
        save_data["Revision"] = GameManager.getPlayerRevision()

        Trace.msg_dev("GameManager._onSave: {}".format(save_data))
        return save_data

    @staticmethod
    def getLocalSave():
        """ returns json string of game data saves """
        dict_save = GameManager._onSave()
        return dict_save

    @staticmethod
    def _onLoad(saved_data):
        Trace.msg_dev("GameManager._onLoad: {}".format(saved_data))
        game_data = {}

        # Load story data
        story_session_save = saved_data.get(GAME_MODE_STORY)
        if story_session_save is not None:
            story_data = GameManager.getPlayerGameData(GAME_MODE_STORY)
            ready_store_session_save = GameDataCompressor.decompress(story_session_save)
            story_data.loadData(ready_store_session_save)
            game_data[GAME_MODE_STORY] = story_session_save

        # Load player revision
        revision = saved_data.get("Revision", 0)
        GameManager.setPlayerRevision(revision)

        # Load player data cache (for cases when user is offline!)
        player_data = {
            "Games": game_data,
            "Bank": {
                "AccountInfo": {
                    "Revision": revision
                }
            }
        }

        GameManager.setLoadDataCache("PlayerData", player_data)

    # - Player data ----------------------------------------------------------------------------------------------------

    @staticmethod
    def getPlayerData():
        return GameManager._player_data

    @staticmethod
    def getPlayerGameData(game_mode=GAME_MODE_STORY):
        player_data = GameManager.getPlayerData()
        games_data = player_data["Games"]
        game_mode_data = games_data.get(game_mode, None)
        return game_mode_data

    @staticmethod
    def resetPlayerData():
        new_player_data = {
            "Games": {
                GAME_MODE_STORY: StoryPlayerGameData(),
            },
            "Revision": 0,
        }
        GameManager._player_data = new_player_data
        GameManager.clearLoadDataCache()

    @staticmethod
    def setDummyPlayerData():
        active_chapter_id, quest_index, levels_data = GameManager.getRandomPlayerData()
        Trace.msg_dev("[GameManager] set dummy player data" + "\n" +
                      " ChapterId: {}".format(active_chapter_id) + "\n" +
                      " QuestIndex: {}".format(quest_index) + "\n" +
                      " LevelsData: {}".format(levels_data))

        story_data = GameManager.getPlayerGameData(GAME_MODE_STORY)
        save_data = {
            "Data": {
                "active_chapter_id": active_chapter_id,
                "active_quest_index": quest_index,
                "levels_data": levels_data,
            }
        }
        story_data.loadData(save_data)

        GameManager.initRandomizer()  # reset randomizer

    @staticmethod
    def getPlayerRevision():
        player_data = GameManager.getPlayerData()
        player_revision = player_data["Revision"]
        return player_revision

    @staticmethod
    def setPlayerRevision(new_revision):
        player_data = GameManager.getPlayerData()
        player_revision = player_data["Revision"]
        Trace.msg_dev("[GameManager] set player revision {} -> {}".format(player_revision, new_revision))
        player_data["Revision"] = new_revision

    @staticmethod
    def incPlayerRevision():
        player_data = GameManager.getPlayerData()
        player_revision = player_data["Revision"]
        Trace.msg_dev("[GameManager] inc player revision {} -> {}".format(player_revision, player_revision + 1))
        player_data["Revision"] += 1

    # - Cache data -----------------------------------------------------------------------------------------------------

    @staticmethod
    def setCache(key, data):
        GameManager._cache_data[key] = data

    @staticmethod
    def updateCache():
        pass

    # - Loading cache data ---------------------------------------------------------------------------------------------

    @staticmethod
    def loadDataFromCache():
        Trace.msg_dev("LOAD DATA FROM CACHE START...")
        Notification.notify(Notificator.onLoadDataFromCacheBegin)

        player_data = GameManager.getLoadDataCache("PlayerData")
        Trace.msg_dev("load data from cache {}".format(player_data))

        if player_data is None:
            Trace.msg_err("GameManager loadDataFromCache failed - Player data cache is None")

            Notification.notify(Notificator.onLoadDataFromCacheEnd)
            Trace.msg_dev("... LOAD DATA FROM CACHE END")
            return

        # ------------------------------------------------
        # load games data
        games_data = player_data["Games"]

        story_data = GameManager.getPlayerGameData(GAME_MODE_STORY)
        story_save_data = GameDataCompressor.decompress(games_data[GAME_MODE_STORY])
        story_data.loadData(story_save_data)

        # bank data
        bank_data = player_data["Bank"]
        revision = bank_data["AccountInfo"].get("Revision", 0)
        GameManager.setPlayerRevision(revision)

        # ------------------------------------------------

        Notification.notify(Notificator.onLoadDataFromCacheEnd)
        Trace.msg_dev("... LOAD DATA FROM CACHE END")

    @staticmethod
    def getLoadDataCache(tag):
        return GameManager._loading_cache.get(tag)

    @staticmethod
    def setLoadDataCache(tag, data):
        Trace.msg_dev("GameManager.setLoadDataCache {}, {}".format(tag, data))
        GameManager._loading_cache[tag] = data

    @staticmethod
    def clearLoadDataCache():
        GameManager._loading_cache = {}

    # - Game params ----------------------------------------------------------------------------------------------------

    @staticmethod
    def getChapterParams(chapter_id):
        db = DatabaseManager.getDatabase(GameManager.s_db_module, GameManager.s_db_name_chapters)
        params = DatabaseManager.findDB(db, ChapterId=chapter_id)
        return params

    @staticmethod
    def getLevelParams(level_id):
        db = DatabaseManager.getDatabase(GameManager.s_db_module, GameManager.s_db_name_levels)
        params = DatabaseManager.findDB(db, LevelId=level_id)
        return params

    @staticmethod
    def getLevelParamsByChapter(chapter_id):
        params = DatabaseManager.filterDatabaseORM(GameManager.s_db_module, GameManager.s_db_name_levels,
                                                   filter=lambda param: param.ChapterId == chapter_id)
        return params

    @staticmethod
    def getQuestParamsByChapter(chapter_id):
        params = DatabaseManager.filterDatabaseORM(GameManager.s_db_module, GameManager.s_db_name_quests,
                                                   filter=lambda param: param.ChapterId == chapter_id)
        return params

    @staticmethod
    def getQuestParamsWithChapterIdAndQuestIndex(chapter_id, quest_index):
        params_list = DatabaseManager.filterDatabaseORM(GameManager.s_db_module, GameManager.s_db_name_quests,
                                                        filter=lambda param: param.ChapterId == chapter_id)

        if 0 <= quest_index < len(params_list):
            quest_params = params_list[quest_index]
            return quest_params
        else:
            return None

    @staticmethod
    def getCurrentQuestParams():
        player_data = GameManager.getPlayerGameData()
        chapter_data = player_data.getCurrentChapterData()
        chapter_id = chapter_data.getChapterId()
        current_quest_index = chapter_data.getCurrentQuestIndex()
        quest_params = GameManager.getQuestParamsWithChapterIdAndQuestIndex(chapter_id, current_quest_index)
        return quest_params

    @staticmethod
    def getQuestParamsByLevel(level_id):
        params = DatabaseManager.filterDatabaseORM(GameManager.s_db_module, GameManager.s_db_name_quests,
                                                   filter=lambda param: param.LevelId == level_id)
        return params

    @staticmethod
    def getCurrentQuestCutsceneId():
        current_quest_params = GameManager.getCurrentQuestParams()
        if current_quest_params is None:
            return None
        cutscene_id = current_quest_params.CutsceneId
        return cutscene_id

    @staticmethod
    def getRandomPlayerData():
        randomizer = GameManager.getRandomizer()

        db_chapters = DatabaseManager.getDatabase(GameManager.s_db_module, GameManager.s_db_name_chapters)
        db_chapters_params = db_chapters.getORMs()
        db_chapters_len = len(db_chapters_params)
        chapter_params_index = randomizer.getRandom(db_chapters_len)
        chapter_params = db_chapters_params[chapter_params_index]
        chapter_id = chapter_params.ChapterId

        quest_params_list = GameManager.getQuestParamsByChapter(chapter_id)
        quest_params_len = len(quest_params_list)
        quest_params_index = randomizer.getRandom(quest_params_len)

        # new
        levels_data = {}
        chapter_quests = GameManager.getQuestParamsByChapter(chapter_id)
        for i, quest_params in enumerate(chapter_quests):
            level_params = GameManager.getLevelParams(quest_params.LevelId)

            if i <= quest_params_index:
                if quest_params.LevelId in levels_data:
                    continue

                levels_data[quest_params.LevelId] = {
                    "Active": True,
                    "QuestPoints": level_params.QuestPointsToUnlock,
                }
            else:
                random_qp = randomizer.getRandom(level_params.QuestPointsToUnlock)

                levels_data[quest_params.LevelId] = {
                    "Active": False,
                    "QuestPoints": random_qp,
                }

        return chapter_id, quest_params_index, levels_data

    # - Game -----------------------------------------------------------------------------------------------------------

    @staticmethod
    def prepareGame(level_id):
        player_data = GameManager.getPlayerGameData()
        chapter_data = player_data.getCurrentChapterData()
        chapter_id = chapter_data.getChapterId()
        # level_id = chapter_data.getCurrentLevelsId()
        quest_index = chapter_data.getCurrentQuestIndex()

        quest_params = GameManager.getQuestParamsWithChapterIdAndQuestIndex(chapter_id, quest_index)

        game = DemonManager.getDemon("GameArea")
        game.setParam("ChapterId", chapter_id)
        game.setParam("LevelId", level_id)

        game.setParam("QuestIndex", None)
        if quest_params is not None:
            if quest_params.LevelId == level_id:
                game.setParam("QuestIndex", quest_index)

        player_data = GameManager.getPlayerGameData()
        player_data.setLastLevelData({})

    @staticmethod
    def endGame(game_name, is_win):
        player_data = GameManager.getPlayerGameData()
        chapter_id = GameManager.getCurrentGameParam("ChapterId")
        level_id = GameManager.getCurrentGameParam("LevelId")
        quest_index = GameManager.getCurrentGameParam("QuestIndex")

        player_data.setLastLevelData({
            "ChapterId": chapter_id,
            "LevelId": level_id,
            "QuestIndex": quest_index,
            "Result": is_win,
        })

        if is_win is True and quest_index is not None:
            current_chapter_data = player_data.getCurrentChapterData()
            current_chapter_data.setCurrentQuestIndex(quest_index + 1)

        GameManager.__apiEndGame(game_name, chapter_id, level_id, quest_index)

    @staticmethod
    def __apiEndGame(game_name, chapter_id, level_id, quest_index):
        API_FUNCTION_NAME = "API_EndGame"
        API_VERSION = 1

        GameManager.incPlayerRevision()

        if GameManager.hasInternetConnection() is False:
            Trace.log("Manager", 0, "[GameManager] user is offline to call {!r}".format(API_FUNCTION_NAME))
            return

        # current_game_params = GameManager.getCurrentGameParams()
        # if current_game_params is None:
        #     Trace.log("Manager", 0, "[GameManager] No game to end, prepare it first!")
        #     return

        # api interaction

        MAX_TRY_COUNT = 15
        DELAY_COEF = 100.0
        holder_try_count = Holder(0)
        semaphore_end = Semaphore(False, "RequestEmptyTries")

        def __inc_holder(holder):
            holder.set(holder.get() + 1)

        def __scope_delay(source, holder):
            try_count = holder.get()
            delay = try_count * DELAY_COEF
            Trace.msg_dev("[PlayFab] {} WAIT TO NEXT TRY {}".format(API_FUNCTION_NAME, delay))
            source.addDelay(delay)

        def __success_cb(result):
            GameManager.setInternetConnection(True)
            semaphore_end.setValue(True)

        def __fail_cb(playFabError):
            Mengine.logError("[PlayFab] {} fail: {}".format(API_FUNCTION_NAME, playFabError))
            GameManager.setInternetConnection(False)
            semaphore_end.setValue(True)

        def __curl_fail_cb(playFabError):
            try_count = holder_try_count.get()
            if try_count > MAX_TRY_COUNT:
                Mengine.logError("[PlayFab] {} fail: {}".format(API_FUNCTION_NAME, playFabError))
                semaphore_end.setValue(True)
                GameManager.setInternetConnection(False)
            else:
                Trace.msg_err("[PlayFab] {} fail: {}".format(API_FUNCTION_NAME, playFabError))
                Notification.notify(Notificator.onInternetConnectionFail)

        error_handlers = {
            "CloudScriptAPIRequestCountExceeded": __fail_cb,
            "CloudScriptAPIRequestError": __fail_cb,
            "CloudScriptFunctionArgumentSizeExceeded": __fail_cb,
            "CloudScriptHTTPRequestError": __fail_cb,
            "CloudScriptNotFound": __fail_cb,
            "JavascriptException": __fail_cb,
            "ServiceUnavailable": __curl_fail_cb,
        }

        with TaskManager.createTaskChain() as tc:
            with tc.addRepeatTask() as (tc_repeat, tc_until):
                tc_repeat.addFunction(__inc_holder, holder_try_count)
                tc_repeat.addScope(
                    PlayFabManager.scopeExecuteCloudScript,
                    API_FUNCTION_NAME,
                    {
                        "GameName": game_name,
                        "ChapterId": chapter_id,
                        "LevelId": level_id,
                        "QuestIndex": quest_index,
                        "__api_version__": API_VERSION
                    },
                    __success_cb, __fail_cb, **error_handlers)
                tc_repeat.addScope(__scope_delay, holder_try_count)

                tc_until.addSemaphore(semaphore_end, From=True)

    @staticmethod
    def removeGame():
        """ Finally removes current game """

        game = GameManager.getCurrentGame()
        game.setParam("ChapterId", None)
        game.setParam("LevelId", None)
        game.setParam("QuestIndex", None)
        game.setParam("FoundItems", [])

    @staticmethod
    def getCurrentGame():
        game = DemonManager.getDemon("GameArea")
        return game

    @staticmethod
    def getCurrentGameParam(param):
        game = GameManager.getCurrentGame()
        game_param = game.getParam(param)
        return game_param

    # - Advertising ----------------------------------------------------------------------------------------------------

    @staticmethod
    def runLevelStartAdvertisement(scene_name):
        """ Do not forget to call setupLevelStartAdvertisement() before. """
        system_advertising = SystemManager.getSystem("SystemAdvertising")
        system_advertising.tryInterstitial(scene_name, "{}_level_start".format(scene_name))

    # - Authentication / Register --------------------------------------------------------------------------------------

    @staticmethod
    def _getNewUserName():
        name_text_limit = DefaultManager.getDefaultInt("UserNameLength", 20)
        try:
            return '{}'.format(Mengine.generateUniqueIdentity(name_text_limit))
        except AttributeError:
            return str(Mengine.getTimeMs())[:name_text_limit]

    @staticmethod
    def _getNewPassword():
        password = str(Mengine.getConfigString("Playfab", "UserPassword", ""))
        if password == "":
            length = DefaultManager.getDefaultInt("UserPasswordLength", 64)
            password = '{}'.format(Mengine.generateUniqueIdentity(length))
        return password

    @staticmethod
    def scopeDefaultRegistration(source, success_cb, fail_cb, **error_handlers):
        default_username = GameManager._getNewUserName()
        default_password = GameManager._getNewPassword()

        Trace.msg("Playfab default registration, username={!r}".format(default_username))

        @PlayFabManager.do_before_cb(success_cb)
        def __success_cb(response):
            Mengine.changeCurrentAccountSetting("FirstLogin", u'False')
            Mengine.changeCurrentAccountSetting("PlayFabId", response.get("PlayFabId"))
            Mengine.changeCurrentAccountSetting("FirstName", unicode(default_username))
            return response

        source.addScope(
            PlayFabManager.scopeRegisterPlayFabUser,
            default_username, default_password,
            __success_cb, fail_cb, **error_handlers)

    @staticmethod
    def scopeAuthenticate(source, isSuccessHolder):
        def __error(func):
            def __wrapper(*args, **kwargs):
                func(*args, **kwargs)

                GameManager.setInternetConnection(False)  # enable offline mode
                if isSuccessHolder is not None:
                    isSuccessHolder.set(False)

            return __wrapper

        def __success(func):
            def __wrapper(response):
                login_playfab_id = response.get("PlayFabId")

                if Mengine.getCurrentAccountSetting("PlayFabId") != login_playfab_id:
                    Mengine.changeCurrentAccountSetting("PlayFabId", login_playfab_id)

                Mengine.saveAccounts()
                GameManager.setInternetConnection(True)

                func(response)

                if isSuccessHolder is not None:
                    isSuccessHolder.set(True)

            return __wrapper

        @__success
        def __success_cb(response):
            login_playfab_id = response.get("PlayFabId")
            Notification.notify(Notificator.onUserAuthSuccess, UserId=login_playfab_id, Provider="PlayFab")

        @__error
        def __fail_cb(playFabError):
            Mengine.logError("[PlayFab] Authenticate with PlayFab fail: {}".format(playFabError))
            Notification.notify(Notificator.onUserAuthFail, Description=playFabError, Provider="PlayFab")

        @__success
        def __register_success_cb(response):
            playfab_id = response.get("PlayFabId")
            Notification.notify(Notificator.onUserRegistrationSuccess, UserId=playfab_id, Provider="PlayFab")
            Notification.notify(Notificator.onUserAuthSuccess, UserId=playfab_id, Provider="PlayFab")

        @__error
        def __register_fail_cb(playFabError):
            Mengine.logError("[PlayFab] Register with PlayFab fail: {}".format(playFabError))
            Notification.notify(Notificator.onUserRegistrationFail, Description=playFabError, Provider="PlayFab")
            Notification.notify(Notificator.onUserAuthFail, Description=playFabError, Provider="PlayFab")

        @__success
        def __fb_success_cb(response):
            login_playfab_id = response.get("PlayFabId")
            Notification.notify(Notificator.onUserAuthSuccess, UserId=login_playfab_id, Provider="Facebook")

        def __fb_fail_cb(error):
            Mengine.logError("[PlayFab] Authenticate with Facebook fail: {}".format(error))
            Notification.notify(Notificator.onUserAuthFail, Description=error, Provider="Facebook")
            Trace.msg("Logout from facebook, error={}. Please login again".format(error))
            FacebookProvider.logout()
            if isSuccessHolder is not None:
                isSuccessHolder.set(False)  # restart auth

        error_handlers = dict(
            AccountNotFound=__fail_cb,
            InvalidEmailOrPassword=__fail_cb,
            InvalidUsernameOrPassword=__fail_cb,
            InvalidTitleId=__fail_cb,
            RequestViewConstraintParamsNotAllowed=__fail_cb,
            EvaluationModePlayerCountExceeded=__fail_cb,
            EncryptionKeyMissing=__fail_cb,
            PlayerSecretNotConfigured=__fail_cb,
            PlayerSecretAlreadyConfigured=__fail_cb,
            # facebook
            FacebookAPIError=__fb_fail_cb,
            InvalidFacebookToken=__fb_fail_cb,
        )

        Notification.notify(Notificator.onUserAuthBegin)

        timeout_delay = DefaultManager.getDefaultInt("PlayFabLoginTimeout", 15) * 1000.0
        with source.addRaceTask(2) as (auth, timeout):
            if Mengine.getCurrentAccountSettingBool("FirstLogin") is True:
                Notification.notify(Notificator.onUserAuthNeedRegister)
                Trace.msg("Authenticate: registration with playfab (FirstLogin)...")
                auth.addScope(
                    GameManager.scopeDefaultRegistration,
                    __register_success_cb, __register_fail_cb, **error_handlers)
            elif Mengine.getGameParamBool("Facebook", False) is True and FacebookProvider.isLoggedIn() is True:
                Trace.msg("Authenticate: login with facebook...")
                fb_access_token = FacebookProvider.getAccessToken()
                auth.addScope(
                    PlayFabManager.scopeLoginFacebookAccount,
                    fb_access_token, False,
                    __fb_success_cb, __fb_fail_cb, **error_handlers)
            else:
                username = Mengine.getCurrentAccountSetting("Name")
                password = Mengine.getCurrentAccountSetting("Password")

                Trace.msg("Authenticate: login with playfab...")
                auth.addScope(
                    PlayFabManager.scopeLoginWithPlayFab,
                    username, password,
                    __success_cb, __fail_cb, **error_handlers)

            timeout.addDelay(timeout_delay)
            timeout.addFunction(__fail_cb, "Timeout")

    # - Version Control and Data Loading -------------------------------------------------------------------------------

    @staticmethod
    def scopePlayerLoggedIn(source, isSuccessHolder=None):
        API_FUNCTION_NAME = "API_OnPlayerLoggedIn"
        API_VERSION = 1

        client_project_version = Utils.getCurrentBuildVersionNumber()
        client_platform = Utils.getCurrentPlatform().lower()
        is_publish = _BUILD_PUBLISH
        token = Mengine.getConfigString("Playfab", "Token", "")
        local_save = GameManager.getLocalSave()

        def __success_cb(data):
            GameManager.setInternetConnection(True)

            Trace.msg_dev("[PlayFab] {} success: {}".format(API_FUNCTION_NAME, data))

            server_status = data.get("ServerStatus")
            update_link = data.get("UpdateLink")
            player_data = data.get("PlayerData")

            def check_data():
                if GameManager._checkServerStatus(server_status) is False:
                    return False
                if GameManager._checkVersionStatus(server_status, update_link) is False:
                    return False
                return True

            if check_data() is False:
                Notification.notify(Notificator.onLoadFromServerFail, Name="PlayerData",
                                    Description="VersionControlFailed")
                if isSuccessHolder is not None:
                    isSuccessHolder.set(False)
                return

            GameManager.setLoadDataCache("PlayerData", player_data)

            Notification.notify(Notificator.onLoadFromServerSuccess, Name="PlayerData")
            if isSuccessHolder is not None:
                isSuccessHolder.set(True)

        def __fail_cb(playFabError):
            Mengine.logError("[PlayFab] {} fail: {}".format(API_FUNCTION_NAME, playFabError))
            GameManager.setInternetConnection(False)
            Notification.notify(Notificator.onLoadFromServerFail, Name="PlayerData", Description=playFabError)

            if isSuccessHolder is not None:
                isSuccessHolder.set(False)

        error_handlers = {
            "CloudScriptAPIRequestCountExceeded": __fail_cb,
            "CloudScriptAPIRequestError": __fail_cb,
            "CloudScriptFunctionArgumentSizeExceeded": __fail_cb,
            "CloudScriptHTTPRequestError": __fail_cb,
            "CloudScriptNotFound": __fail_cb,
            "JavascriptException": __fail_cb,
        }

        Notification.notify(Notificator.onLoadFromServerBegin, Name="PlayerData")

        source.addScope(
            PlayFabManager.scopeExecuteCloudScript,
            API_FUNCTION_NAME,
            {
                "ProjectVersion": client_project_version,
                "Platform": client_platform,
                "IsPublish": is_publish,
                "Token": token,
                "LocalSave": local_save,
                "__api_version__": API_VERSION
            },
            __success_cb, __fail_cb, **error_handlers)

    @staticmethod
    def _checkServerStatus(server_status):
        """
            Checking PlayFab ServerStatus having previously taken ServerStatus from PlayFab response data
        """
        if server_status is None:
            Trace.log("Manager", 0, "GameManager | PlayFab`s ServerStatus is None")
            # Notification.notify(Notificator.onMessageOkPopUp, "ServerFail")
            Notification.notify(Notificator.onServerFail)
            return False

        if server_status is SERVER_STATUS_FAIL:
            Trace.msg_err(" PlayFab`s ServerStatus: FAIL ".center(79, "~"))
            # Notification.notify(Notificator.onMessageOkPopUp, "ServerFail")
            Notification.notify(Notificator.onServerFail)
            return False

        if server_status is SERVER_STATUS_UPDATING:
            Trace.msg_err(" PlayFab`s ServerStatus: UPDATING ".center(79, "~"))
            # Notification.notify(Notificator.onMessageOkPopUp, "ServerUpdating")
            Notification.notify(Notificator.onServerMaintenance)
            return False

        return True

    @staticmethod
    def _checkVersionStatus(version_status, update_link):
        """
           Checking PlayFab ProjectVersion having previously taken ProjectVersion from PlayFab response data
        """
        if version_status is None:
            Trace.log("Manager", 0, "GameManager | PlayFab`s ProjectVersion is None")
            # Notification.notify(Notificator.onMessageOkPopUp, "ServerFail")
            Notification.notify(Notificator.onServerFail)
            return False

        if version_status is SERVER_STATUS_SOFT_UPDATE:
            Trace.msg_dev(" PlayFab`s ProjectVersion: AVAILABLE SOFT UPDATE ".center(79, "~"))
            Trace.msg_dev(" PlayFab`s UpdateLink: {} ".format(update_link).center(79, "~"))
            Notification.notify(Notificator.onUpdateSoft, update_link)
            return True

        if version_status is SERVER_STATUS_HARD_UPDATE:
            Trace.msg_dev(" PlayFab`s ProjectVersion: NEED HARD UPDATE ".center(79, "~"))
            Trace.msg_dev(" PlayFab`s UpdateLink: {} ".format(update_link).center(79, "~"))
            Notification.notify(Notificator.onUpdateHard, update_link)
            return False

        return True

    @staticmethod
    def scopeGetAccountInfo(source, isSuccessHolder):
        def __error(func):
            def __wrapper(*args, **kwargs):
                func(*args, **kwargs)

                GameManager.setInternetConnection(False)
                if isSuccessHolder is not None:
                    isSuccessHolder.set(False)

            return __wrapper

        def __success_cb(response):
            if _DEVELOPMENT:
                Trace.msg("scopeGetAccountInfo success {}".format(response))
            else:
                Trace.msg("PlayFab GetAccountInfo [{}] created at {} success".format(
                    response.get("PlayFabId"), response.get("Created")))

            Mengine.saveAccounts()
            GameManager.setInternetConnection(True)

            title_info = response.get("TitleInfo", {})
            display_name = title_info.get("DisplayName")

            if display_name is not None:
                GameManager.setDisplayName(unicode(display_name))
            else:
                PlayFabManager.setDefaultDisplayName()

            if isSuccessHolder is not None:
                isSuccessHolder.set(True)

            Notification.notify(Notificator.onLoadFromServerSuccess, Name="AccountInfo")

        @__error
        def __fail_cb(playFabError):
            Mengine.logError("[PlayFab] GetAccountInfo fail: {}".format(playFabError))
            Notification.notify(Notificator.onLoadFromServerFail, Name="AccountInfo", Description=playFabError)

        Notification.notify(Notificator.onLoadFromServerBegin, Name="AccountInfo")

        error_handlers = dict(
            AccountNotFound=__fail_cb,
        )
        source.addScope(
            PlayFabManager.scopeGetAccountInfo,
            __success_cb, __fail_cb, **error_handlers)

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

    # - Other ----------------------------------------------------------------------------------------------------------

    @staticmethod
    def getDisplayName():
        display_name = Mengine.getCurrentAccountSetting("DisplayName")
        return display_name

    @staticmethod
    def setDisplayName(display_name):
        Mengine.changeCurrentAccountSetting("DisplayName", unicode(display_name))
        Notification.notify(Notificator.onDisplayNameChanged, display_name)

    @staticmethod
    def getCurrentHeader():
        for name in ["Header", "GameHeader"]:
            demon = DemonManager.getDemon(name)
            if demon.isActive():
                return demon
        return None

    # - Randomizer -----------------------------------------------------------------------------------------------------

    @staticmethod
    def generateSeed():
        return Mengine.rand(1000000)

    @staticmethod
    def initRandomizer(seed=None):
        randomizer = Mengine.generateRandomizer("MT19937Randomizer")
        GameManager.s_randomizer = randomizer
        GameManager.updateRandomizerSeed(seed)

    @staticmethod
    def updateRandomizerSeed(seed=None):
        randomizer = GameManager.getRandomizer()

        if seed is None:
            DebugRandomizerSeed = DefaultManager.getDefault("GameRandomizerSeed", "Random")
            if DebugRandomizerSeed == "Random":
                seed = Mengine.rand(100000)
            else:
                seed = int(DebugRandomizerSeed)

        randomizer.setSeed(seed)
        GameManager._randomizer_seed = seed
        Trace.msg_dev("Randomizer seed: {}".format(seed))

    @staticmethod
    def getRandomizer():
        return GameManager.s_randomizer
