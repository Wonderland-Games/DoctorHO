from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.SystemManager import SystemManager
from Foundation.DemonManager import DemonManager
from Foundation.SceneManager import SceneManager
from Game.Managers.GameManager import GameManager
from Game.Entities.Lobby.ChapterLevels import ChapterLevels


MOVIE_CONTENT = "Movie2_Content"
SLOT_CHAPTER_LEVELS = "ChapterLevels"

POPUP_ITEM_MOVE_EASING = "easyCubicIn"
POPUP_ITEM_MOVE_TIME = 500.0
POPUP_ITEM_SCALE_1_EASING = "easyLinear"
POPUP_ITEM_SCALE_1_TIME = 250.0
POPUP_ITEM_SCALE_1_TO = (1.25, 1.25, 1.0)
POPUP_ITEM_SCALE_2_EASING = "easyBackOut"
POPUP_ITEM_SCALE_2_TIME = 1000.0
POPUP_ITEM_SCALE_2_TO = (0.5, 0.5, 1.0)
POPUP_ITEM_ALPHA_EASING = "easyCubicIn"
POPUP_ITEM_ALPHA_TIME = 1000.0


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
        last_level_data = player_data.getLastLevelData()

        last_game_result = last_level_data.get("Result", None)
        if last_game_result in [False, None]:
            return

        level_name = last_level_data.get("LevelName", None)
        level_params = GameManager.getLevelParams(level_name)
        level_group_name = level_params.GroupName
        quest_item_name = level_params.QuestItem

        popup_object = DemonManager.getDemon("PopUp")
        popup = popup_object.entity

        source.addNotify(Notificator.onPopUpShow, "QuestItemReceived", popup.BUTTONS_STATE_DISABLE,
                         GroupName=level_group_name, ItemName=quest_item_name)

        source.addListener(Notificator.onPopUpQuestItemReceived)
        with source.addParallelTask(2) as (item, popup):
            item.addScope(self._moveItemToLevelCard)
            popup.addDelay(POPUP_ITEM_SCALE_1_TIME)
            popup.addNotify(Notificator.onPopUpHide)

    def _moveItemToLevelCard(self, source):
        # get level card wp
        # level_cards = [card for card in self.chapter_levels.level_cards.values()]
        level_cards = [card for card in self.chapter_levels.level_cards.values() if card.state == card.STATE_BLOCKED]
        if len(level_cards) == 0:
            return

        level_card = level_cards[0]
        level_card_node = level_card.getRoot()
        level_card_wp = level_card_node.getWorldPosition()

        # get current popup content (QuestItemReceived)
        popup_object = DemonManager.getDemon("PopUp")
        popup = popup_object.entity
        popup_content = popup.pop_up_content

        # get item sprite and item wp
        item = popup_content.item_sprite
        item_slot = item.getParent()
        item_wp = item_slot.getWorldPosition()

        # create moving node
        moving_node = Mengine.createNode("Interender")
        moving_node.setName("Temp")
        moving_node.addChild(item)

        # attach moving node to current scene main layer
        current_scene = SceneManager.getCurrentScene()
        current_scene_main_layer = current_scene.getMainLayer()
        scene_parent = current_scene_main_layer.getParent()
        scene_parent.addChild(moving_node)

        # set item wp for moving node
        moving_node.setWorldPosition(item_wp)

        # animation taskchain
        with source.addParallelTask(2) as (scale, popup):
            scale.addTask("TaskNodeScaleTo", Node=moving_node, Easing=POPUP_ITEM_SCALE_1_EASING, To=POPUP_ITEM_SCALE_1_TO,
                          Time=POPUP_ITEM_SCALE_1_TIME)
            popup.addListener(Notificator.onPopUpHideEnd)
        with source.addParallelTask(3) as (scale, move, alpha):
            scale.addTask("TaskNodeScaleTo", Node=moving_node, Easing=POPUP_ITEM_SCALE_2_EASING, To=POPUP_ITEM_SCALE_2_TO,
                          Time=POPUP_ITEM_SCALE_2_TIME)
            move.addTask("TaskNodeBezier2To", Node=moving_node, Easing=POPUP_ITEM_MOVE_EASING, From=item_wp, To=level_card_wp,
                         Time=POPUP_ITEM_MOVE_TIME)
            alpha.addTask("TaskNodeAlphaTo", Node=moving_node, Easing=POPUP_ITEM_ALPHA_EASING, To=0.0,
                          Time=POPUP_ITEM_ALPHA_TIME)

        source.addTask("TaskNodeRemoveFromParent", Node=item)
        source.addTask("TaskNodeDestroy", Node=item)
        source.addTask("TaskNodeRemoveFromParent", Node=moving_node)
        source.addTask("TaskNodeDestroy", Node=moving_node)

        source.addScope(level_card.scopeChangeLevelState, level_card.STATE_UNLOCKING)
