from Foundation.System import System
from Foundation.TaskManager import TaskManager
from Foundation.DefaultManager import DefaultManager


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

    def _runDevThings(self):
        pass

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
        Mengine.androidMethod("Application", "setSessionId", playfab_id)
        return False
