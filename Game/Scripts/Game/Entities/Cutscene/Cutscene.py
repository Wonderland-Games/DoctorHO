from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.GroupManager import GroupManager
from Game.Managers.CutsceneManager import CutsceneManager
from UIKit.Managers.PrototypeManager import PrototypeManager
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils


MOVIE_CONTENT = "Movie2_Content"

SLOT_SKIP = "Skip"
PROTOTYPE_SKIP = "Cutscene_Skip"
ALIAS_SKIP = "$UIText"
TEXT_SKIP = "ID_Cutscene_Skip"
SKIP_ALPHA_TIME = 200.0

SLOT_CUTSCENE = "Cutscene"
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
        self.movie_skip = None
        self.cutscene_params = None

    def _isPlayable(self):
        if self.CutsceneId is None:
            return False

        self.cutscene_params = CutsceneManager.getCutscene(self.CutsceneId)
        if self.cutscene_params is None:
            return False

        self.content = self.object.getObject(MOVIE_CONTENT)
        if self.content is None:
            return False

        return True

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        super(Cutscene, self)._onPreparation()
        if self._isPlayable() is False:
            return

        self._setupSkipMovie()
        self._setupCutscene()

    def _onActivate(self):
        super(Cutscene, self)._onActivate()
        if self._isPlayable() is False:
            Notification.notify(Notificator.onChangeScene, "Lobby")
            return

        self._runTaskChains()

    def _onDeactivate(self):
        super(Cutscene, self)._onDeactivate()
        self.content = None

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        if self.movie_skip is not None:
            self.movie_skip.onDestroy()
            self.movie_skip = None

        self.cutscene_params = None

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupSkipMovie(self):
        self.movie_skip = PrototypeManager.generateObjectUnique(PROTOTYPE_SKIP, PROTOTYPE_SKIP)
        self.movie_skip.setTextAliasEnvironment(PROTOTYPE_SKIP)
        Mengine.setTextAlias(PROTOTYPE_SKIP, ALIAS_SKIP, TEXT_SKIP)

        skip_slot = self.content.getMovieSlot(SLOT_SKIP)
        skip_node = self.movie_skip.getEntityNode()
        skip_slot.addChild(skip_node)

        _, game_height, _, bottom_offset, _, x_center, _ = AdjustableScreenUtils.getMainSizesExt()

        skip_bounds = self.movie_skip.getCompositionBounds()
        skip_size = Utils.getBoundingBoxSize(skip_bounds)
        skip_pos_y = game_height - bottom_offset - skip_size.y / 2
        skip_slot.setWorldPosition(Mengine.vec2f(x_center, skip_pos_y))

    def _setupCutscene(self):
        cutscene_slot = self.content.getMovieSlot(SLOT_CUTSCENE)
        _, _, _, _, _, x_center, y_center = AdjustableScreenUtils.getMainSizesExt()
        cutscene_slot.setWorldPosition(Mengine.vec2f(x_center, y_center))

    # - Movies ---------------------------------------------------------------------------------------------------------

    def _searchCutsceneMoviesInGroup(self):
        cutscene_movies = []
        cutscene_movie_number = 1
        movies_count_over = False

        while movies_count_over is False:

            cutscene_movie_play_name = CUTSCENE_MOVIE_TEMPLATE.format(CUTSCENE_MOVIE_STATE_PLAY, cutscene_movie_number)
            if GroupManager.hasObject(self.cutscene_params.cutscene_group_name, cutscene_movie_play_name) is False:
                movies_count_over = True
                break

            cutscene_movies.append(cutscene_movie_play_name)

            cutscene_movie_loop_name = CUTSCENE_MOVIE_TEMPLATE.format(CUTSCENE_MOVIE_STATE_LOOP, cutscene_movie_number)
            if GroupManager.hasObject(self.cutscene_params.cutscene_group_name, cutscene_movie_loop_name) is True:
                cutscene_movies.append(cutscene_movie_loop_name)

            cutscene_movie_number += 1

        return cutscene_movies

    def _validateCutsceneMovies(self, cutscene_movies):
        valid_cutscene_movies = []
        for cutscene_movie_name in cutscene_movies:
            if GroupManager.hasObject(self.cutscene_params.cutscene_group_name, cutscene_movie_name):
                valid_cutscene_movies.append(cutscene_movie_name)
            else:
                Trace.msg_err("Cutscene movie {!r} not found in group {!r}".format(cutscene_movie_name, self.cutscene_params.cutscene_group_name))

        return valid_cutscene_movies

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base + "_" + name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        cutscene_movies = self.cutscene_params.cutscene_movies
        if len(cutscene_movies) == 0:
            cutscene_movies = self._searchCutsceneMoviesInGroup()
        else:
            cutscene_movies = self._validateCutsceneMovies(cutscene_movies)

        print len(cutscene_movies), cutscene_movies

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
        # get skip movie entity node for alpha animation
        skip_node = self.movie_skip.getEntityNode()

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

                # enable and alpha out movie skip
                click_skip.addEnable(self.movie_skip)
                click_skip.addTask("TaskNodeAlphaTo", Node=skip_node, From=0.0, To=1.0, Time=SKIP_ALPHA_TIME)

                # click mouse button
                click_skip.addTask("TaskMouseButtonClick", isDown=False)

                # disable and alpha in movie skip
                click_skip.addTask("TaskNodeAlphaTo", Node=skip_node, From=1.0, To=0.0, Time=SKIP_ALPHA_TIME)
                click_skip.addDisable(self.movie_skip)

        # return cutscene movie node to its parent
        source.addReturn(cutscene_movie)
