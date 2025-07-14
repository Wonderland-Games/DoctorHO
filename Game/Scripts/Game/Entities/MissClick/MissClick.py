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
        position = (x_pos, y_pos)
        play_idle_time = SETTINGS.MissClick.base_play_time * self.x_factor

        source.addInteractive("Socket_Block", True)
        source.addScope(self._spawnEffect, MOVIE_SHOW, position)
        source.addScope(self._spawnEffectTime, MOVIE_IDLE, position, play_idle_time)
        source.addScope(self._spawnEffect, MOVIE_HIDE, position)
        source.addInteractive("Socket_Block", False)

    def _increaseXFactor(self):
        if self.x_factor < SETTINGS.MissClick.x_factor_limit:
            self.x_factor += 1.0


    def _resetXFactor(self):
        self.x_factor = 1.0

    def _spawnEffectTime(self, source, movie_name, position, play_time):
        movie_effect = self.object.generateObjectUnique(movie_name, movie_name, Enable=True, Position=position)
        source.addPlay(movie_effect, Wait=False)

        source.addDelay(play_time)
        source.addInterrupt(movie_effect)

        source.addFunction(movie_effect.getEntityNode().removeFromParent)
        source.addFunction(movie_effect.onDestroy)

    def _spawnEffect(self, source, movie_name, position):
        movie_effect = self.object.generateObjectUnique(movie_name, movie_name, Enable=True, Position=position)
        source.addPlay(movie_effect)
        source.addFunction(movie_effect.getEntityNode().removeFromParent)
        source.addFunction(movie_effect.onDestroy)
