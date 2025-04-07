from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.SystemManager import SystemManager
from Foundation.DemonManager import DemonManager
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
        # chapter_name = "MediterraneanAncientCivilizations"  # MediterraneanAncientCivilizations, SolarSystemAdventure
        player_game_data = GameManager.getPlayerGameData()
        current_chapter_data = player_game_data.getCurrentChapterData()
        chapter_name = current_chapter_data.getChapterName()

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
                # with race.addIfTask(lambda: card.state == card.STATE_ACTIVE) as (active, _):
                #     active.addTask("TaskMovie2SocketClick", Movie2=card.movie, Any=True)
                #     active.addScope(self._scopePlay, level_name)
                race.addTask("TaskMovie2SocketClick", Movie2=card.movie, Any=True)
                race.addScope(self._scopePlay, level_name)

        with self._createTaskChain("CardsStatesTester", Repeat=True) as tc:
            tc.addScope(self._scopeLevelCardsStateTest)

    def _scopePlay(self, source, level_name):
        zoom_target = self.chapter_levels.level_cards[level_name].movie
        system_global = SystemManager.getSystem("SystemGlobal")
        system_global.setTransitionSceneParams(ZoomEffectTransitionObject=zoom_target)

        source.addFunction(GameManager.removeGame)
        source.addFunction(GameManager.prepareGame, level_name)
        source.addFunction(GameManager.runLevelStartAdvertisement)

    def _scopeLevelCardsStateTest(self, source):
        popup_object = DemonManager.getDemon("PopUp")
        popup = popup_object.entity

        source.addTask("TaskKeyPress", Keys=[Keys.getVirtualKeyCode("VK_Q")])
        source.addNotify(Notificator.onPopUpShow, "QuestItemReceived", popup.BUTTONS_STATE_DISABLE, LevelName="01_AncientEgypt", ItemName="Item_Armor")
        # for card, parallel in source.addParallelTaskList(self.chapter_levels.level_cards.values()):
        #     parallel.addScope(card.scopeChangeLevelState, card.STATE_UNLOCKING)
