from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager


MOVIE_MISSCLICK_EFFECT = "Movie2_MissClickEffects_"


class MissClick(BaseEntity):

    def __init__(self):
        super(MissClick, self).__init__()

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, obj, game=None):
        super(MissClick, self)._onInitialize(obj)

    def _onFinalize(self):
        super(MissClick, self)._onFinalize()

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        super(MissClick, self)._onPreparation()

    def _onActivate(self):
        super(MissClick, self)._onActivate()

    def _onDeactivate(self):
        super(MissClick, self)._onDeactivate()

    def _createRoot(self):
        pass

    def _show(self):
        pass

    def _hide(self):
        pass