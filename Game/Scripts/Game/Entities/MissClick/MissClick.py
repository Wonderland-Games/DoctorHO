from Foundation.Entity.BaseScopeEntity import BaseScopeEntity


MOVIE_MISSCLICK_EFFECT = "Movie2_MissClickEffect_"


class MissClick(BaseScopeEntity):
    ENTITY_SCOPE_REPEAT = True

    def __init__(self):
        super(MissClick, self).__init__()

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onScopeActivate(self, source):
        super(MissClick, self)._onScopeActivate(source)

        source.addListener(Notificator.onMissClickEffect)

        source.addTask("TaskSetParam", ObjectName="Socket_Block", Param="Interactive", Value=True)

        for state in ("Show", "Idle", "Hide"):
            source.addScope(self._createAndPlayEffect, state)

        source.addTask("TaskSetParam", ObjectName="Socket_Block", Param="Interactive", Value=False)

    def _onDeactivate(self):
        super(MissClick, self)._onDeactivate()

        for state in self.movies.keys():
            self.movies.pop(state, None)
        self.movies = []

    # - MissClick ------------------------------------------------------------------------------------------------------

    def _createAndPlayEffect(self, source, state):
        movie_name = MOVIE_MISSCLICK_EFFECT + state
        movie_prototype = self.object.generateObjectUnique(movie_name, movie_name)

        prototype_movie_node = movie_prototype.getEntityNode()
        self.object.getEntityNode().addChild(prototype_movie_node)

        movie_prototype.setEnable(True)

        position = self._getCurPos()
        prototype_movie_node.setWorldPosition(position)

        source.addPlay(movie_prototype, Loop=False)
        source.addFunction(movie_prototype.setEnable, False)
        source.addFunction(prototype_movie_node.removeFromParent)

    def _getCurPos(self):
        arrow = Mengine.getArrow()
        node = arrow.getNode()
        return node.getWorldPosition()