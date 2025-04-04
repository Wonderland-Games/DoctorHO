from Foundation.Manager import Manager
from Foundation.DemonManager import DemonManager
from Foundation.SystemManager import SystemManager
from Foundation.DatabaseManager import DatabaseManager
from Foundation.DefaultManager import DefaultManager
from Foundation.Providers.FacebookProvider import FacebookProvider
from PlayFab.PlayFabManager import PlayFabManager
from Game.Managers.GameData import PlayerGameData


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

    _loading_cache = {}  # clears after loading screen
    _cache_data = {}  # always available
    _current_game_params = None

    __update_stats_ready = None

    _player_data = {}   # see resetPlayerData
    s_randomizer = None
    _randomizer_seed = None

    semaphore_offline_mode = Semaphore(False, "OfflineMode")

    # - Manager --------------------------------------------------------------------------------------------------------

    @classmethod
    def _onInitialize(cls, *args):
        if Mengine.hasOption("offline") is True:
            GameManager.setInternetConnection(False)

        cls.resetPlayerData()

        cls.updateCache()
        cls.initRandomizer()

    @classmethod
    def _onFinalize(cls):
        GameManager._cache_data = {}
        GameManager._loading_cache = {}
        GameManager._player_data = {}
        GameManager.s_randomizer = None
        GameManager._current_game_params = None

    @classmethod
    def _onSave(cls):
        save_data = {}

        # Save game data
        # ...

        # Save player revision
        save_data["Revision"] = GameManager.getPlayerRevision()

        Trace.msg_dev("GameManager._onSave: {}".format(save_data))
        return save_data

    @staticmethod
    def getLocalSave():
        """ returns json string of game data saves """
        dict_save = GameManager._onSave()
        return dict_save

    @classmethod
    def _onLoad(cls, saved_data):
        Trace.msg_dev("GameManager._onLoad: {}".format(saved_data))
        game_data = {}

        # Load game data
        # ...

        # Load player revision
        revision = saved_data.get("Revision", 0)
        GameManager.setPlayerRevision(revision)

        # Load player data cache (for cases when user is offline!)
        player_data = {
            "Game": game_data,
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
    def resetPlayerData():
        new_player_data = {
            "Game": PlayerGameData(),
            "Revision": 0,
        }
        GameManager._player_data = new_player_data
        GameManager.clearLoadDataCache()

    @staticmethod
    def setDummyPlayerData():
        randomizer = GameManager.getRandomizer()

        active_chapter_params, active_levels_params = GameManager.getRandomChapterLevelsParams()
        # print active_chapter_params, active_level_params

        chapter = None
        level = None

        game_data = GameManager.getPlayerData()
        # game_data.loadData({chapter: level})

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
        games_data = player_data["Game"]
        # ...

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
    def getChapterParams(chapter_name):
        db = DatabaseManager.getDatabase(GameManager.s_db_module, GameManager.s_db_name_chapters)
        params = DatabaseManager.findDB(db, ChapterName=chapter_name)
        return params

    @staticmethod
    def getRandomChapterLevelsParams():
        db_chapters = DatabaseManager.getDatabase(GameManager.s_db_module, GameManager.s_db_name_chapters)
        db_chapters_params = db_chapters.getORMs()
        db_chapters_len = len(db_chapters_params)
        chapter_params_index = Mengine.rand(db_chapters_len)
        chapter_params = db_chapters_params[chapter_params_index]
        # print "Random chapter name:", chapter_params.ChapterName

        db_levels = DatabaseManager.getDatabase(GameManager.s_db_module, GameManager.s_db_name_levels)
        chapter_levels = chapter_params.Levels
        chapter_levels_len = len(chapter_levels)
        active_levels_count = Mengine.rand(chapter_levels_len) + 1
        levels_params = []
        for index in range(active_levels_count):
            chapter_level = chapter_levels[index]
            # print "Level names:", chapter_level
            level_params = DatabaseManager.findDB(db_levels, LevelName=chapter_level)
            levels_params.append(level_params)

        return chapter_params, levels_params

    @staticmethod
    def getLevelParams(level_name):
        db = DatabaseManager.getDatabase(GameManager.s_db_module, GameManager.s_db_name_levels)
        params = DatabaseManager.findDB(db, LevelName=level_name)
        return params

    # - Game -----------------------------------------------------------------------------------------------------------

    @staticmethod
    def prepareGame(level_name):
        game = DemonManager.getDemon("GameArea")
        game.setParam("LevelName", level_name)

        params_orm = GameManager.getLevelParams(level_name)
        GameManager._current_game_params = params_orm

    @staticmethod
    def endGame():
        pass

    @staticmethod
    def removeGame():
        """ Finally removes current game """
        GameManager._current_game_params = None

        game = DemonManager.getDemon("GameArea")
        game.setParam("LevelName", None)
        game.setParam("FoundItems", [])

    @staticmethod
    def getCurrentGameParams():
        return GameManager._current_game_params

    @staticmethod
    def getCurrentGame():
        game = DemonManager.getDemon("GameArea")
        return game

    @staticmethod
    def getCurrentGameParam(param):
        game = DemonManager.getDemon("GameArea")
        game_param = game.getParam(param)
        return game_param

    # - Advertising ----------------------------------------------------------------------------------------------------

    @staticmethod
    def runLevelStartAdvertisement():
        """ Do not forget to call setupLevelStartAdvertisement() before. """
        system_advertising = SystemManager.getSystem("SystemAdvertising")
        level_name = GameManager.getCurrentGameParam("LevelName")
        system_advertising.tryInterstitial("GameArea", "{}_level_start".format(level_name.lower()))

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
