from Foundation.Initializer import Initializer


LAYER_HINT_EFFECT_CUTOUT = "cutout"
MOVIE_HINT_EFFECT = "Movie2_HintEffect_"


class HintEffect(Initializer):
    def __init__(self):
        super(HintEffect, self).__init__()
        self.root = None
        self.game = None
        self.movies = {}

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game):
        super(HintEffect, self)._onInitialize()
        self.game = game

        self._createRoot()

    def _onFinalize(self):
        super(HintEffect, self)._onFinalize()

        for state in self.movies.keys():
            self._destroyEffect(state)
        self.movies.clear()

        if self.root is not None:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

        self.game = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__)

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    # - Effect ---------------------------------------------------------------------------------------------------------

    def _createEffect(self, state, transformation):
        print(" * CREATE HINT EFFECT '{}'".format(state))

        movie_name = MOVIE_HINT_EFFECT + state

        prototype = self.game.object.generateObjectUnique(movie_name, movie_name)
        self.movies[state] = prototype

        prototype_node = prototype.getEntityNode()
        self.root.addChild(prototype_node)

        prototype.setEnable(True)
        prototype_movie = prototype.getMovie()
        prototype_movie.setExtraTransformation(LAYER_HINT_EFFECT_CUTOUT, transformation, True)

    def _playEffect(self, source, state):
        print(" * PLAY HINT EFFECT '{}'".format(state))

        prototype = self.movies.get(state)
        if prototype is None:
            return

        source.addPlay(prototype)

    def _destroyEffect(self, state):
        print(" * DESTROY HINT EFFECT '{}'".format(state))

        prototype = self.movies.get(state)
        if prototype is None:
            return

        self.movies[state] = None

        prototype.setEnable(True)
        prototype_movie = prototype.getMovie()
        prototype_movie.removeExtraTransformation(LAYER_HINT_EFFECT_CUTOUT)

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
