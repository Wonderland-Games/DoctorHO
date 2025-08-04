from Foundation.ArrowManager import ArrowManager
from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.GroupManager import GroupManager
from Game.Entities.FinalStage.DropLevel.DropLevel import DropLevel
from Game.Entities.FinalStage.DropPanel.DropPanel import DropPanel
from Game.Entities.GameArea.SearchPanel.Item import Item
from Game.Managers.GameManager import GameManager
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils


MOVIE_CONTENT = "Movie2_Content"
MOVIE_PANEL = "Movie2_DropPanel"
MOVIE_ARMOR_CLICK = "Movie2_Armor"
MOVIE_HELMET_CLICK = "Movie2_Helmet"

SLOT_DROP_LEVEL = "drop_level"
SLOT_DROP_PANEL = "drop_panel"

QUEST_ITEM_STORE_GROUP = "QuestItemStore"
QUEST_ITEM_NAME = "Item_{}_{}"

SCENE_ANIMATION_TIME = 1000.0
SCENE_MOVE_EASING = "easyCubicIn"
SCENE_SCALE_EASING = "easyBackOut"


class FinalStage(BaseEntity):

    def __init__(self):
        super(FinalStage, self).__init__()
        self.content = None
        self.tcs = []
        self.miss_click = None
        self.drop_level = None
        self.drop_panel = None
        self.quest_items = []
        self.attach_item = None
        self.movie_items = []
        self.group_name = None

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
        print("{} is enable {}".format(self.group_name, GroupManager.isEnableGroup(self.group_name)))

        self._initDropPanel()
        self._initDropLevel()

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
        if self.attach_item is not None:
            self.attach_item.onFinalize()
            self.attach_item = None

        self.movie_items = []
        self.group_name = None

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
        self.drop_level.onInitialize(frame_points, self.group_name)

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
        movie_panel = self.object.getObject(MOVIE_PANEL)
        self.drop_panel.onInitialize(movie_panel, self.quest_items)

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
        items_to_click = list(self.drop_panel.items)

        with self._createTaskChain("ItemsPick", Repeat=True) as tc:
            for item, parallel in tc.addRaceTaskList(items_to_click):
                item_obj = item.item_obj
                item_socket = item.getSocket()
                parallel.addTask("TaskNodeSocketClick", Socket=item_socket, isDown=True)
                parallel.addPrint(" * FINAL STAGE CLICK ON '{}'".format(item_obj.getName()))
                parallel.addFunction(self.quest_items.remove, item_obj)
                parallel.addFunction(self.drop_panel.findRemovingItem, item_obj)
                parallel.addFunction(self._attachToCursor)

                with parallel.addParallelTask(2) as (scale, click):
                    scale.addScope(self.drop_panel.playRemovePanelItemAnim)
                    scale.addScope(self._scaleAttachItem)
                    click.addTask("TaskMouseButtonClick", isDown=False)

                parallel.addScope(self._playReturnItemToPanelAnimation)

        with self._createTaskChain("FinalStageClick", Repeat=True) as tc:
            group = GroupManager.getGroup(self.group_name)
            items_to_drop = list(self.movie_items)
            for item, parallel in tc.addRaceTaskList(items_to_drop):
                MovieItem = group.getObject(item)

                parallel.addEnable(MovieItem)
                parallel.addTask("TaskMovie2SocketClick", SocketName="click", Movie2=MovieItem, isDown=False, isPressed=False, UseArrowFilter=False)
                parallel.addTask("TaskMovie2Play", Movie2=MovieItem, Wait=True)
            '''
            MovieHelmet = group.getObject(MOVIE_HELMET_CLICK)

            tc.addEnable(MovieArmor)
            tc.addTask("TaskMovie2SocketClick", SocketName="click", Movie2=MovieHelmet, isDown=False)
            tc.addTask("TaskMovie2Play", Movie2=MovieHelmet, Wait=True)
            '''

        pass

    def _setupChapterQuestItems(self):
        # get current chapter data
        player_game_data = GameManager.getPlayerGameData()
        current_chapter_data = player_game_data.getCurrentChapterData()
        chapter_id = current_chapter_data.getChapterId()
        self.group_name = "{:02d}_FinalStage".format(chapter_id)

        print(chapter_id)
        items_name = []
        chapter_quests_params = GameManager.getQuestParamsByChapter(chapter_id)
        for i, quest_param in enumerate(chapter_quests_params):
            items_name.append(quest_param.QuestItem)
            quest_param_item_name = quest_param.QuestItem.replace("Item_", "")
            quest_item_name = QUEST_ITEM_NAME.format(chapter_id, quest_param_item_name)

            quest_item_store_group = GroupManager.getGroup(QUEST_ITEM_STORE_GROUP)
            quest_item_object = quest_item_store_group.getObject(quest_item_name)

            self.quest_items.append(quest_item_object)

            print(quest_item_name)

        self._setupMovieItems(items_name)


    def _setupMovieItems(self, items):
        self.movie_items = ["Movie2_" + item.split("Quest_")[-1] for item in items]
        print(self.movie_items)

    def _attachToCursor(self):
        arrow = Mengine.getArrow()
        arrow_node = arrow.getNode()
        drop_item =  self.drop_panel.getDropItem()
        self.attach_item = Item()
        self.attach_item.onInitialize(self, drop_item.item_obj, False)
        attach_item_root = self.attach_item.getRoot()

        ArrowManager.attachArrow(attach_item_root)
        arrow_node.addChildFront(attach_item_root)

    def _scaleAttachItem(self, source):
        item_node = self.attach_item.sprite
        scale_from = self.attach_item.getSpriteScale()
        scale_to = (1.0, 1.0, 1.0)

        source.addTask("TaskNodeScaleTo",
                      Node=item_node,
                      Easing=SCENE_SCALE_EASING,
                      From=scale_from,
                      To=scale_to,
                      Time=SCENE_ANIMATION_TIME)

    def _moveLevelItemToPanelItem(self, source):
        source.addTask("TaskRemoveArrowAttach")
        # generate level item pure sprite

        item_entity = self.attach_item.getObj().getEntity()
        item_pure = item_entity.generatePure()
        item_pure.enable()

        # create moving node
        item_moving_node = Mengine.createNode("Interender")
        item_moving_node.setName("BezierFollow")

        item_moving_node.setWorldPosition(self.attach_item.sprite_node.getWorldPosition())

        item_moving_node.addChild(item_pure)
        self.addChild(item_moving_node)

        drop_item = self.drop_panel.getDropItem()
        drop_item_scale = drop_item.getDefaultSpriteScale()

        scale_from = self.attach_item.getSpriteScale()
        scale_to = (drop_item_scale, drop_item_scale, 1.0)

        panel_item_sprite = drop_item.getSprite()

        source.addFunction(self.attach_item.onFinalize)

        source.addPrint(" * START BEZIER ITEM ANIM")

        with source.addParallelTask(2) as (scale, move):
            scale.addTask("TaskNodeScaleTo",
                          Node=item_moving_node,
                          Easing=SCENE_SCALE_EASING,
                          From=scale_from,
                          To=scale_to,
                          Time=SCENE_ANIMATION_TIME)

            move.addTask("TaskNodeBezier2ScreenFollow",
                           Node=item_moving_node,
                           Easing=SCENE_MOVE_EASING,
                           Follow=panel_item_sprite,
                           Time=SCENE_ANIMATION_TIME)

        source.addPrint(" * END BEZIER ITEM ANIM")

        source.addTask("TaskNodeRemoveFromParent", Node=item_pure)
        source.addTask("TaskNodeDestroy", Node=item_pure)
        source.addTask("TaskNodeRemoveFromParent", Node=item_moving_node)
        source.addTask("TaskNodeDestroy", Node=item_moving_node)

    def _playReturnItemToPanelAnimation(self, source):
        source.addFunction(self.drop_panel.returnDropItem)

        with source.addParallelTask(2) as (moving_item, add_item):
            moving_item.addScope(self._moveLevelItemToPanelItem)
            add_item.addScope(self.drop_panel.playAddPanelItemAnim)

        drop_item = self.drop_panel.getDropItem()
        source.addFunction(self.quest_items.append, drop_item.getObj())
        source.addScope(drop_item.setItemVisible, True)
        source.addFunction(self.drop_panel.clearDropItem)
