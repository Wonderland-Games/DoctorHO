from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.DemonManager import DemonManager
from Foundation.GroupManager import GroupManager
from UIKit.Managers.PrototypeManager import PrototypeManager
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils
from Game.Managers.GameManager import GameManager
from Game.Entities.QuestBackpack.ChapterQuestItems import ChapterQuestItems


MOVIE_CONTENT = "Movie2_Content"
SLOT_CHAPTER_QUEST_ITEMS = "ChapterQuestItems"
SLOT_LOBBY = "Lobby"
SLOT_FINAL_STAGE = "FinalStage"
PROTOTYPE_LOBBY = "Lobby"
PROTOTYPE_FINAL_STAGE = "Movie2Button_FinalStageButton"

CHAPTER_QUEST_ITEMS_SPACE_PERCENT = 0.7
LOBBY_SPACE_PERCENT = 0.3


class QuestBackpack(BaseEntity):
    def __init__(self):
        super(QuestBackpack, self).__init__()
        print "BACKPACK INIT !!!!!!!!!!!!!!!!!!!"
        self.content = None
        self.tcs = []
        self.chapter_quest_items = None
        self.lobby = None
        self.final_stage = None
        self.backpack_group = None

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        print "BACKPACK PREPARATION !!!!!!!!!!!!!!!!!!!!!!!!!"
        self.content = self.object.getObject(MOVIE_CONTENT)
        if self.content is None:
            return

        backpack_group_name = GameManager.getCurrentQuestBackpackGroupName()
        self.backpack_group = GroupManager.getGroup(backpack_group_name)

        #self.content.setActive(True)
        self._setupChapterQuestItems()
        self._setupLobby()
        self._setupFinalStage()
        print("_onPreparation")
        self._setupSlotsPositions()

    def _onActivate(self):
        self._runTaskChains()
        self._handleCheats()

    def _onDeactivate(self):
        self.content = None

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        if self.chapter_quest_items is not None:
            self.chapter_quest_items.onFinalize()
            self.chapter_quest_items = None

        if self.lobby is not None:
            self.lobby.onDestroy()
            self.lobby = None

        if self.final_stage is not None:
            self.final_stage.onDestroy()
            self.final_stage = None

        if self.backpack_group is not None:
            self.backpack_group = None

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupChapterQuestItems(self):
        # get current chapter data
        player_game_data = GameManager.getPlayerGameData()
        current_chapter_data = player_game_data.getCurrentChapterData()
        chapter_id = current_chapter_data.getChapterId()

        self.chapter_quest_items = ChapterQuestItems()
        self.chapter_quest_items.onInitialize(self, chapter_id)

        chapter_quest_items_node = self.chapter_quest_items.getRoot()
        chapter_quest_items_slot = self.content.getMovieSlot(SLOT_CHAPTER_QUEST_ITEMS)
        print("ChapterQuestItemsSlot")
        print(chapter_quest_items_slot)
        chapter_quest_items_slot.addChild(chapter_quest_items_node)

    def _setupLobby(self):
        self.lobby = PrototypeManager.generateObjectContainer(PROTOTYPE_LOBBY, PROTOTYPE_LOBBY)
        self.lobby.setEnable(True)

        lobby_node = self.lobby.getEntityNode()
        lobby_slot = self.content.getMovieSlot(SLOT_LOBBY)
        lobby_slot.addChild(lobby_node)

    def _setupFinalStage(self):
        print("_setupFinalStage")
        #chapter_finished = GameManager.isChapterCompleted()
        #if chapter_finished is False:
        #    return

        self.final_stage = self.backpack_group.generateObjectUnique(PROTOTYPE_FINAL_STAGE, PROTOTYPE_FINAL_STAGE)
        self.final_stage.setEnable(True)

        final_stage_node = self.final_stage.getEntityNode()
        final_stage_slot = self.content.getMovieSlot(SLOT_FINAL_STAGE)
        final_stage_slot.addChild(final_stage_node)


    def _setupSlotsPositions(self):
        print("setupSlotPosition")
        game_width, game_height, top_offset, banner_height, _, x_center, _ = AdjustableScreenUtils.getMainSizesExt()
        available_space_y = game_height - banner_height - top_offset

        chapter_quest_items_space_y = available_space_y * CHAPTER_QUEST_ITEMS_SPACE_PERCENT
        lobby_space_y = available_space_y * LOBBY_SPACE_PERCENT

        chapter_quest_items_pos_y = top_offset + chapter_quest_items_space_y / 2
        lobby_pos_y = top_offset + chapter_quest_items_space_y + lobby_space_y / 2

        chapter_quest_items_slot = self.content.getMovieSlot(SLOT_CHAPTER_QUEST_ITEMS)
        chapter_quest_items_slot.setWorldPosition(Mengine.vec2f(x_center, chapter_quest_items_pos_y))

        lobby_slot = self.content.getMovieSlot(SLOT_LOBBY)
        lobby_slot.setWorldPosition(Mengine.vec2f(x_center, lobby_pos_y))

        #chapter_finished = GameManager.isChapterCompleted()
        #if chapter_finished is True:
        final_stage_slot = self.content.getMovieSlot(SLOT_FINAL_STAGE)
        final_stage_slot.setWorldPosition(Mengine.vec2f(x_center, chapter_quest_items_pos_y))
        print("lobby y:{}".format(chapter_quest_items_pos_y))
        print("final stage y:{}".format(lobby_pos_y))

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base + "_" + name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        with self._createTaskChain(SLOT_LOBBY) as tc:
            tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.lobby.movie)
            tc.addNotify(Notificator.onChangeScene, "Lobby")

        chapter_finished = GameManager.isChapterCompleted()
        if chapter_finished is True:
            with self._createTaskChain(SLOT_FINAL_STAGE) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.final_stage)
                tc.addScope(self._setFinalStageScene)

        if len(self.chapter_quest_items.quest_items.items()) > 0:
            self._runChapterQuestItemsTaskChains()

    def _setFinalStageScene(self, source):
        final_stage_scene_name = GameManager.getCurrentFinalStageSceneName()
        source.addNotify(Notificator.onChangeScene, final_stage_scene_name)

    def _runChapterQuestItemsTaskChains(self):
        popup_object = DemonManager.getDemon("PopUp")
        popup = popup_object.entity
        player_game_data = GameManager.getPlayerGameData()
        current_chapter_data = player_game_data.getCurrentChapterData()
        chapter_id = current_chapter_data.getChapterId()
        chapter_finished = GameManager.isChapterCompleted()

        with self._createTaskChain(SLOT_CHAPTER_QUEST_ITEMS, Repeat=True) as tc:
            #tc.addFunction(self.final_stage.setBlock, not chapter_finished)

            for (quest_item_name, quest_item_entity), tc_race in tc.addRaceTaskList(self.chapter_quest_items.quest_items.items()):
                def _filter(item_name, lookup_item_name=quest_item_name):
                    """ copy-paste logic from Marjorie/GameArea/ImageCell click logic """
                    return lookup_item_name == item_name

                tc_race.addListener(Notificator.onQuestItemClicked, Filter=_filter)
                tc_race.addPrint("Quest item {!r} clicked".format(quest_item_name))
                tc_race.addNotify(Notificator.onPopUpShow, "QuestItemDescription", popup.BUTTONS_STATE_CLOSE, popup.PROTOTYPE_BG_BIG,
                                  ChapterId=chapter_id, ItemName=quest_item_name, ConvertToStoreItemName=False)

    def _handleCheats(self):
        if Mengine.hasOption("cheats") is False:
            return

        Trace.msg(" Game cheats ".center(50, "-"))
        Trace.msg(" C - clear items")
        Trace.msg(" G - get all items")
        Trace.msg("".center(50, "-"))

        with self._createTaskChain("CheatForFinalStage") as tc:
            with tc.addRaceTask(2) as (clear, get):
                clear.addTask("TaskKeyPress", Keys=[Mengine.KC_C])
                clear.addPrint("Clear items")
                clear.addFunction(GameManager.resetPlayerProgress)
                get.addTask("TaskKeyPress", Keys=[Mengine.KC_G])
                get.addPrint("Get all items")
                get.addFunction(GameManager.setMaxPlayerProgress)
