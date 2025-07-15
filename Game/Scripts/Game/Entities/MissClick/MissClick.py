from Foundation.Entity.BaseScopeEntity import BaseScopeEntity
from Foundation.Task.Capture import Capture


MOVIE_POSITION = "Movie2_MissClickEffect_"
MOVIE_BACKGROUND = "Movie2_MissClickEffect_Background_"
SHOW_SUFFIX = "Show"
IDLE_SUFFIX = "Idle"
HIDE_SUFFIX = "Hide"


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
        source.addScope(self._playEffect, SHOW_SUFFIX, position)
        source.addScope(self._playEffectTime, IDLE_SUFFIX, position, play_idle_time)
        source.addScope(self._playEffect, HIDE_SUFFIX, position)
        source.addInteractive("Socket_Block", False)

    def _playEffect(self, source, suffix, position):
        position_movie_name = MOVIE_POSITION + suffix
        background_movie_name = MOVIE_BACKGROUND + suffix

        with source.addParallelTask(2) as (position_source, background_source):
            position_source.addScope(self._spawnEffect, position_movie_name, position)
            background_source.addScope(self._spawnEffect, background_movie_name, position)

    def _playEffectTime(self, source, suffix, position, play_time):
        position_movie_name = MOVIE_POSITION + suffix
        background_movie_name = MOVIE_BACKGROUND + suffix

        with source.addParallelTask(2) as (position_source, background_source):
            position_source.addScope(self._spawnEffectTime, position_movie_name, position, play_time)
            background_source.addScope(self._spawnEffectTime, background_movie_name, position, play_time)

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
