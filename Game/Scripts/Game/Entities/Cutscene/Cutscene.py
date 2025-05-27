from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.GroupManager import GroupManager
from Game.Managers.CutsceneManager import CutsceneManager
from UIKit.Managers.PrototypeManager import PrototypeManager
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils


MOVIE_CONTENT = "Movie2_Content"
SLOT_CUTSCENE = "Cutscene"
SLOT_SKIP = "Skip"
PROTOTYPE_SKIP = "Cutscene_Skip"

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

        self.cutscene_current_number = None
        self.cutscene_movies = {}

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
        self.skip_button = PrototypeManager.generateObjectUnique(PROTOTYPE_SKIP, PROTOTYPE_SKIP)
        self.skip_button.setTextAliasEnvironment(PROTOTYPE_SKIP)
        # self.skip_button.setEnable(True)

        skip_button_slot = self.content.getMovieSlot(SLOT_SKIP)
        skip_button_node = self.skip_button.getEntityNode()
        skip_button_slot.addChild(skip_button_node)

        _, game_height, _, bottom_offset, _, x_center, _ = AdjustableScreenUtils.getMainSizesExt()

        skip_button_bounds = self.skip_button.getCompositionBounds()
        skip_button_size = Utils.getBoundingBoxSize(skip_button_bounds)
        skip_button_pos_y = game_height - bottom_offset - skip_button_size.y / 2
        skip_button_slot.setWorldPosition(Mengine.vec2f(x_center, skip_button_pos_y))

    def _setupCutscene(self):
        self.cutscene_params = CutsceneManager.getCutscene(self.CutsceneId)
        if self.cutscene_params is None:
            return

        self.cutscene_movie_number = 1
        self.cutscene_movie_state = CUTSCENE_MOVIE_STATE_PLAY
        self.cutscene_movie_index = 0

        self.cutscene_movies = {
            1: {
                "Play": "movie_obj",
                "Loop": "movie_obj",
            },
            2: {
                "Play": "movie_obj",
                "Loop": "movie_obj",
            },
        }

        movies_count_over = False
        while movies_count_over is False:
            # self.cutscene_movies

            movies_count_over = True

        # self.cutscene_movie = self._getCutsceneMovieByNumberAndState()
        #
        # self._setupCutsceneMovie(self.cutscene_movie)

        # temp
        # self.cutscene_movie.setEnable(True)
        # self.cutscene_movie.setPlay(True)
        # self.cutscene_movie.setLoop(True)

        cutscene_slot = self.content.getMovieSlot(SLOT_CUTSCENE)
        _, _, _, _, _, x_center, y_center = AdjustableScreenUtils.getMainSizesExt()
        cutscene_slot.setWorldPosition(Mengine.vec2f(x_center, y_center))

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

    def _getNextCutsceneMovie(self):
        self.cutscene_current_number

        cutscene_group_name = self.cutscene_params.cutscene_group_name
        cutscene_movie_name = CUTSCENE_MOVIE_TEMPLATE.format("state", "number")
        cutscene_movie = GroupManager.getObject(cutscene_group_name, cutscene_movie_name)
        return cutscene_movie

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base + "_" + name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        if self.cutscene_params is None:
            return

        cutscene_movies = self.cutscene_params.cutscene_movies
        cutscene_movies_len = len(cutscene_movies)
        print cutscene_movies_len, cutscene_movies

        with self._createTaskChain(SLOT_CUTSCENE) as tc:
            # for each cutscene movie
            for cutscene_movie_name in cutscene_movies:
                cutscene_movie = GroupManager.getObject(self.cutscene_params.cutscene_group_name, cutscene_movie_name)
                if cutscene_movie is None:
                    continue

                # play cutscene movie with conditions
                tc.addScope(self._scopePlayCutsceneMovie2, cutscene_movie)

            tc.addNotify(Notificator.onChangeScene, "Lobby")

    def _scopePlayCutsceneMovie2(self, source, cutscene_movie):
        # get cutscene movie node and remember its parent
        cutscene_movie_node = cutscene_movie.getEntityNode()

        # attach cutscene movie node to cutscene slot
        cutscene_slot = self.content.getMovieSlot(SLOT_CUTSCENE)
        cutscene_slot.addChild(cutscene_movie_node)

        # get cutscene movie name to check its type
        cutscene_movie_name = cutscene_movie.getName()

        # cutscene movie state is Play
        if CUTSCENE_MOVIE_STATE_PLAY in cutscene_movie_name:
            source.addPlay(cutscene_movie, ValidationParentEnable=False)

        # cutscene movie state is Loop
        elif CUTSCENE_MOVIE_STATE_LOOP in cutscene_movie_name:
            with source.addRaceTask(2) as (play_loop, click_skip):
                # play cutscene idle movie with loop
                play_loop.addPlay(cutscene_movie, Loop=True, ValidationParentEnable=False)

                # enable skip button
                click_skip.addEnable(self.skip_button)
                click_skip.addPrint("Skip button enabled")

                # click skip button
                click_skip.addTask("TaskMovie2ButtonClick", Movie2Button=self.skip_button)
                click_skip.addPrint("Skip button clicked")

                # disable skip button
                click_skip.addDisable(self.skip_button)
                click_skip.addPrint("Skip button disabled")

        # return cutscene movie node to its parent
        source.addReturn(cutscene_movie)

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
