from Foundation.ArrowManager import ArrowManager
from Foundation.DatabaseManager import DatabaseManager
from Foundation.Entity.BaseScopeEntity import BaseScopeEntity
from Foundation.GroupManager import GroupManager
from Foundation.LayoutBox import LayoutBox
from Game.Managers.GameManager import GameManager
from Game.Entities.FinalStage.DropLevel.DropLevel import DropLevel
from Game.Entities.FinalStage.DropPanel.DropPanel import DropPanel
from Game.Entities.FinalStage.FinalStageDropItem.FinalStageDropItem import FinalStageDropItem
from Game.Entities.FinalStage.FinalStageAttachItem.FinalStageAttachItem import FinalStageAttachItem
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils
from UIKit.LayoutWrapper.LayoutBoxElementFuncWrapper import LayoutBoxElementFuncWrapper


MOVIE_CONTENT = "Movie2_Content"
MOVIE_PANEL = "Movie2_DropPanel"

SLOT_DROP_LEVEL = "drop_level"
SLOT_DROP_PANEL = "drop_panel"

QUEST_ITEM_NAME = "Item_{}"

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
        self.movie_items = []

    # - ScopeBaseEntity ------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        self.content = self.object.getObject(MOVIE_CONTENT)

        self._fillQuestItems()

        self._initDropPanel()
        self._initDropLevel()

        self._setupLayoutBox()

    def _onScopeActivate(self, source):
        super(FinalStage, self)._onScopeActivate(source)
        self._runTaskChains(source)

    def _onDeactivate(self):
        super(FinalStage, self)._onDeactivate()

        if self.layout_box:
            self.layout_box.finalize()
            self.layout_box = None

        if self.drop_panel:
            self.drop_panel.onFinalize()
            self.drop_panel = None

        if self.drop_level:
            self.drop_level.onFinalize()
            self.drop_level = None

        for item in self.items:
            item.onFinalize()
        self.items = []

        for item in self.attached_items:
            self._finalizeAttachedItem(item)
        self.attached_items = []

        for item in self.movie_items:
            item.onFinalize()
        self.movie_items = []

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
            banner_width = AdjustableScreenUtils.getBannerWidth()
            banner_height = AdjustableScreenUtils.getBannerHeight()
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

    def _runTaskChains(self, source):
        for item, parallel in source.addParallelTaskList(self.items):
            event_run = Event(item)

            with parallel.addRepeatTask() as (source_repeat, source_until):
                event_finish = Event(item)
                source_repeat.addScope(self._makeClickAction(item, event_finish))
                source_until.addEvent(event_finish)

        source.addScope(self._playFinalAnimation)

        backpack_scene_name = GameManager.getCurrentQuestBackpackSceneName()
        source.addNotify(Notificator.onChangeScene, backpack_scene_name)

    def _makeClickAction(self, drop_item, event_finish):
        def __clickAction(source):
            # click on DropItem socket
            source.addTask("TaskNodeSocketClick", Socket=drop_item.getSocket(), isDown=True)
            source.addPrint(" * FINAL STAGE CLICK ON '{}'".format(drop_item.sprite_object.getName()))

            # USELESS?
            item_index = self._findItem(drop_item)
            print "item_index", item_index
            if item_index is None:
                return

            # get item movie from final stage group
            movie_info = drop_item.getMovieInfo()
            group_item_movie = GroupManager.getObject(movie_info["group"], movie_info["name"])

            # generate ObjectSprite from clicked DropItem
            item_object_name = drop_item.getQuestItemName()
            item_object = GameManager.generateQuestItem(item_object_name)

            # init AttachItem with generated ObjectSprite
            attach_item = FinalStageAttachItem()
            attach_item.onInitialize(item_object)
            self.attached_items.append(attach_item)

            # attach AttachItem to cursor
            source.addFunction(self._attachToCursor, attach_item)

            # remove item from panel and start click / drop logic
            with source.addParallelTask(2) as (panel_anim, click):
                # remove item from panel and play panel rearrange animation
                panel_anim.addScope(self.drop_panel.playRemovePanelItemAnim, drop_item, item_index)

                def __clickRace(click_socket, mouse_up):
                    click_socket.addTask(
                        "TaskMovie2SocketClick",
                        SocketName="click",
                        Movie2=group_item_movie,
                        isDown=False,
                        isPressed=False,
                        UseArrowFilter=False
                    )
                    mouse_up.addTask("TaskMouseButtonClickEnd", isDown=False)

                with click.addRaceScope(2, __clickRace) as (click_socket, mouse_up):
                    mouse_up.addPrint("mouse_up")
                    mouse_up.addScope(self._playReturnItemToPanelAnimation,
                                      drop_item,
                                      item_index,
                                      attach_item)

                    click_socket.addScope(self._playCorrectDrop, group_item_movie, attach_item)
                    click_socket.addFunction(event_finish)

            source.addFunction(self._finalizeAttachedItem, attach_item)

        return __clickAction

    def _findItem(self, drop_item):
        index = None
        for i, item in enumerate(self.items):
            if item is drop_item:
                index = i
                break

        return index

    def _playFinalAnimation(self, source):
        MovieItem = GroupManager.getObject(self.scene_name, "Movie2_Final")
        source.addEnable(MovieItem)
        source.addTask("TaskMovie2Play", Movie2=MovieItem, Wait=True)

    def _playCorrectDrop(self, source, MovieItem, attach_item):
        with source.addParallelTask(2) as (play, remove):
            play.addTask("TaskMovie2Play", Movie2=MovieItem, Wait=True)
            play.addTask("TaskRemoveArrowAttach")

            remove.addScope(attach_item.setSpriteEnable, False)

    def _fillQuestItems(self):
        # get current chapter data
        chapter_id = self._getCurrentChapterId()
        self.scene_name = GameManager.getFinalStageSceneByChapter(chapter_id)

        player_data = GameManager.getPlayerGameData()
        chapter_data = player_data.getCurrentChapterData()
        current_quest_index = chapter_data.getCurrentQuestIndex()

        final_stage_params = self._getFinalStageMappingParams(self.scene_name)
        for i, param in enumerate(final_stage_params):
            if i >= current_quest_index:
                break

            item_object = self._getItemObject(param)

            movie_info = {
                "group": param.GroupName,
                "name": param.MovieName
            }

            item = FinalStageDropItem()
            item.onInitialize(self, item_object, movie_info)
            self.items.append(item)

    def _getItemObject(self, param):
        item_object = GameManager.generateQuestItem(param.ItemName)
        return item_object

    def _getFinalStageMappingParams(self, stage_name):
        s_db_module = "Database"
        s_db_name_final_stage_mapping = "FinalStageMapping"
        params = DatabaseManager.filterDatabaseORM(s_db_module,
                                                   s_db_name_final_stage_mapping,
                                                   filter=lambda param: param.StageName == stage_name)
        return params

    def _getCurrentChapterId(self):
        player_game_data = GameManager.getPlayerGameData()
        current_chapter_data = player_game_data.getCurrentChapterData()
        return current_chapter_data.getChapterId()

    def _attachToCursor(self, attach_item):
        attach_item_root = attach_item.getRoot()
        ArrowManager.attachArrow(attach_item_root)
        arrow_node = Mengine.getArrowNode()
        arrow_node.addChildFront(attach_item_root)

    def _moveLevelItemToPanelItem(self, source, drop_item, attach_item):
        # move attached item from cursor back to panel item using temporary moving node
        attach_root = attach_item.getRoot()

        # detach from arrow, but keep item visible while it flies back
        source.addTask("TaskRemoveArrowAttach")
        source.addScope(attach_item.setSpriteEnable, True)

        # create moving node that will carry attached item back to its (moving) panel item
        def _setup_moving_node():
            moving_node = Mengine.createNode("Interender")
            moving_node.setName("BezierFollow")

            attach_pos = attach_root.getWorldPosition()
            moving_node.setWorldPosition(attach_pos)

            # attach current attach_root under moving node
            moving_node.addChild(attach_root)
            self.addChild(moving_node)

            return moving_node

        moving_node = _setup_moving_node()

        source.addPrint(" * START BEZIER ITEM ANIM")

        # follow actual panel item root; if panel reflows items during animation,
        # the moving item will chase its new cell position. No extra scaling here –
        # panel sprite scale is handled independently when it is re-enabled.
        panel_item_root = drop_item.getRoot()
        source.addTask("TaskNodeBezier2ScreenFollow",
                       Node=moving_node,
                       Easing=SCENE_MOVE_EASING,
                       Follow=panel_item_root,
                       Time=SCENE_ANIMATION_TIME)

        source.addPrint(" * END BEZIER ITEM ANIM")

        # destroy only temporary helper node, attach_item will be finalized separately
        source.addTask("TaskNodeRemoveFromParent", Node=moving_node)
        source.addTask("TaskNodeDestroy", Node=moving_node)

        # hide attached item sprite so only panel item is visible
        source.addScope(attach_item.setSpriteEnable, False)

    def _playReturnItemToPanelAnimation(self, source, drop_item, item_index, attach_item):
        source.addFunction(self.drop_panel.returnDropItem, drop_item, item_index)

        with source.addParallelTask(2) as (moving_item, add_item):
            moving_item.addScope(self._moveLevelItemToPanelItem, drop_item, attach_item)
            add_item.addScope(self.drop_panel.playAddPanelItemAnim, drop_item)

        source.addScope(drop_item.setSpriteEnable, True)

    def _finalizeAttachedItem(self, item):
        if item in self.attached_items:
            self.attached_items.remove(item)
        item.onFinalize()
