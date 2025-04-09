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

        with self._createTaskChain("QuestItemReceived") as tc:
            tc.addScope(self._scopeQuestItemReceived)

    def _scopePlay(self, source, level_name):
        zoom_target = self.chapter_levels.level_cards[level_name].movie
        system_global = SystemManager.getSystem("SystemGlobal")
        system_global.setTransitionSceneParams(ZoomEffectTransitionObject=zoom_target)

        source.addFunction(GameManager.removeGame)
        source.addFunction(GameManager.prepareGame, level_name)
        source.addFunction(GameManager.runLevelStartAdvertisement)

    def _scopeLevelCardsStateTest(self, source):
        source.addTask("TaskKeyPress", Keys=[Keys.getVirtualKeyCode("VK_Q")])

        for card, parallel in source.addParallelTaskList(self.chapter_levels.level_cards.values()):
            parallel.addScope(card.scopeChangeLevelState, card.STATE_UNLOCKING)

    def _scopeQuestItemReceived(self, source):
        player_data = GameManager.getPlayerGameData()
        last_game_result = player_data.getLastResult()
        if last_game_result in [False, None]:
            return

        popup_object = DemonManager.getDemon("PopUp")
        popup = popup_object.entity

        level_name = "01_AncientEgypt"
        level_params = GameManager.getLevelParams(level_name)
        level_group_name = level_params.GroupName
        item_name = "Item_Armor"

        source.addNotify(Notificator.onPopUpShow, "QuestItemReceived", popup.BUTTONS_STATE_DISABLE,
                         GroupName=level_group_name, ItemName=item_name)

        source.addListener(Notificator.onPopUpHide)
        source.addScope(self._moveItemToLevelCard)

    def _moveItemToLevelCard(self, source):
        popup_object = DemonManager.getDemon("PopUp")
        popup = popup_object.entity
        print popup
        popup_content = popup.pop_up_content
        print popup_content
        item = popup_content.item_sprite
        item_wp = item.getParent().getWorldPosition()

        # create moving node
        moving_node = Mengine.createNode("Interender")
        moving_node.setName("Temp")

        moving_node.addChild(item)
        self.addChild(moving_node)
        moving_node.setWorldPosition(item_wp)

        # blocked_level_cards = [card for card in self.chapter_levels.level_cards.values() if card.getState() == card.STATE_BLOCKED]
        blocked_level_cards = [card for card in self.chapter_levels.level_cards.values()]
        # if len(blocked_level_cards) == 0:
        #     return

        level_card = blocked_level_cards[0]
        level_card_node = level_card.getRoot()
        level_card_wp = level_card_node.getWorldPosition()
        print level_card_wp

        with source.addParallelTask(2) as (scale, move):
            # scale.addTask("TaskNodeScaleTo", Node=moving_node, Easing=SCENE_ITEM_SCALE_EASING, To=panel_item_scale,
            #               Time=SCENE_ITEM_SCALE_TIME)
            # move.addTask("TaskNodeBezier2ScreenFollow", Node=moving_node, Easing=SCENE_ITEM_MOVE_EASING, Follow=level_card_node,
            #              Time=SCENE_ITEM_MOVE_TIME)
            move.addTask("TaskNodeMoveTo", Node=moving_node, To=level_card_wp, Time=1000.0)
            move.addPrint("{}".format(level_card_node.getWorldPosition()))

        # source.addTask("TaskNodeRemoveFromParent", Node=item)
        # source.addTask("TaskNodeDestroy", Node=item)
        # source.addTask("TaskNodeRemoveFromParent", Node=moving_node)
        # source.addTask("TaskNodeDestroy", Node=moving_node)
