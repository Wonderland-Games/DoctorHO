from Foundation.System import System


class SystemGame(System):
    def __init__(self):
        super(SystemGame, self).__init__()
        pass

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self):
        super(SystemGame, self)._onInitialize()
        pass

    def _onFinalize(self):
        super(SystemGame, self)._onFinalize()
        pass

    # - System ---------------------------------------------------------------------------------------------------------

    def _onSave(self):
        super(SystemGame, self)._onSave()
        return None

    def _onLoad(self, save_dict):
        super(SystemGame, self)._onLoad(save_dict)
        pass

    def _onRun(self):
        super(SystemGame, self)._onRun()

        self.addObserver(Notificator.onChangeScene, self._onSceneEnterFilter)
        self.addObserver(Notificator.onLevelStart, self._onLevelStart)

        return True

    def _onStop(self):
        super(SystemGame, self)._onStop()
        pass

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _onSceneEnterFilter(self, scene_name):
        print("_onSceneEnterFilter", scene_name)
        if scene_name is not "GameArea":
            return False

        if self.existTaskChain("SystemGame") is True:
            self.removeTaskChain("SystemGame")

        self._runTaskChains()

        return False

    def _runTaskChains(self):
        with self.createTaskChain("SystemGame") as tc:
            tc.addPrint(" * RUN GAME LOGIC")
            tc.addNotify(Notificator.onLevelStart)

    def _onLevelStart(self):

        if self.existTaskChain("PickLevelItems") is True:
            self.removeTaskChain("PickLevelItems")

        return False

