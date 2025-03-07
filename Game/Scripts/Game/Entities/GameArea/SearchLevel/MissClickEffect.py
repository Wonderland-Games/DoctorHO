from Foundation.Initializer import Initializer
from Foundation.TaskManager import TaskManager
from UIKit.Managers.PrototypeManager import PrototypeManager


PROTOTYPE_EFFECT = "MissClickEffect"


class MissClickEffect(Initializer):
    def __init__(self):
        super(MissClickEffect, self).__init__()
        self.game = None
        self.tcs = []
        self.observers = []
        self.effects = []
        self.semaphore_free = Semaphore(True, "NoEffects")

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game):
        super(MissClickEffect, self)._onInitialize()
        self.game = game
        self._setupObservers()

    def _onFinalize(self):
        super(MissClickEffect, self)._onFinalize()
        self._cleanUp()

    # - Tools ----------------------------------------------------------------------------------------------------------

    def _addObserver(self, identity, callback, *args, **kwargs):
        observer = Notification.addObserver(identity, callback, *args, **kwargs)
        self.observers.append(observer)
        return observer

    def _createTaskChain(self, **params):
        tc_name = "%s_%s" % (self.__class__.__name__, Mengine.getTimeMs())
        tc = TaskManager.createTaskChain(Name=tc_name,  **params)
        self.tcs.append(tc)
        return tc

    def _cleanUp(self):
        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        for observer in self.observers:
            Notification.removeObserver(observer)
        self.observers = []

        self._destroyEffects()

        self.semaphore_free = None
        self.game = None

    # - Observers ------------------------------------------------------------------------------------------------------

    def _setupObservers(self):
        self._addObserver(Notificator.onLevelMissClicked, self._cbLevelMissClicked)

    def _cbLevelMissClicked(self):
        arrow = Mengine.getArrow()
        node = arrow.getNode()
        position = node.getWorldPosition()

        effect = self._createEffect()
        self._placeEffect(effect, position)
        self._runEffect(effect)

        return False

    # - Effect ---------------------------------------------------------------------------------------------------------

    def _createEffect(self):
        effect = PrototypeManager.generateObjectUnique(PROTOTYPE_EFFECT, PROTOTYPE_EFFECT)
        self.effects.append(effect)
        return effect

    def _placeEffect(self, effect, position):
        effect_node = effect.getEntityNode()
        search_level_node = self.game.search_level.getRoot()
        search_level_node.addChild(effect_node)

        node = effect.getEntityNode()
        node.setWorldPosition(position)

    def _runEffect(self, effect):
        def _cb(isSkip):
            self._destroyEffect(effect)

        with self._createTaskChain(Cb=_cb) as tc:
            tc.addSemaphore(self.semaphore_free, To=False)
            tc.addEnable(effect)
            tc.addPlay(effect, Wait=True, Loop=False)
            tc.addDisable(effect)

    def _destroyEffect(self, effect):
        effect.onDestroy()
        self.effects.remove(effect)

        if len(self.effects) == 0:
            self.semaphore_free.setValue(True)

    def _destroyEffects(self):
        for effect in self.effects:
            effect.onDestroy()
        self.effects = []
