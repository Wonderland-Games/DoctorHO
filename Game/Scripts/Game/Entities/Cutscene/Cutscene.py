from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager


MOVIE_CONTENT = "Movie2_Content"


class Cutscene(BaseEntity):
    def __init__(self):
        super(Cutscene, self).__init__()
        self.content = None
        self.tcs = []

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        super(Cutscene, self)._onPreparation()
        self.content = self.object.getObject(MOVIE_CONTENT)
        if self.content is None:
            return

    def _onActivate(self):
        super(Cutscene, self)._onActivate()
        self._runTaskChains()

    def _onDeactivate(self):
        super(Cutscene, self)._onDeactivate()
        self.content = None

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base + "_" + name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        pass
