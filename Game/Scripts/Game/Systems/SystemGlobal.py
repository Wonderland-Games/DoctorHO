from Foundation.System import System
from Foundation.TaskManager import TaskManager


class SystemGlobal(System):

    def _onRun(self):
        self.__runTaskChain()
        return True

    def _onStop(self):
        pass

    def __runTaskChain(self):
        with TaskManager.createTaskChain(Name="GlobalMain") as tc:
            tc.addListener(Notificator.onRun)
            tc.addFunction(self._onLaunch)

    def _onLaunch(self):
        Mengine.setCursorMode(True)
