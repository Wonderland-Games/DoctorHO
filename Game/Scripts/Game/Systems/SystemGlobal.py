from Foundation.System import System
from Foundation.TaskManager import TaskManager
from Foundation.SceneManager import SceneManager


class SystemGlobal(System):
    def __init__(self):
        super(SystemGlobal, self).__init__()
        self._change_scene_params = {}

    def _onRun(self):
        self.addObserver(Notificator.onChangeScene, self.__cbSceneTransition)

        self.__runTaskChain()
        return True

    def __cbSceneTransition(self, scene_name):
        with TaskManager.createTaskChain() as tc:
            # tc.addNotify(Notificator.onTransitionBegin, SceneManager.getCurrentSceneName(), scene_name, None)
            # tc.addTask("TaskTransition", SceneName=scene_name)
            # tc.addNotify(Notificator.onTransitionEnd, SceneManager.getCurrentSceneName(), scene_name, None)

            tc.addTask("AliasTransition", SceneName=scene_name, **self._change_scene_params)
            tc.addFunction(self._change_scene_params.clear)

        return False

    def __runTaskChain(self):
        with TaskManager.createTaskChain(Name="GlobalMain") as tc:
            tc.addListener(Notificator.onRun)
            tc.addFunction(self._onLaunch)
            tc.addNotify(Notificator.onChangeScene, "Lobby")

    def _onLaunch(self):
        Mengine.setCursorMode(True)

    def setChangeSceneParams(self, **params):
        self._change_scene_params = params
