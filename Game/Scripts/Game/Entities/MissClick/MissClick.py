from Foundation.Entity.BaseScopeEntity import BaseScopeEntity


MOVIE_MISSCLICK_EFFECT = "Movie2_MissClickEffect_"


class MissClick(BaseScopeEntity):
    ENTITY_SCOPE_REPEAT = True

    def __init__(self):
        super(MissClick, self).__init__()
        self.movies = {}

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onScopeActivate(self, source):
        super(MissClick, self)._onScopeActivate(source)
        source.addListener(Notificator.onMissClickEffect)
        source.addTask("TaskSetParam", ObjectName="Socket_Block", Param="Interactive", Value=True)
        source.addFunction(self._createEffect, "Show")
        source.addScope(self._playEffect, "Show")
        source.addFunction(self._destroyEffect, "Show")

        source.addFunction(self._createEffect, "Idle")
        source.addScope(self._playEffect, "Idle")
        source.addFunction(self._destroyEffect, "Idle")

        source.addFunction(self._createEffect, "Hide")
        source.addScope(self._playEffect, "Hide")
        source.addFunction(self._destroyEffect, "Hide")
        source.addTask("TaskSetParam", ObjectName="Socket_Block", Param="Interactive", Value=False)

    def _onDeactivate(self):
        super(MissClick, self)._onDeactivate()

        for state in self.movies.keys():
            self.movies.pop(state, None)
        self.movies = []

    # - MissClick ------------------------------------------------------------------------------------------------------
    def _createEffect(self, state):
        movie_name = MOVIE_MISSCLICK_EFFECT + state
        movie_prototype = self.object.generateObjectUnique(movie_name, movie_name)
        self.movies[state] = movie_prototype

        prototype_movie_node = movie_prototype.getEntityNode()
        self.object.getEntityNode().addChild(prototype_movie_node)
        movie_prototype.setEnable(True)

        arrow = Mengine.getArrow()
        node = arrow.getNode()
        position = node.getWorldPosition()

        prototype_movie_node.setWorldPosition(position)

    def _destroyEffect(self, state):
        movie_prototype = self.movies.get(state)

        if state in self.movies:
            del self.movies[state]

        movie_prototype.setEnable(True)

        movie_prototype_node = movie_prototype.getEntityNode()
        movie_prototype_node.removeFromParent()

    def _playEffect(self, source, state):
        movie_prototype = self.movies.get(state)
        if movie_prototype is None:
            return

        source.addPlay(movie_prototype, Loop=False)
