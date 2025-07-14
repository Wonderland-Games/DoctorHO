from Foundation.Entity.BaseScopeEntity import BaseScopeEntity
from Foundation.Task.Capture import Capture


MOVIE_SHOW = "Movie2_MissClickEffect_Show"
MOVIE_IDLE = "Movie2_MissClickEffect_Idle"
MOVIE_HIDE = "Movie2_MissClickEffect_Hide"


class MissClick(BaseScopeEntity):
    ENTITY_SCOPE_REPEAT = True

    def __init__(self):
        super(MissClick, self).__init__()
        self.x_factor = 1.0

    # - BaseEntity -----------------------------------------------------------

    def _onScopeActivate(self, source):
        super(MissClick, self)._onScopeActivate(source)
        mouse_position_capture = Capture(None)

        with source.addWaitListener(SETTINGS.MissClick.unfreeze_time, Notificator.onMissClickEffect, Capture=mouse_position_capture) as (source_expire, source_effect):
            source_expire.addFunction(self._resetXFactor)
            source_effect.addFunction(self._increaseXFactor)
            source_effect.addScope(self._playEffect, mouse_position_capture)

    def _onDeactivate(self):
        super(MissClick, self)._onDeactivate()

        self.x_factor = 0.0

    # - MissClick ------------------------------------------------------------

    def _playEffect(self, source, capture):
        x_pos, y_pos = capture.getArgs()
        position = Mengine.vec2f(x_pos, y_pos)
        play_idle_time = SETTINGS.MissClick.base_play_time * self.x_factor

        source.addInteractive("Socket_Block", True)
        source.addScope(self._spawnEffect, MOVIE_SHOW, position)
        source.addScope(self._spawnEffect, MOVIE_IDLE, position, wait_param=False, play_time_param=play_idle_time)
        source.addScope(self._spawnEffect, MOVIE_HIDE, position)
        source.addInteractive("Socket_Block", False)

    def _increaseXFactor(self):
        self.x_factor *= 2

    def _resetXFactor(self):
        self.x_factor = 1

    def _spawnEffect(self, source, movie_name, position, wait_param=True, play_time_param=None):
        movie_effect = self._createEffect(movie_name, position)
        source.addPlay(movie_effect, Wait=wait_param)

        if play_time_param:
            source.addDelay(play_time_param)
            source.addInterrupt(movie_effect)

        source.addFunction(movie_effect.setEnable, False)
        source.addFunction(movie_effect.getEntityNode().removeFromParent)

    def _createEffect(self, movie_name, position):
        movie_prototype = self.object.generateObjectUnique(movie_name, movie_name)
        node = movie_prototype.getEntityNode()
        self.object.getEntityNode().addChild(node)

        movie_prototype.setEnable(True)
        node.setWorldPosition(position)

        return movie_prototype
