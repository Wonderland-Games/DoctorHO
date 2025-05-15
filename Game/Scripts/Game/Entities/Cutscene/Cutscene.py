from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager


MOVIE_CONTENT = "Movie2_Content"
SLOT_CUTSCENE = "Cutscene"
SLOT_SKIP = "Skip"


class Cutscene(BaseEntity):
    def __init__(self):
        super(Cutscene, self).__init__()
        self.content = None
        self.tcs = []
        self.skip_button = None
        self.cutscene_movie = None

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        super(Cutscene, self)._onPreparation()
        self.content = self.object.getObject(MOVIE_CONTENT)
        if self.content is None:
            return

        self._setupSkipButton()
        self._setupCutscene()

    def _onActivate(self):
        super(Cutscene, self)._onActivate()
        self._runTaskChains()

    def _onDeactivate(self):
        super(Cutscene, self)._onDeactivate()
        self.content = None

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        if self.skip_button is not None:
            self.skip_button.onDestroy()
            self.skip_button = None

        if self.cutscene_movie is not None:
            self.cutscene_movie.onDestroy()
            self.cutscene_movie = None

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupSkipButton(self):
        pass

    def _setupCutscene(self):
        pass

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base + "_" + name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        pass
