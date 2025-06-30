from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager


MOVIE_CONTENT = "Movie2_Content"
MOVIE_MISSCLICK_EFFECT = "Movie2_MissClick_"


class MissClick(BaseEntity):

    def __init__(self):
        super(MissClick).__init__()

        self.tcs = []

        self.root = None
        self.game = None
        self.movies = {}

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, obj, game):
        super(MissClick, self)._onInitialize(obj)
        self.game = game

        self._createRoot()

    def _onFinalize(self):
        super(MissClick, self)._onFinalize()

        self.game = None

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        super(MissClick, self)._onPreparation()

    def _onActivate(self):
        super(MissClick, self)._onActivate()

    def _onDeactivate(self):
        super(MissClick, self)._onDeactivate()

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__)

    # - Effects --------------------------------------------------------------------------------------------------------

    def _createEffect(self, state, transformation):
        print(" * CREATE MISSCLICK EFFECT '{}'".format(state))

        movie_name = MOVIE_MISSCLICK_EFFECT + state

        prototype = self.game.object.generateObjectUnique(movie_name, movie_name)
        self.movies[state] = prototype

        prototype_node = prototype.getEntityNode()
        self.root.addChild(prototype_node)

        prototype.setEnable(True)
        prototype_movie = prototype.getMovie()
        #prototype_movie.setExtraTransformation(LAYER_HINT_EFFECT_CUTOUT, transformation, True)

    def _playEffect(self, source, state):
        print(" * PLAY MISSCLICK EFFECT '{}'".format(state))

        prototype = self.movies.get(state)
        if prototype is None:
            return

        source.addPlay(prototype)

    def _destroyEffect(self, state):
        print(" * DESTROY MISSCLICK EFFECT '{}'".format(state))

        prototype = self.movies.get(state)
        if prototype is None:
            return

        self.movies[state] = None

        prototype.setEnable(True)
        prototype_movie = prototype.getMovie()
        #prototype_movie.removeExtraTransformation(LAYER_HINT_EFFECT_CUTOUT)

        prototype_node = prototype.getEntityNode()
        prototype_node.removeFromParent()

        prototype.onDestroy()

    def show(self, source, transformation):
        # create, play, destroy show state
        source.addFunction(self._createEffect, "Show", transformation)
        source.addScope(self._playEffect, "Show")
        source.addFunction(self._destroyEffect, "Show")

        # create idle state
        source.addFunction(self._createEffect, "Idle", transformation)

    def hide(self, source, transformation):
        # destroy idle state
        source.addFunction(self._destroyEffect, "Idle")

        # create, play, destroy hide state
        source.addFunction(self._createEffect, "Hide", transformation)
        source.addScope(self._playEffect, "Hide")
        source.addFunction(self._destroyEffect, "Hide")