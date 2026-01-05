from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.SystemManager import SystemManager
from Foundation.DemonManager import DemonManager
from Foundation.SceneManager import SceneManager
from Game.Managers.GameManager import GameManager
from Game.Entities.Lobby.ChapterLevels import ChapterLevels
from UIKit.Managers.PrototypeManager import PrototypeManager
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils


MOVIE_CONTENT = "Movie2_Content"
SLOT_CHAPTER_LEVELS = "ChapterLevels"

PROTOTYPE_QUEST_BACKPACK = "QuestBackpack"
SLOT_QUEST_BACKPACK = "QuestBackpack"

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

CHAPTER_LEVELS_SPACE_PERCENT = 0.7
QUEST_BACKPACK_SPACE_PERCENT = 0.3


class Lobby(BaseEntity):
    def __init__(self):
        super(Lobby, self).__init__()
        self.content = None
        self.tcs = []
        self.chapter_levels = None
        self.quest_backpack = None

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        self.content = self.object.getObject(MOVIE_CONTENT)
        if self.content is None:
            return

        self._setupChapterLevels()
        self._setupQuestBackpack()
        self._setupSlotsPositions()

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

        if self.quest_backpack is not None:
            self.quest_backpack.onDestroy()
            self.quest_backpack = None

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupChapterLevels(self):
        # get current chapter data
        player_game_data = GameManager.getPlayerGameData()
        current_chapter_data = player_game_data.getCurrentChapterData()
        chapter_id = current_chapter_data.getChapterId()

        self.chapter_levels = ChapterLevels()
        self.chapter_levels.onInitialize(chapter_id)

        chapter_levels_node = self.chapter_levels.getRoot()
        chapter_levels_slot = self.content.getMovieSlot(SLOT_CHAPTER_LEVELS)
        chapter_levels_slot.addChild(chapter_levels_node)

    def _setupQuestBackpack(self):
        self.quest_backpack = PrototypeManager.generateObjectContainer(PROTOTYPE_QUEST_BACKPACK, PROTOTYPE_QUEST_BACKPACK)
        self.quest_backpack.setEnable(True)

        quest_backpack_node = self.quest_backpack.getEntityNode()
        quest_backpack_slot = self.content.getMovieSlot(SLOT_QUEST_BACKPACK)
        quest_backpack_slot.addChild(quest_backpack_node)

    def _setupSlotsPositions(self):
        _, game_height, top_offset, banner_height, _, x_center, _ = AdjustableScreenUtils.getMainSizesExt()
        available_space_y = game_height - banner_height - top_offset

        chapter_levels_space_y = available_space_y * CHAPTER_LEVELS_SPACE_PERCENT
        quest_backpack_space_y = available_space_y * QUEST_BACKPACK_SPACE_PERCENT

        chapter_levels_pos_y = top_offset + chapter_levels_space_y / 2
        quest_backpack_pos_y = top_offset + chapter_levels_space_y + quest_backpack_space_y / 2

        chapter_levels_slot = self.content.getMovieSlot(SLOT_CHAPTER_LEVELS)
        chapter_levels_slot.setWorldPosition(Mengine.vec2f(x_center, chapter_levels_pos_y))

        quest_backpack_slot = self.content.getMovieSlot(SLOT_QUEST_BACKPACK)
        quest_backpack_slot.setWorldPosition(Mengine.vec2f(x_center, quest_backpack_pos_y))

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base+"_"+name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        with self._createTaskChain(SLOT_CHAPTER_LEVELS) as tc:
            for card, race in tc.addRaceTaskList(self.chapter_levels.level_cards.values()):
                race.addTask("TaskMovie2SocketClick", Movie2=card.movie, SocketName="socket", Filter=card.isActive)
                race.addScope(self._scopePlay, card.level_id)

        with self._createTaskChain("LevelEnd") as tc:
            tc.addScope(self._scopeLevelEnd)

        with self._createTaskChain(SLOT_QUEST_BACKPACK) as tc:
            tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.quest_backpack.movie)

            backpack_scene_name = GameManager.getCurrentQuestBackpackSceneName()
            tc.addNotify(Notificator.onChangeScene, backpack_scene_name)

    def _scopePlay(self, source, level_id):
        # player_data = GameManager.getPlayerGameData()
        # current_chapter_data = player_data.getCurrentChapterData()
        # quest_index = current_chapter_data.getCurrentQuestIndex()

        level_params = GameManager.getLevelParams(level_id)
        level_scene_name = level_params.SceneName

        source.addScope(self._scopeSetTransitionParams, level_id)
        source.addFunction(GameManager.removeGame)
        source.addFunction(GameManager.prepareGame, level_id)
        source.addFunction(GameManager.runLevelStartAdvertisement, level_scene_name)

    def _scopeSetTransitionParams(self, source, level_id):
        zoom_target = self.chapter_levels.level_cards[level_id].movie
        system_global = SystemManager.getSystem("SystemGlobal")
        system_global.setTransitionSceneParams(ZoomEffectTransitionObject=zoom_target)

    def _scopeLevelEnd(self, source):
        player_data = GameManager.getPlayerGameData()
        last_level_data = player_data.getLastLevelData()

        last_game_result = last_level_data.get("Result", None)
        if last_game_result in [False, None]:
            return

        chapter_id = last_level_data.get("ChapterId", None)

        quest_index = last_level_data.get("QuestIndex", None)
        if quest_index is not None:
            quest_params = GameManager.getQuestParamsWithChapterIdAndQuestIndex(chapter_id, quest_index)
            quest_item_name = quest_params.QuestItem

        popup_object = DemonManager.getDemon("PopUp")
        popup = popup_object.entity

        blocked_level_cards = [card for card in self.chapter_levels.level_cards.values() if card.state == card.STATE_BLOCKED]

        def _calcLevelRewardQuestPoints(_level_id):
            return 50

        if quest_index is not None:
            source.addNotify(Notificator.onPopUpShow, "QuestItemReceived", popup.BUTTONS_STATE_DISABLE, ChapterId=chapter_id, ItemName=quest_item_name)

            source.addListener(Notificator.onPopUpQuestItemReceived)
            with source.addParallelTask(2) as (item, popup):
                # item.addScope(self._moveItemToLevelCard)
                # popup.addDelay(POPUP_ITEM_SCALE_1_TIME)
                item.addScope(self._moveItemToQuestBackpack)
                popup.addNotify(Notificator.onPopUpHide)

            source.addListener(Notificator.onPopUpHideEnd)

        for level_card, tc in source.addParallelTaskList(blocked_level_cards):
            source.addScope(level_card.scopeProgressOnQuestBar, _calcLevelRewardQuestPoints(level_card.level_id))

    def _moveItemToLevelCard(self, source):
        # get level card wp
        # level_cards = [card for card in self.chapter_levels.level_cards.values()]
        level_cards = [card for card in self.chapter_levels.level_cards.values() if card.state == card.STATE_BLOCKED]
        if len(level_cards) == 0:
            return

        level_card = level_cards[0]
        level_card_node = level_card.getRoot()
        level_card_wp = level_card_node.getWorldPosition()

        source.addScope(self._moveItemToWP, level_card_wp)
        source.addScope(level_card.scopeChangeLevelState, level_card.STATE_UNLOCKING)

    def _moveItemToQuestBackpack(self, source):
        # get quest backpack wp
        quest_backpack_node = self.quest_backpack.getEntityNode()
        quest_backpack_wp = quest_backpack_node.getWorldPosition()

        source.addScope(self._moveItemToWP, quest_backpack_wp)

    def _moveItemToWP(self, source, destination_wp):
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
            move.addTask("TaskNodeBezier2To", Node=moving_node, Easing=POPUP_ITEM_MOVE_EASING, From=item_wp, To=destination_wp,
                         Time=POPUP_ITEM_MOVE_TIME)
            alpha.addTask("TaskNodeAlphaTo", Node=moving_node, Easing=POPUP_ITEM_ALPHA_EASING, To=0.0,
                          Time=POPUP_ITEM_ALPHA_TIME)

        source.addTask("TaskNodeRemoveFromParent", Node=item)
        source.addFunction(popup_content.item_object.onDestroy)
        source.addTask("TaskNodeRemoveFromParent", Node=moving_node)
        source.addTask("TaskNodeDestroy", Node=moving_node)
