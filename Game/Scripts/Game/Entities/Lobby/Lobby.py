from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.SystemManager import SystemManager
from Game.Managers.GameManager import GameManager
from Game.Entities.Lobby.ChapterLevels import ChapterLevels


MOVIE_CONTENT = "Movie2_Content"
SLOT_CHAPTER_LEVELS = "ChapterLevels"


class Lobby(BaseEntity):
    def __init__(self):
        super(Lobby, self).__init__()
        self.content = None
        self.tcs = []
        self.chapter_levels = None

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        self.content = self.object.getObject(MOVIE_CONTENT)
        if self.content is None:
            return

        self._setupChapterLevels()

    def _onActivate(self):
        self._runTaskChains()

    def _onDeactivate(self):
        self.content = None

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        if self.chapter_levels is not None:
            self.chapter_levels.onFinalize()
            self.chapter_levels = None

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupChapterLevels(self):
        # get current chapter data
        chapter_name = "MediterraneanAncientCivilizations"  # MediterraneanAncientCivilizations, SolarSystemAdventure

        self.chapter_levels = ChapterLevels()
        self.chapter_levels.onInitialize(chapter_name)

        chapter_levels_node = self.chapter_levels.getRoot()
        card_slot = self.content.getMovieSlot(SLOT_CHAPTER_LEVELS)
        card_slot.addChild(chapter_levels_node)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base+"_"+name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        with self._createTaskChain(SLOT_CHAPTER_LEVELS) as tc:
            for (level_name, card), race in tc.addRaceTaskList(self.chapter_levels.level_cards.items()):
                race.addTask("TaskMovie2SocketClick", Movie2=card.movie, Any=True)
                race.addScope(self._scopePlay, level_name)

    def _scopePlay(self, source, level_name):
        zoom_target = self.chapter_levels.level_cards[level_name].movie
        system_global = SystemManager.getSystem("SystemGlobal")
        system_global.setTransitionSceneParams(ZoomEffectTransitionObject=zoom_target)

        source.addFunction(GameManager.removeGame)
        source.addFunction(GameManager.prepareGame, level_name)
        source.addFunction(GameManager.runLevelStartAdvertisement)
