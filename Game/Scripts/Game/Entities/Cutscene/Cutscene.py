from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.GroupManager import GroupManager
from Game.Managers.CutsceneManager import CutsceneManager
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils


MOVIE_CONTENT = "Movie2_Content"
SLOT_CUTSCENE = "Cutscene"
SLOT_SKIP = "Skip"


class Cutscene(BaseEntity):
    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        Type.addAction(Type, "CutsceneId")

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

        # temp
        self.object.setParam("CutsceneId", "Intro")
        if self.CutsceneId is None:
            return

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

        self.cutscene_movie = None

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupSkipButton(self):
        pass

    def _setupCutscene(self):
        cutscene_object = CutsceneManager.getCutscene(self.CutsceneId)
        if cutscene_object is None:
            return

        cutscene_group_name = cutscene_object.cutscene_group_name
        self.cutscene_movie = GroupManager.getObject(cutscene_group_name, cutscene_object.cutscene_movie_name)
        cutscene_movie_node = self.cutscene_movie.getEntityNode()

        cutscene_slot = self.content.getMovieSlot(SLOT_CUTSCENE)
        cutscene_slot.addChild(cutscene_movie_node)

        _, _, _, _, _, x_center, y_center = AdjustableScreenUtils.getMainSizesExt()
        cutscene_slot.setWorldPosition(Mengine.vec2f(x_center, y_center))

        # temp
        self.cutscene_movie.setEnable(True)
        self.cutscene_movie.setPlay(True)
        self.cutscene_movie.setLoop(True)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base + "_" + name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        pass
