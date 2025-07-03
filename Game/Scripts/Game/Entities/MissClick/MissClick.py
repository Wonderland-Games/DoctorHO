from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager


MOVIE_MISSCLICK_EFFECT = "Movie2_MissClickEffect_"


class MissClick(BaseEntity):

    def __init__(self):
        super(MissClick, self).__init__()
        self.observers = []
        self.movies = {}
        self.tcs = []

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, obj):
        super(MissClick, self)._onInitialize(obj)
        self._setupObservers()

    def _onFinalize(self):
        super(MissClick, self)._onFinalize()
        for state in self.movies.keys():
            self._destroyEffect(state)
        self.movies.clear()

        for observer in self.observers:
            Notification.removeObserver(observer)
        self.observers = []

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []


    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        super(MissClick, self)._onPreparation()

    def _onActivate(self):
        super(MissClick, self)._onActivate()
        #self._setupObservers()

    def _onDeactivate(self):
        super(MissClick, self)._onDeactivate()
        '''
        for state in self.movies.keys():
            self.movies.pop(state, None)
        self.movies = []

        for observer in self.observers:
            Notification.removeObserver(observer)
        self.observers = []

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []
        '''

    # - MissClick ------------------------------------------------------------------------------------------------------
    def _addObserver(self, identity, callback, *args, **kwargs):
        observer = Notification.addObserver(identity, callback, *args, **kwargs)
        self.observers.append(observer)
        return observer

    def _setupObservers(self):
        self._addObserver(Notificator.onMissClickEffect, self._cbMissClickEffect)

    def _cbMissClickEffect(self):
        print("SHOW AMAIZING MISSCLICK EFFECT!")

        with self._createTaskChain() as tc:
            tc.addFunction(self._createEffect, "Show")
            tc.addScope(self._playEffect, "Show")
            tc.addFunction(self._destroyEffect, "Show")

            tc.addFunction(self._createEffect, "Idle")
            tc.addScope(self._playEffect, "Idle")
            tc.addFunction(self._destroyEffect, "Idle")

            tc.addFunction(self._createEffect, "Hide")
            tc.addScope(self._playEffect, "Hide")
            tc.addFunction(self._destroyEffect, "Hide")

        return False

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

    def _createTaskChain(self, **params):
        tc_name = "%s_%s" % (self.__class__.__name__, Mengine.getTimeMs())
        tc = TaskManager.createTaskChain(Name=tc_name, **params)
        self.tcs.append(tc)
        return tc