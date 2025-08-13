from Foundation.ArrowManager import ArrowManager
from Foundation.DatabaseManager import DatabaseManager
from Foundation.Entity.BaseScopeEntity import BaseScopeEntity
from Foundation.GroupManager import GroupManager
from Foundation.LayoutBox import LayoutBox
from Game.Entities.FinalStage.DropLevel.DropLevel import DropLevel
from Game.Entities.FinalStage.DropPanel.DropPanel import DropPanel
from Game.Entities.GameArea.SearchPanel.Item import Item
from Game.Managers.GameManager import GameManager
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils
from UIKit.LayoutWrapper.LayoutBoxElementFuncWrapper import LayoutBoxElementFuncWrapper


MOVIE_CONTENT = "Movie2_Content"
MOVIE_PANEL = "Movie2_DropPanel"

SLOT_DROP_LEVEL = "drop_level"
SLOT_DROP_PANEL = "drop_panel"

QUEST_ITEM_STORE_GROUP = "QuestItemStore"
QUEST_ITEM_NAME = "Item_{}_{}"

SCENE_NAME_TEMPLATE = "{:02d}_FinalStage"
SCENE_ANIMATION_TIME = 1000.0
SCENE_MOVE_EASING = "easyCubicIn"
SCENE_SCALE_EASING = "easyBackOut"


class FinalStage(BaseScopeEntity):
    def __init__(self):
        super(FinalStage, self).__init__()
        self.content = None
        self.drop_level = None
        self.drop_panel = None
        self.items = []
        self.scene_name = None
        self.layout_box = None
        self.attached_items = []

    # - ScopeBaseEntity -----------------------------------------------------------------------------------------------------

    def _onScopeActivate(self, source):
        super(FinalStage, self)._onScopeActivate(source)

        self.content = self.object.getObject(MOVIE_CONTENT)

        self._setupChapterQuestItems()

        self._initDropPanel()
        self._initDropLevel()

        self._setupLayoutBox()

        items_to_click = self.items
        for item, parallel in source.addParallelTaskList(items_to_click):
            event_run = Event(item)
            def makeClickAction(this_item, event_finish):
                def __clickAction(source):
                    source.addTask("TaskNodeSocketClick", Socket=this_item.getSocket(), isDown=True)
                    source.addPrint(" * FINAL STAGE CLICK ON '{}'".format(this_item.getObj().getName()))

                    item_index = self._findItem(this_item)
                    if item_index is None:
                        return

                    group = GroupManager.getGroup(self.scene_name)
                    movie_name = this_item.getMovieName()
                    MovieItem = group.getObject(movie_name)
                    source.addEnable(MovieItem)

                    attach_item = Item()
                    attach_item.onInitialize(self, this_item.getObj(), with_box=False)
                    self.attached_items.append(attach_item)

                    source.addFunction(self._attachToCursor, attach_item)

                    with source.addParallelTask(2) as (scale, click):
                        scale.addScope(self.drop_panel.playRemovePanelItemAnim, this_item, item_index)
                        scale.addTask("TaskNodeScaleTo",
                                      Node=attach_item.sprite,
                                      Easing=SCENE_SCALE_EASING,
                                      From=attach_item.getSpriteScale(),
                                      To=(1.0, 1.0, 1.0),
                                      Time=SCENE_ANIMATION_TIME)
                        #scale.addScope(self._scaleAttachItem, attach_item)

                        def __clickRace(click_socket, mouse_up):
                            click_socket.addTask(
                                "TaskMovie2SocketClick",
                                SocketName="click",
                                Movie2=MovieItem,
                                isDown=False,
                                isPressed=False,
                                UseArrowFilter=False
                            )
                            mouse_up.addTask("TaskMouseButtonClickEnd", isDown=False)

                        with click.addRaceScope(2, __clickRace) as (click_socket, mouse_up):
                            mouse_up.addScope(self._playReturnItemToPanelAnimation,
                                              this_item,
                                              item_index,
                                              attach_item)

                            click_socket.addScope(self._playCorrectDrop, MovieItem, attach_item)
                            click_socket.addFunction(event_finish)

                return __clickAction

            with parallel.addRepeatTask() as (source_repeat, source_until):
                event_finish = Event(item)
                source_repeat.addScope(makeClickAction(item, event_finish))
                source_until.addEvent(event_finish)

        source.addScope(self._playFinalAnimation)
        source.addNotify(Notificator.onChangeScene, "QuestBackpack")

    def _finalizeAndClear(self, attr_name):
        obj = getattr(self, attr_name)
        if obj is not None:
            finalize = getattr(obj, "onFinalize", getattr(obj, "finalize", None))
            if callable(finalize):
                finalize()
            setattr(self, attr_name, None)

    def _onDeactivate(self):
        super(FinalStage, self)._onDeactivate()

        self._finalizeAndClear("layout_box")
        self._finalizeAndClear("drop_panel")
        self._finalizeAndClear("drop_level")

        if self.items:
            for item in self.items:
                item.onFinalize()
            self.items = []

        if self.attached_items:
            for item in self.attached_items:
                self._finalizeAttachedItem(item)
            self.attached_items = []

        self.scene_name = None

    # - DropLevel ------------------------------------------------------------------------------------------------------

    def _initDropLevel(self):
        self.drop_level = DropLevel()
        self.drop_level.onInitialize(self.scene_name)

        drop_level_slot = self.content.getMovieSlot(SLOT_DROP_LEVEL)
        self.drop_level.attachTo(drop_level_slot)

    # - DropPanel ----------------------------------------------------------------------------------------------------

    def _initDropPanel(self):
        self.drop_panel = DropPanel()
        movie_panel = self.object.getObject(MOVIE_PANEL)
        self.drop_panel.onInitialize(movie_panel, self.items)

        drop_panel_slot = self.content.getMovieSlot(SLOT_DROP_PANEL)
        self.drop_panel.attachTo(drop_panel_slot)

    # - FinalStage -----------------------------------------------------------------------------------------------------

    def _setupLayoutBox(self):
        # HEADER
        def _getHeaderSize():
            header_size = AdjustableScreenUtils.getHeaderSize()
            return (header_size.x, header_size.y)

        # DROP LEVEL
        def _getDropLevelSize():
            drop_level_size = self.drop_level.getSize()
            return (drop_level_size.x, drop_level_size.y)

        def _setDropLevelPos(layout_box, layout_offset, layout_size):
            game_center = AdjustableScreenUtils.getGameCenter()
            drop_level_slot = self.content.getMovieSlot(SLOT_DROP_LEVEL)
            drop_level_slot.setWorldPosition((game_center.x, layout_offset[1] + layout_size[1]/2))

        # DROP PANEL
        def _getDropPanelSize():
            drop_panel_size = self.drop_panel.getSize()
            return (drop_panel_size.x, drop_panel_size.y)

        def _setDropPanelPos(layout_box, layout_offset, layout_size):
            game_center = AdjustableScreenUtils.getGameCenter()
            drop_panel_slot = self.content.getMovieSlot(SLOT_DROP_PANEL)
            drop_panel_slot.setWorldPosition((game_center.x, layout_offset[1] + layout_size[1]/2))

        # BANNER
        def _getBannerSize():
            banner_width = AdjustableScreenUtils.getActualBannerWidth()
            banner_height = AdjustableScreenUtils.getActualBannerHeight()
            return (banner_width, banner_height)

        # LAYOUT BOX
        def _getLayoutBoxSize():
            return AdjustableScreenUtils.getGameWidth(), AdjustableScreenUtils.getGameHeight()

        self.layout_box = LayoutBox(_getLayoutBoxSize)

        with LayoutBox.BuilderVertical(self.layout_box) as vertical:
            vertical.addFixedObject(LayoutBoxElementFuncWrapper(_getHeaderSize, None))
            vertical.addPadding(1)
            vertical.addFixedObject(LayoutBoxElementFuncWrapper(_getDropLevelSize, _setDropLevelPos))
            vertical.addPadding(1)
            vertical.addFixedObject(LayoutBoxElementFuncWrapper(_getDropPanelSize, _setDropPanelPos))
            vertical.addPadding(1)
            vertical.addFixedObject(LayoutBoxElementFuncWrapper(_getBannerSize, None))

    def _findItem(self, remove_item):
        return next((i for i, item in enumerate(self.items) if item is remove_item), None)

    def _playFinalAnimation(self, source):
        group = GroupManager.getGroup(self.scene_name)
        movie_name = "Movie2_Final"
        MovieItem = group.getObject(movie_name)
        source.addEnable(MovieItem)
        source.addTask("TaskMovie2Play", Movie2=MovieItem, Wait=True)

    def _playCorrectDrop(self, source, MovieItem, attach_item):
        with source.addParallelTask(2) as (play, remove):
            play.addTask("TaskMovie2Play", Movie2=MovieItem, Wait=True)
            play.addTask("TaskRemoveArrowAttach")

            remove.addFunction(self._finalizeAttachedItem, attach_item)

    def _setupChapterQuestItems(self):
        # get current chapter data
        chapter_id = self._getCurrentChapterId()
        self.scene_name = SCENE_NAME_TEMPLATE.format(chapter_id)

        player_data = GameManager.getPlayerGameData()
        chapter_data = player_data.getCurrentChapterData()
        current_quest_index = chapter_data.getCurrentQuestIndex()

        final_stage_params = self._getFinalStageMappingParams(self.scene_name)
        for i, param in enumerate(final_stage_params):
            if i >= current_quest_index:
                break

            item_object = self._getItemObject(param)

            movie_name = param.MovieName

            item = Item()
            item.onInitialize(self, item_object, movie_name)
            self.items.append(item)

    def _getItemObject(self, param):
        chapter_id = self._getCurrentChapterId()
        param_item_name = param.ItemName.replace("Item_", "")
        item_name = QUEST_ITEM_NAME.format(chapter_id, param_item_name)

        quest_item_store_group = GroupManager.getGroup(QUEST_ITEM_STORE_GROUP)
        return quest_item_store_group.getObject(item_name)

    def _getFinalStageMappingParams(self, group_name):
        s_db_module = "Database"
        s_db_name_final_stage_mapping = "FinalStageMapping"
        params = DatabaseManager.filterDatabaseORM(s_db_module, s_db_name_final_stage_mapping,
                                                   filter=lambda param: param.GroupName == group_name)
        return params

    def _getCurrentChapterId(self):
        player_game_data = GameManager.getPlayerGameData()
        current_chapter_data = player_game_data.getCurrentChapterData()
        return current_chapter_data.getChapterId()

    def _attachToCursor(self, attach_item):
        if ArrowManager.emptyArrowAttach() is False:
            attach = ArrowManager.getArrowAttach()
            attach.setParam("Enable", False)
            attachEntity = attach.getEntity()
            attachEntity.disable()

        attach_item_root = attach_item.getRoot()
        ArrowManager.attachArrow(attach_item_root)
        Mengine.getArrow().getNode().addChildFront(attach_item_root)

    def _scaleAttachItem(self, source, attach_item):
        source.addTask("TaskNodeScaleTo",
                      Node=attach_item.sprite,
                      Easing=SCENE_SCALE_EASING,
                      From=attach_item.getSpriteScale(),
                      To=(1.0, 1.0, 1.0),
                      Time=SCENE_ANIMATION_TIME)

    def _moveLevelItemToPanelItem(self, source, drop_item, attach_item):
        # generate level item pure sprite
        item_entity = attach_item.getObj().getEntity()
        item_pure = item_entity.generatePure()
        item_pure.enable()

        # create moving node
        item_moving_node = Mengine.createNode("Interender")
        item_moving_node.setName("BezierFollow")

        item_moving_node.setWorldPosition(attach_item.sprite_node.getWorldPosition())

        item_moving_node.addChild(item_pure)
        self.addChild(item_moving_node)

        drop_item_scale = drop_item.getDefaultSpriteScale()

        scale_from = attach_item.getSpriteScale()
        scale_to = (drop_item_scale, drop_item_scale, 1.0)

        panel_item_sprite = drop_item.getSprite()

        source.addTask("TaskRemoveArrowAttach")
        source.addFunction(self._finalizeAttachedItem, attach_item)

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

    def _playReturnItemToPanelAnimation(self, source, item, item_index, attach_item):
        source.addFunction(self.drop_panel.returnDropItem, item, item_index)

        with source.addParallelTask(2) as (moving_item, add_item):
            moving_item.addScope(self._moveLevelItemToPanelItem, item, attach_item)
            add_item.addScope(self.drop_panel.playAddPanelItemAnim, item)

        source.addScope(item.setItemVisible, True)

    def _finalizeAttachedItem(self, item):
        if item in self.attached_items:
            self.attached_items.remove(item)
        item.onFinalize()
