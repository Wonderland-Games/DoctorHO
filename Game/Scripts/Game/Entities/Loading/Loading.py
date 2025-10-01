from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.Systems.SystemAnalytics import SystemAnalytics
from Foundation.Providers.AdvertisementProvider import AdvertisementProvider
from Foundation.SystemManager import SystemManager
from UIKit.Managers.PrototypeManager import PrototypeManager
from Game.Entities.Loading.Prefetcher import Prefetcher
from Game.Managers.GameManager import GameManager


MOVIE_CONTENT = "Movie2_Content"
SLOT_PROGRESS_BAR = "LoadingBar"

PROTOTYPE_PROGRESS_BAR = "LoadingBar"
PROGRESS_BAR_TEXT_PROGRESS = "ID_LoadingBar_Progress"
PROGRESS_BAR_FOLLOW_SPEED = 0.1


class Loading(BaseEntity):
    def __init__(self):
        super(Loading, self).__init__()
        self.content = None
        self.tcs = []

        self._prefetcher = None
        self.semaphore_loading_finished = None
        self.progress_value_follower = None
        self.progressbar_loading = None

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        self.content = self.object.getObject(MOVIE_CONTENT)
        if self.content is None:
            return

        self._prefetcher = Prefetcher(self)
        self.semaphore_loading_finished = Semaphore(False, "LoadingFinished")

        self.setupLoadingProgressBar()
        self.setupLoadingProgressBarFollower()

    def _onActivate(self):
        self._runTaskChains()

    def _onDeactivate(self):
        self.content = None

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        if self.progress_value_follower is not None:
            Mengine.destroyValueFollower(self.progress_value_follower)
            self.progress_value_follower = None

        if self.progressbar_loading is not None:
            self.progressbar_loading.onDestroy()
            self.progressbar_loading = None

        self._prefetcher = None
        self.semaphore_loading_finished = None

    # - ProgressBar ----------------------------------------------------------------------------------------------------

    def setupLoadingProgressBar(self):
        slot_progress_bar = self.content.getMovieSlot(SLOT_PROGRESS_BAR)
        self.progressbar_loading = PrototypeManager.generateObjectUniqueOnNode(slot_progress_bar, PROTOTYPE_PROGRESS_BAR, PROTOTYPE_PROGRESS_BAR)
        self.progressbar_loading.setEnable(True)
        self.progressbar_loading.setValue(0)
        self.progressbar_loading.setText_ID(PROGRESS_BAR_TEXT_PROGRESS)

    def updateLoadingProgressBar(self, value):
        if self.progressbar_loading is not None:
            self.progressbar_loading.setValue(value)

        if value >= 100.0:
            self.semaphore_loading_finished.setValue(True)

    def setupLoadingProgressBarFollower(self):
        self.progress_value_follower = Mengine.createValueFollowerLinear(
            0.0,
            PROGRESS_BAR_FOLLOW_SPEED,
            self.updateLoadingProgressBar
        )

    def addLoadingProgress(self, progress):
        current_value = self.progress_value_follower.getFollow()
        new_value = current_value + progress

        self.setLoadingProgress(new_value)

    def setLoadingProgress(self, progress):
        self.progress_value_follower.setFollow(progress)
        Trace.msg("Loading progress: {} / 100.0".format(progress))

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base + "_" + name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        with self._createTaskChain("Main") as tc:
            tc.addScope(self.scopeTryLoad)
            tc.addScope(self.scopeLoadingProgressEnd)
            tc.addScope(self.scopePlay)

    def scopeTryLoad(self, source):
        source.addFunction(SystemAnalytics.sendCustomAnalytic, "loading_screen_begin", {})

        loading_steps = [
            ("PREFETCH SCRIPTS", Functor(self._prefetcher.scopePrefetchScripts, 5.0)),
            ("PREFETCH FONTS", Functor(self._prefetcher.scopePrefetchFonts, 5.0)),
            ("PREFETCH GROUPS", Functor(self._prefetcher.scopePrefetchGroups, 5.0)),
            ("LOAD DUMMY DATA", Functor(self._scopeLoadDummyData, 70.0)),
            # ("LOAD SERVER DATA", Functor(self._scopeLoadServerData, 85.0)),
            ("PREPARE SYSTEMS", Functor(self._scopePrepareSystems, 15.0)),
        ]

        for (i, (task_name, scope)), parallel in source.addParallelTaskList(enumerate(loading_steps)):
            parallel.addPrint(" PARALLEL {} START {} ".format(i, task_name).center(79, "S"))
            parallel.addScope(scope)
            parallel.addPrint(" PARALLEL {} END {} ".format(i, task_name).center(79, "E"))

        with source.addIfSemaphore(GameManager.semaphore_offline_mode, True) as (true, false):
            true.addSemaphore(self.semaphore_loading_finished, To=True)

        source.addNotify(Notificator.onGameDataLoaded)

    def _scopeLoadDummyData(self, source, progress_value):
        source.addFunction(GameManager.setDummyPlayerData)
        source.addFunction(self.addLoadingProgress, progress_value)

    def _scopePrepareSystems(self, source, progress_value):
        systems = SystemManager.getSystems()
        for name, system in systems.items():
            if system.isRun() is False:
                continue
            system.preparation(source)

        source.addFunction(self.addLoadingProgress, progress_value)

    def scopeLoadingProgressEnd(self, source):
        source.addSemaphore(self.semaphore_loading_finished, From=True)
        source.addFunction(self.setLoadingProgress, 100.0)
        source.addFunction(SystemAnalytics.sendCustomAnalytic, "loading_screen_end", {})

    def scopePlay(self, source):
        if Mengine.hasOption("nobanner") is False:
            source.addFunction(AdvertisementProvider.showBanner)

        source.addNotify(Notificator.onChangeScene, "Lobby")
