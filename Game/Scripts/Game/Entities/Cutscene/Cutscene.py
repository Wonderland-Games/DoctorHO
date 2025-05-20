from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.GroupManager import GroupManager
from Game.Managers.CutsceneManager import CutsceneManager
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils


MOVIE_CONTENT = "Movie2_Content"
SLOT_CUTSCENE = "Cutscene"
SLOT_SKIP = "Skip"

CUTSCENE_MOVIE_STATE_PLAY = "Play"
CUTSCENE_MOVIE_STATE_LOOP = "Loop"
CUTSCENE_MOVIE_TEMPLATE = "Movie2_{}_{}"


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

        self.cutscene_params = None
        self.cutscene_movie = None
        self.cutscene_movie_index = None
        self.cutscene_movie_number = None
        self.cutscene_movie_state = None

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

        if self.cutscene_movie is not None:
            self.cutscene_movie.returnToParent()
            self.cutscene_movie = None

        self.cutscene_movie_number = None
        self.cutscene_movie_state = None
        self.cutscene_params = None
        self.cutscene_movie_index = None

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupSkipButton(self):
        pass

    def _setupCutscene(self):
        self.cutscene_params = CutsceneManager.getCutscene(self.CutsceneId)
        if self.cutscene_params is None:
            return

        self.cutscene_movie_number = 1
        self.cutscene_movie_state = CUTSCENE_MOVIE_STATE_PLAY
        self.cutscene_movie_index = 0

        # self.cutscene_movie = self._getCutsceneMovieByNumberAndState()
        #
        # self._setupCutsceneMovie(self.cutscene_movie)

        # temp
        # self.cutscene_movie.setEnable(True)
        # self.cutscene_movie.setPlay(True)
        # self.cutscene_movie.setLoop(True)

    def _setupCutsceneMovie(self, source=None):
        print "1 Cutscene movie parent: {}".format(self.cutscene_movie.getParent())
        cutscene_movie_node = self.cutscene_movie.getEntityNode()
        cutscene_slot = self.content.getMovieSlot(SLOT_CUTSCENE)
        cutscene_slot.addChild(cutscene_movie_node)

        _, _, _, _, _, x_center, y_center = AdjustableScreenUtils.getMainSizesExt()
        cutscene_slot.setWorldPosition(Mengine.vec2f(x_center, y_center))

        self.cutscene_movie.setEnable(True)

        print "2 Cutscene movie parent: {}".format(self.cutscene_movie.getParent())

    # - Movies ---------------------------------------------------------------------------------------------------------

    def _incCutsceneMovieIndex(self):
        self.cutscene_movie_index += 1

    def _getCutsceneMovieByListIndex(self):
        if self.cutscene_movie_index + 1 > len(self.cutscene_params.cutscene_movies):
            return None

        cutscene_movies = self.cutscene_params.cutscene_movies
        print ("Cutscene movies: ", cutscene_movies)

        cutscene_group_name = self.cutscene_params.cutscene_group_name
        cutscene_movie_name = self.cutscene_params.cutscene_movies[self.cutscene_movie_index]
        print ("Cutscene movie name: ", cutscene_movie_name)
        cutscene_movie = GroupManager.getObject(cutscene_group_name, cutscene_movie_name)

        return cutscene_movie

    def _getCutsceneMovieStateByName(self):
        cutscene_movie_name = self.cutscene_params.cutscene_movies[self.cutscene_movie_index]

        states = [CUTSCENE_MOVIE_STATE_PLAY, CUTSCENE_MOVIE_STATE_LOOP]
        for state in states:
            if state in cutscene_movie_name:
                return state

        return None

    def _getCutsceneMovieByNumberAndState(self):
        cutscene_movies = self.cutscene_params.cutscene_movies
        print ("Cutscene movies: ", cutscene_movies)

        cutscene_group_name = self.cutscene_params.cutscene_group_name
        cutscene_movie_name = CUTSCENE_MOVIE_TEMPLATE.format(self.cutscene_movie_state, self.cutscene_movie_number)
        print ("Cutscene movie name: ", cutscene_movie_name)
        cutscene_movie = GroupManager.getObject(cutscene_group_name, cutscene_movie_name)

        return cutscene_movie

    # def _changeCurrentCutsceneMovieState(self):

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base + "_" + name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        if self.cutscene_params is None:
            return

        with self._createTaskChain(SLOT_CUTSCENE) as tc:
            with tc.addRepeatTask() as (repeat, until):
                repeat.addScope(self._scopePlayLoop)
                until.addTask("TaskMouseButtonClick")
                until.addTask("TaskMouseButtonClick")
                until.addTask("TaskMouseButtonClick")
                until.addTask("TaskMouseButtonClick")

    def _scopePlayLoop(self, source):
        source.addScope(self._scopePlayCutsceneMovie)

        source.addTask("TaskMouseButtonClick")
        source.addFunction(self._incCutsceneMovieIndex)

    def _scopePlayCutsceneMovie(self, source):
        self.cutscene_movie = self._getCutsceneMovieByListIndex()
        self._setupCutsceneMovie()

        # source.addScope(self._setupCutsceneMovie)
        source.addPrint("3 Cutscene movie parent: {}".format(self.cutscene_movie.getParent()))
        # source.addPlay(self.cutscene_movie)
        source.addPrint(" Start playing cutscene movie: {}".format(self.cutscene_movie.getName()))
        source.addDelay(1000.0)
        source.addPrint(" End playing cutscene movie: {}".format(self.cutscene_movie.getName()))
