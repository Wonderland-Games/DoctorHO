from Foundation.Initializer import Initializer
from Foundation.TaskManager import TaskManager
from UIKit.Managers.PrototypeManager import PrototypeManager
from Foundation.DemonManager import DemonManager


PROTOTYPE_EFFECT = "MissClickEffect"
MOVIE_MISSCLICK_EFFECT = "Movie2_MissClickEffect_"


class MissClickEffect(Initializer):
    def __init__(self):
        super(MissClickEffect, self).__init__()
        self.game = None
        self.tcs = []
        self.observers = []
        self.effects = []
        self.semaphore_free = Semaphore(True, "NoEffects")
        self.movies = {}
        self.cur_pos = 0.0

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game):
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
        self.movies.clear()
        self.cur_pos = None

    # - Observers ------------------------------------------------------------------------------------------------------

    def _setupObservers(self):
        self._addObserver(Notificator.onLevelMissClicked, self._cbLevelMissClicked)

    def _cbLevelMissClicked(self):
        arrow = Mengine.getArrow()
        node = arrow.getNode()
        #position = node.getWorldPosition()
        self.cur_pos = node.getWorldPosition()

        '''
        effect = self._createEffect()
        self._placeEffect(effect, position)
        self._runEffect(effect)
        '''
        self._runEffectNew()


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

    def _runEffectNew(self):
        '''
        movie_name = MOVIE_MISSCLICK_EFFECT + "Show"
        MissClickDemon = DemonManager.getDemon("MissClick")

        prototype = MissClickDemon.generateObjectUnique(movie_name, movie_name)
        prototype_node = prototype.getEntityNode()
        search_level_node = self.game.search_level.getRoot()
        search_level_node.addChild(prototype_node)
        prototype_node.setWorldPosition(position)
        prototype.setEnable(True)
        prototype.setPlay(True)
        '''

        with self._createTaskChain() as tc:
            tc.addScope(self.showNew)
            tc.addScope(self.idleNew)
            tc.addScope(self.hideNew)

    def _createEffectNew(self, state):
        print(" * CREATE MISSCLICK EFFECT '{}'".format(state))

        movie_name = MOVIE_MISSCLICK_EFFECT + state

        print("_createEffectNew")
        miss_click_demon = DemonManager.getDemon("MissClick")
        prototype = miss_click_demon.generateObjectUnique(movie_name, movie_name)

        self.movies[state] = prototype

        prototype_node = prototype.getEntityNode()
        search_level_node = self.game.search_level.getRoot()
        search_level_node.addChild(prototype_node)

        prototype_node.setWorldPosition(self.cur_pos)
        prototype.setEnable(True)


    def _playEffectNew(self, source, state):
        print(" * PLAY MISSCLICK EFFECT '{}'".format(state))

        prototype = self.movies.get(state)
        if prototype is None:
            return

        source.addPlay(prototype, Wait=True, Loop=False)

    def _destroyEffectNew(self, state):
        print(" * DESTROY MISSCLICK EFFECT '{}'".format(state))

        prototype = self.movies.get(state)
        if prototype is None:
            return

        self.movies[state] = None

        prototype.setEnable(True)

        prototype_node = prototype.getEntityNode()
        prototype_node.removeFromParent()

        prototype.onDestroy()

    def showNew(self, source):
        # create, play, destroy show state
        source.addFunction(self._createEffectNew, "Show")
        source.addScope(self._playEffectNew, "Show")
        source.addFunction(self._destroyEffectNew, "Show")


    def idleNew(self, source):
        # create, play, destroy idle state
        source.addFunction(self._createEffectNew, "Idle")
        source.addScope(self._playEffectNew, "Idle")
        source.addFunction(self._destroyEffectNew, "Idle")


    def hideNew(self, source):
        # create, play, destroy hide state
        source.addFunction(self._createEffectNew, "Hide")
        source.addScope(self._playEffectNew, "Hide")
        source.addFunction(self._destroyEffectNew, "Hide")