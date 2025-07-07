from Foundation.Entity.BaseScopeEntity import BaseScopeEntity


MOVIE_SHOW = "Movie2_MissClickEffect_Show"
MOVIE_IDLE = "Movie2_MissClickEffect_Idle"
MOVIE_HIDE = "Movie2_MissClickEffect_Hide"


class MissClick(BaseScopeEntity):
    ENTITY_SCOPE_REPEAT = True

    def __init__(self):
        super(MissClick, self).__init__()
        self.play_time = 1000.0 # ms
        self.x_factor = 1.0
        self.freeze_time = 10000.0 # ms

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onScopeActivate(self, source):
        super(MissClick, self)._onScopeActivate(source)

        with source.addWaitListener(self.freeze_time, Notificator.onMissClickEffect) as (source_expire, source_effect):
            source_expire.addFunction(self._resetXFactor)

            source_effect.addFunction(self._increaseXFactor)

            source_effect.addTask("TaskSetParam", ObjectName="Socket_Block", Param="Interactive", Value=True)
            source_effect.addScope(self._show)
            source_effect.addScope(self._idle)
            source_effect.addScope(self._hide)
            source_effect.addTask("TaskSetParam", ObjectName="Socket_Block", Param="Interactive", Value=False)

    def _onDeactivate(self):
        super(MissClick, self)._onDeactivate()

        self.play_time = 0.0
        self.x_factor = 0.0
        self.freeze_time = 0.0

    # - MissClick ------------------------------------------------------------------------------------------------------

    def _increaseXFactor(self):
        self.x_factor *= 2

    def _resetXFactor(self):
        self.x_factor = 1

    def _createEffect(self, movie_name, position):
        movie_prototype = self.object.generateObjectUnique(movie_name, movie_name)
        node = movie_prototype.getEntityNode()
        self.object.getEntityNode().addChild(node)

        movie_prototype.setEnable(True)
        node.setWorldPosition(position)

        return movie_prototype

    def _show(self, source):
        position = self._getCurPos()
        show_movie = self._createEffect(MOVIE_SHOW, position)
        source.addPlay(show_movie, Loop=False)
        source.addFunction(show_movie.setEnable, False)
        source.addFunction(show_movie.getEntityNode().removeFromParent)

    def _idle(self, source):
        position = self._getCurPos()
        idle_movie = self._createEffect(MOVIE_IDLE, position)

        source.addPlay(idle_movie, Wait=False, Loop=True)
        play_idle_time = self.play_time * self.x_factor
        source.addDelay(play_idle_time)
        source.addInterrupt(idle_movie)

        source.addFunction(idle_movie.setEnable, False)
        source.addFunction(idle_movie.getEntityNode().removeFromParent)

    def _hide(self, source):
        position = self._getCurPos()
        idle_movie = self._createEffect(MOVIE_HIDE, position)
        source.addPlay(idle_movie, Loop=False)
        source.addFunction(idle_movie.setEnable, False)
        source.addFunction(idle_movie.getEntityNode().removeFromParent)

    def _getCurPos(self):
        arrow = Mengine.getArrow()
        node = arrow.getNode()
        return node.getWorldPosition()