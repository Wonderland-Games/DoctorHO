from Foundation.System import System
from Foundation.TaskManager import TaskManager
from Foundation.DefaultManager import DefaultManager
from Game.Managers.GameManager import GameManager


class SystemGlobal(System):
    def __init__(self):
        super(SystemGlobal, self).__init__()
        self._transition_scene_params = {}

    def setTransitionSceneParams(self, **params):
        self._transition_scene_params = params

    def _onRun(self):
        self.__setObservers()
        self.__runTaskChain()
        return True

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def __runTaskChain(self):
        is_skip_loading_scene = DefaultManager.getDefaultBool("DebugSkipLoadingScene", False)

        with TaskManager.createTaskChain(Name="GlobalMain") as tc:
            tc.addListener(Notificator.onRun)
            tc.addFunction(self._onLaunch)

            if is_skip_loading_scene is True:
                tc.addNotify(Notificator.onChangeScene, "Lobby")
            else:
                tc.addNotify(Notificator.onChangeScene, "Loading")

    def _onLaunch(self):
        Mengine.setCursorMode(True)
        self._runDevThings()

    # - Observers ------------------------------------------------------------------------------------------------------

    def __setObservers(self):
        self.addObserver(Notificator.onChangeScene, self.__cbSceneTransition)
        if _ANDROID is True:
            self.addObserver(Notificator.onGameDataLoaded, self.__cbAndroidGameDataLoaded)

    def __cbSceneTransition(self, scene_name):
        with TaskManager.createTaskChain() as tc:
            tc.addTask("AliasTransition", SceneName=scene_name, **self._transition_scene_params)
            tc.addFunction(self._transition_scene_params.clear)
        return False

    def __cbAndroidGameDataLoaded(self):
        playfab_id = str(Mengine.getCurrentAccountSetting("PlayFabId"))
        Mengine.androidMethod("Application", "setUserId", playfab_id)
        return False

    # - Development ----------------------------------------------------------------------------------------------------

    def _runDevThings(self):
        self.__runPlayerDataDescriber()

    def __runPlayerDataDescriber(self):
        if _DEVELOPMENT is False:
            return

        def _describe():
            player_data = GameManager.getPlayerData()
            games_data = player_data["Games"]
            for data in games_data.values():
                data.describe()

        Trace.msg_dev("[*] Press 'D' to describe all player data")

        with TaskManager.createTaskChain(Repeat=True) as tc:
            tc.addTask("TaskKeyPress", Keys=[Mengine.KC_D])
            tc.addFunction(_describe)

        # DevToDebug
        if Mengine.isAvailablePlugin("DevToDebug") is False:
            return

        tab = Mengine.getDevToDebugTab("Cheats") or Mengine.addDevToDebugTab("Cheats")
        if tab.findWidget("print_all_player_data") is None:
            widget = Mengine.createDevToDebugWidgetButton("print_all_player_data")
            widget.setTitle("Print all player data")
            widget.setClickEvent(_describe)
            tab.addWidget(widget)
