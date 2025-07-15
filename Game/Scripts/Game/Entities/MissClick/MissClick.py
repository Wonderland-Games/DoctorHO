from Foundation.Entity.BaseScopeEntity import BaseScopeEntity
from Foundation.Task.Capture import Capture


MOVIE_POSITION_PREFIX = "Movie2_MissClickEffect"
MOVIE_BACKGROUND_PREFIX = "Movie2_MissClickEffect_Background"


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
            source_effect.addScope(self._play, mouse_position_capture)

    def _onDeactivate(self):
        super(MissClick, self)._onDeactivate()

        self.x_factor = 0.0

    # - MissClick ------------------------------------------------------------
    def _play(self, source, capture):
        x_pos, y_pos = capture.getArgs()
        position = (x_pos, y_pos)
        play_idle_time = SETTINGS.MissClick.base_play_time * self.x_factor

        source.addInteractive("Socket_Block", True)

        with source.addParallelTask(2) as (position_source, background_source):
            position_source.addScope(self._playEffectSequence, MOVIE_POSITION_PREFIX, position, play_idle_time)
            background_source.addScope(self._playEffectSequence, MOVIE_BACKGROUND_PREFIX, (0.0, 0.0), play_idle_time)

        source.addInteractive("Socket_Block", False)

    def _playEffectSequence(self, source, movie_prefix, position, play_time):
        show = "{}_Show".format(movie_prefix)
        idle = "{}_Idle".format(movie_prefix)
        hide = "{}_Hide".format(movie_prefix)

        source.addScope(self._spawnEffect, show, position)
        source.addScope(self._spawnEffectTime, idle, position, play_time)
        source.addScope(self._spawnEffect, hide, position)

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
