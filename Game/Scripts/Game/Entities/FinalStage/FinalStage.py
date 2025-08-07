from Foundation.ArrowManager import ArrowManager
from Foundation.DatabaseManager import DatabaseManager
from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.GroupManager import GroupManager
from Foundation.TaskManager import TaskManager
from Game.Entities.FinalStage.DropLevel.DropLevel import DropLevel
from Game.Entities.FinalStage.DropPanel.DropPanel import DropPanel
from Game.Entities.GameArea.SearchPanel.Item import Item
from Game.Entities.QuestBackpack.ChapterQuestItems import ChapterQuestItems
from Game.Managers.GameManager import GameManager
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils



MOVIE_CONTENT = "Movie2_Content"
MOVIE_PANEL = "Movie2_DropPanel"

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
        self.items = []
        self.attach_item = None
        self.scene_name = None
        self.on_socket_click = False

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

        if self.items is not None:
            for item in self.items:
                item.onFinalize()
        self.items = []

        if self.attach_item is not None:
            self.attach_item.onFinalize()
            self.attach_item = None

        self.quest_items = []
        self.scene_name = None

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
        self.drop_level.onInitialize(frame_points, self.scene_name)

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
        self.drop_panel.onInitialize(movie_panel, self.items)

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
        with self._createTaskChain("ItemsPick", Repeat=True) as tc:
            def __ItemsPickScope(source):
                items_to_click = self.items
                print(len(items_to_click))
                for item, parallel in tc.addRaceTaskList(items_to_click):
                    item_socket = item.getSocket()

                    group = GroupManager.getGroup(self.scene_name)
                    movie_name = item.getMovieName()
                    MovieItem = group.getObject(movie_name)

                    parallel.addEnable(MovieItem)

                    parallel.addTask("TaskNodeSocketClick", Socket=item_socket, isDown=True)
                    parallel.addPrint(" * FINAL STAGE CLICK ON '{}'".format(item.getObj().getName()))
                    parallel.addFunction(self.drop_panel.findRemovingItem, item)
                    parallel.addFunction(self._attachToCursor)

                    with parallel.addParallelTask(2) as (scale, click):
                        scale.addScope(self.drop_panel.playRemovePanelItemAnim)
                        scale.addScope(self._scaleAttachItem)

                        def __clickRace(click_socket, mouse_up):
                            click_socket.addTask("TaskMovie2SocketClick",
                                                 SocketName="click",
                                                 Movie2=MovieItem,
                                                 isDown=False,
                                                 isPressed=False,
                                                 UseArrowFilter=False)

                            mouse_up.addTask("TaskMouseButtonClickEnd", isDown=False)

                        with click.addRaceScope(2, __clickRace) as (click_socket, mouse_up):
                            mouse_up.addPrint("mouse_up")
                            #mouse_up.addScope(self._playReturnItemToPanelAnimation)

                            click_socket.addPrint("click_socket")
                            #click_socket.addScope(self._playCorrectDrop, MovieItem)
                    parallel.addScope(self._playReturnItemToPanelAnimation)

            tc.addScope(__ItemsPickScope)

        pass

    def _playCorrectDrop(self, source, MovieItem):
        source.addTask("TaskMovie2Play", Movie2=MovieItem, Wait=True)
        source.addTask("TaskRemoveArrowAttach")
        #source.addFunction(self.attach_item.playItemDestroyAnim)
        source.addFunction(self.drop_panel.clearDropItem)

    def _setupChapterQuestItems(self):
        # get current chapter data
        chapter_id = self._getCurrentChapterId()
        self.scene_name = "{:02d}_FinalStage".format(chapter_id)

        player_data = GameManager.getPlayerGameData()
        chapter_data = player_data.getCurrentChapterData()
        current_quest_index = chapter_data.getCurrentQuestIndex()

        final_stage_params = self.getFinalStageMappingParams(self.scene_name)
        for i, param in enumerate(final_stage_params):
            if i >= current_quest_index:
                break

            item_object = self.getItemObject(param)
            self.quest_items.append(item_object)

            movie_name = param.MovieName

            item = Item()
            item.onInitialize(self, item_object, movie_name)
            self.items.append(item)

    def getItemObject(self, param):
        chapter_id = self._getCurrentChapterId()
        param_item_name = param.ItemName.replace("Item_", "")
        item_name = QUEST_ITEM_NAME.format(chapter_id, param_item_name)

        quest_item_store_group = GroupManager.getGroup(QUEST_ITEM_STORE_GROUP)
        return quest_item_store_group.getObject(item_name)

    def getFinalStageMappingParams(self, group_name):
        s_db_module = "Database"
        s_db_name_final_stage_mapping = "FinalStageMapping"
        params = DatabaseManager.filterDatabaseORM(s_db_module, s_db_name_final_stage_mapping,
                                                   filter=lambda param: param.GroupName == group_name)
        return params

    def _getCurrentChapterId(self):
        player_game_data = GameManager.getPlayerGameData()
        current_chapter_data = player_game_data.getCurrentChapterData()
        return current_chapter_data.getChapterId()

    def _attachToCursor(self):
        arrow = Mengine.getArrow()
        arrow_node = arrow.getNode()
        drop_item =  self.drop_panel.getDropItem()
        self.attach_item = Item()
        self.attach_item.onInitialize(self, drop_item.item_obj, with_box=False)
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
