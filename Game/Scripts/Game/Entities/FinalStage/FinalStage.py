from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.GroupManager import GroupManager
from Game.Entities.FinalStage.DropLevel.DropLevel import DropLevel
from Game.Entities.FinalStage.DropPanel.DropPanel import DropPanel
from Game.Managers.GameManager import GameManager
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils


MOVIE_CONTENT = "Movie2_Content"
SLOT_DROP_LEVEL = "drop_level"
SLOT_DROP_PANEL = "drop_panel"
QUEST_ITEM_STORE_GROUP = "QuestItemStore"
QUEST_ITEM_NAME = "Item_{}_{}"
MOVIE_CLICK = "Movie2_Armor"


class FinalStage(BaseEntity):

    def __init__(self):
        super(FinalStage, self).__init__()
        self.content = None
        self.tcs = []
        self.miss_click = None
        self.drop_level = None
        self.drop_panel = None
        self.quest_items = []

    # - Object ----------------------------------------------------------------------------------------------------

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

    def _appendFoundItems(self, id, item):
        print("FOUND ITEMS".format(self.FoundItems))

    def _updateFoundItems(self, list):
        pass

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, obj):
        super(FinalStage, self)._onInitialize(obj)
        pass

    def _onFinalize(self):
        super(FinalStage, self)._onFinalize()
        pass

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        super(FinalStage, self)._onPreparation()
        pass

    def _onActivate(self):
        super(FinalStage, self)._onActivate()

        self.content = self.object.getObject(MOVIE_CONTENT)

        self._setupChapterQuestItems()

        self._initDropPanel()
        self._initDropLevel()

        self.drop_panel.onInitialize2()

        self._attachDropLevel()
        self._attachDropPanel()

        self._runTaskChains()

        '''
        self._handleCheats()
        '''

    def _onDeactivate(self):
        super(FinalStage, self)._onDeactivate()

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        if self.drop_panel is not None:
            self.drop_panel.onFinalize()
            self.drop_panel = None

        if self.drop_level is not None:
            self.drop_level.onFinalize()
            self.drop_level = None

        self.quest_items = []

    # - DropLevel ----------------------------------------------------------------------------------------------------

    def _initDropLevel(self):
        drop_panel_size = self.drop_panel.getSize()
        _, _, header_height, banner_height, viewport, _, _ = AdjustableScreenUtils.getMainSizesExt()

        frame_begin_x = viewport.begin.x
        frame_begin_y = viewport.begin.y + header_height
        frame_end_x = viewport.end.x
        frame_end_y = viewport.end.y - banner_height - drop_panel_size.y
        frame_points = Mengine.vec4f(frame_begin_x, frame_begin_y, frame_end_x, frame_end_y)

        self.drop_level = DropLevel()
        self.drop_level.onInitialize(self, frame_points)

    def _attachDropLevel(self):
        _, _, header_height, _, viewport, x_center, _ = AdjustableScreenUtils.getMainSizesExt()

        drop_level_size = self.drop_level.getSize()
        pos_y = viewport.begin.y + header_height + drop_level_size.y / 2

        drop_level_slot = self.content.getMovieSlot(SLOT_DROP_LEVEL)
        drop_level_slot.setWorldPosition(Mengine.vec2f(x_center, pos_y))
        self.drop_level.attachTo(drop_level_slot)

    # - DropPanel ----------------------------------------------------------------------------------------------------

    def _initDropPanel(self):
        self.drop_panel = DropPanel()
        self.drop_panel.onInitialize(self)

    def _attachDropPanel(self):
        _, game_height, _, banner_height, _, x_center, _ = AdjustableScreenUtils.getMainSizesExt()

        drop_panel_size = self.drop_panel.getSize()
        pos_y = game_height - banner_height - drop_panel_size.y / 2

        drop_panel_slot = self.content.getMovieSlot(SLOT_DROP_PANEL)
        drop_panel_slot.setWorldPosition(Mengine.vec2f(x_center, pos_y))
        self.drop_panel.attachTo(drop_panel_slot)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base+"_"+name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        #Notification.notify

        pass

    def _setupChapterQuestItems(self):
        # get current chapter data
        player_game_data = GameManager.getPlayerGameData()
        current_chapter_data = player_game_data.getCurrentChapterData()
        chapter_id = current_chapter_data.getChapterId()

        chapter_quests_params = GameManager.getQuestParamsByChapter(chapter_id)
        for i, quest_param in enumerate(chapter_quests_params):
            quest_param_item_name = quest_param.QuestItem.replace("Item_", "")
            quest_item_name = QUEST_ITEM_NAME.format(chapter_id, quest_param_item_name)

            quest_item_store_group = GroupManager.getGroup(QUEST_ITEM_STORE_GROUP)
            quest_item_object = quest_item_store_group.getObject(quest_item_name)

            self.quest_items.append(quest_item_object)

            print(quest_item_name)
