from Foundation.ArrowManager import ArrowManager
from Foundation.Initializer import Initializer
from Foundation.Entities.MovieVirtualArea.VirtualArea import VirtualArea
from Game.Entities.GameArea.SearchPanel.Item import Item
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils


MOVIE_PANEL = "Movie2_DropPanel"

ITEMS_OFFSET_BETWEEN = 25.0
ITEMS_NODE_MOVE_TIME = 300.0
ITEMS_MOVE_TIME = 300.0
ITEMS_MOVE_EASING = "easyCubicInOut"
SCENE_ITEM_MOVE_EASING = "easyCubicIn"
SCENE_ITEM_MOVE_TIME = 1000.0
SCENE_ITEM_SCALE_EASING = "easyBackOut"
SCENE_ITEM_SCALE_TIME = 1000.0


class DropPanel(Initializer):
    def __init__(self):
        super(DropPanel, self).__init__()
        self.final_stage = None
        self.virtual_area = None
        self.va_hotspot = None
        self.root = None
        self.movie_panel = None
        self.quest_items = []
        self.items = []
        self.items_node = None
        self.va_range_points = None
        self.semaphore_allow_panel_items_move = None
        self.drop_item = None
        self.drop_item_num = None
        self.attach_item = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, final_stage, movie_panel, quest_items):
        super(DropPanel, self)._onInitialize()
        self.final_stage = final_stage

        self.movie_panel = movie_panel
        self.quest_items = quest_items

        self._initVirtualArea()

        self._createRoot()
        self._attachPanel()

        self._initItems()

        self._setupVirtualArea()
        self._calcVirtualAreaContentSize()

        self.virtual_area.set_percentage(0.5, 0.0)  # on start always set VA to the middle of content
        self.semaphore_allow_panel_items_move = Semaphore(True, "AllowPanelItemsMove")

        return True

    def _onFinalize(self):
        super(DropPanel, self)._onFinalize()

        for item in self.items:
            item.onFinalize()
        self.items = []

        if self.items_node is not None:
            Mengine.destroyNode(self.items_node)
            self.items_node = None

        if self.root is not None:
            Mengine.destroyNode(self.root)
            self.root = None

        if self.virtual_area is not None:
            self.virtual_area.onFinalize()
            self.virtual_area = None

        if self.va_hotspot is not None:
            self.va_hotspot.removeFromParent()
            Mengine.destroyNode(self.va_hotspot)
            self.va_hotspot = None

        self.movie_panel = None
        self.quest_items = []
        self.va_range_points = None
        self.semaphore_allow_panel_items_move = None
        self.drop_item = None
        self.drop_item_num = None
        self.attach_item = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__)

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    def getRoot(self):
        return self.root

    # - VirtualArea ----------------------------------------------------------------------------------------------------

    def _initVirtualArea(self):
        self.virtual_area = VirtualArea()
        self.virtual_area.onInitialize(
            name="DropPanelVirtualArea",
            dragging_mode="horizontal",
            enable_scale=False,
            disable_drag_if_invalid=False,
            camera_name="DropPanelVirtualCamera",
            viewport_name="DropPanelViewport",
        )

    def _setupVirtualArea(self):
        self.va_hotspot = Mengine.createNode("HotSpotPolygon")
        self.va_hotspot.setName(self.__class__.__name__ + "_" + "VirtualAreaSocket")

        item = self.items[0]
        item_size = item.getSize()
        panel_size = self.getSize()

        va_begin_x = 0
        va_begin_y = 0
        va_end_x = panel_size.x
        va_end_y = item_size.y

        hotspot_polygon = [
            (va_begin_x, va_begin_y),
            (va_end_x, va_begin_y),
            (va_end_x, va_end_y),
            (va_begin_x, va_end_y)
        ]
        hotspot_polygon_center = Mengine.vec2f(
            panel_size.x / -2,
            panel_size.y / 2 - item_size.y
        )

        self.va_hotspot.setPolygon(hotspot_polygon)
        self.va_hotspot.setDefaultHandle(False)

        self.root.addChild(self.va_hotspot)
        self.va_hotspot.enable()
        self.va_hotspot.setLocalPosition(hotspot_polygon_center)

        self.virtual_area.setup_viewport(va_begin_x, va_begin_y, va_end_x, va_end_y)
        self.virtual_area.init_handlers(self.va_hotspot)

        # attach VA to root
        virtual_area_node = self.virtual_area.get_node()
        self.root.addChild(virtual_area_node)
        virtual_area_node.setLocalPosition(hotspot_polygon_center)

    def _calcVirtualAreaContentSize(self):
        if not self.items:
            return

        content_size_x = sum(item.getSize().x for item in self.items) + (len(self.items) - 1) * ITEMS_OFFSET_BETWEEN
        panel_size = self.getSize()

        center_panel_pos = Mengine.vec2f(panel_size.x / 2, self.items[0].getSize().y / 2)

        if content_size_x <= panel_size.x:
            self.virtual_area.set_content_size(0, 0, panel_size.x, panel_size.y)
            self.items_node.setLocalPosition(center_panel_pos)
        else:
            self.virtual_area.set_content_size(0, 0, content_size_x, panel_size.y)

    # - Panel ----------------------------------------------------------------------------------------------------------

    def _attachPanel(self):
        self.movie_panel.setInteractive(True)
        movie_panel_node = self.movie_panel.getEntityNode()
        self.root.addChild(movie_panel_node)


    def getBounds(self):
        panel_bounds = self.movie_panel.getCompositionBounds()
        return panel_bounds

    def getSize(self):
        game_width, _, _, _ = AdjustableScreenUtils.getMainSizes()
        panel_bounds = self.getBounds()
        panel_size = Utils.getBoundingBoxSize(panel_bounds)

        # panel_width = game_width
        panel_width = panel_size.x

        return Mengine.vec2f(panel_width, panel_size.y)

    # - Items ----------------------------------------------------------------------------------------------------------

    def _initItems(self):
        # create items node
        self.items_node = Mengine.createNode("Interender")
        self.items_node.setName("Items")
        self.virtual_area.add_node(self.items_node)

        # init items
        for i, item_obj in enumerate(self.quest_items):
            item = Item()
            item.onInitialize(self, item_obj)
            item.attachTo(self.items_node)
            self.items.append(item)

        items_node_pos = self._calcItemsNodeLocalPosition()
        self.items_node.setLocalPosition(items_node_pos)

        # set items local position
        for i, item in enumerate(self.items):
            item_pos = self._calcItemLocalPosition(i)
            item.setLocalPositionX(item_pos.x)

    def findRemovingItem(self, item_obj):
        for i, item in enumerate(self.items):
            if item.item_obj is item_obj:
                self.drop_item = item
                self.drop_item_num = i
                break

    def _calcItemsNodeLocalPosition(self):
        content_width = sum(item.getSize().x for item in self.items) + (len(self.items) - 1) * ITEMS_OFFSET_BETWEEN
        content_height = self.items[0].getSize().y

        return Mengine.vec2f(content_width / 2, content_height / 2)


    def _calcItemLocalPosition(self, i):
        items_node_pos = self._calcItemsNodeLocalPosition()
        item_size = self.items[0].getSize()

        item_pos = Mengine.vec2f(-items_node_pos.x + item_size.x / 2 + ITEMS_OFFSET_BETWEEN * i + item_size.x * i, 0)
        return item_pos

    def playRemovePanelItemAnim(self, source, item_obj):
        # remove item
        del self.items[self.drop_item_num]

        # play destroy panel item anim
        source.addScope(self.drop_item.playItemDestroyAnim)

        # re-calc VA content size
        source.addFunction(self._calcVirtualAreaContentSize)

        # block other movements of items
        source.addSemaphore(self.semaphore_allow_panel_items_move, From=True, To=False)
        source.addPrint(" * START ITEMS REMOVE ANIM")

        # move items in parallel with condition of sides
        for (i, item), tc in source.addParallelTaskList(enumerate(self.items)):
            item_node = item.getRoot()
            item_pos = self._calcItemLocalPosition(i)

            tc.addTask("TaskNodeMoveTo",
                       Node=item_node,
                       Time=ITEMS_MOVE_TIME,
                       Easing=ITEMS_MOVE_EASING,
                       To=item_pos)

        # Re-calculate item_node position if needed
        items_node_pos = self._calcItemsNodeLocalPosition()
        with source.addIfTask(lambda: items_node_pos.x >= self.virtual_area.get_content_size()[3]) as (move, _):
            move.addTask("TaskNodeMoveTo",
                         Node=self.items_node,
                         Time=ITEMS_NODE_MOVE_TIME,
                         Easing=ITEMS_MOVE_EASING,
                         To=items_node_pos)

        # fix VA after removing 1 item and moving all items
        source.addFunction(self.virtual_area.update_target)

        # allow other movements of items
        source.addSemaphore(self.semaphore_allow_panel_items_move, From=False, To=True)
        source.addPrint(" * END ITEMS REMOVE ANIM")

    def returnDropItem(self):
        self.items.insert(self.drop_item_num, self.drop_item)
        self.drop_item.attachTo(self.items_node)

    def playAddPanelItemAnim(self, source):
        # TODO check maybe remove validation
        if self.drop_item is None or self.drop_item_num is None:
            return

        # block other movements of items
        source.addSemaphore(self.semaphore_allow_panel_items_move, From=True, To=False)
        source.addPrint(" * START ITEMS ADD ANIM")

        # Create new Item
        source.addScope(self.drop_item.setItemVisible, False)

        # re-calc VA content size
        source.addFunction(self._calcVirtualAreaContentSize)

        # move elements to right from insert position
        for (i, item), parallel in source.addParallelTaskList(enumerate(self.items)):
            item_node = item.getRoot()
            item_pos = self._calcItemLocalPosition(i)

            parallel.addTask("TaskNodeMoveTo",
                       Node=item_node,
                       Time=ITEMS_MOVE_TIME,
                       Easing=ITEMS_MOVE_EASING,
                       To=item_pos)

        # Re-calculate items_node position
        items_node_pos = self._calcItemsNodeLocalPosition()
        with source.addIfTask(lambda: items_node_pos.x >= self.virtual_area.get_content_size()[3]) as (move, _):
            move.addTask("TaskNodeMoveTo",
                         Node=self.items_node,
                         Time=ITEMS_NODE_MOVE_TIME,
                         Easing=ITEMS_MOVE_EASING,
                         To=items_node_pos)

        # play add item animation
        source.addScope(self.drop_item.playItemCreateAnim)

        # Update VA
        source.addFunction(self.virtual_area.update_target)

        # Unblock other item movements
        source.addSemaphore(self.semaphore_allow_panel_items_move, From=False, To=True)
        # Clear variables
        # self.drop_item = None
        # self.drop_item_num = None
        source.addPrint(" * END ITEMS ADD ANIM")

    def moveLevelItemToPanelItem(self, source):
        source.addTask("TaskRemoveArrowAttach")
        # generate level item pure sprite

        item_entity = self.attach_item.item_obj.getEntity()
        item_pure = item_entity.generatePure()
        item_pure.enable()

        # create moving node
        item_moving_node = Mengine.createNode("Interender")
        item_moving_node.setName("BezierFollow")

        item_moving_node.setWorldPosition(self.attach_item.sprite_node.getWorldPosition())

        item_moving_node.addChild(item_pure)
        self.final_stage.addChild(item_moving_node)

        scale_from = self.attach_item.getSpriteScale()
        scale_to = (self.drop_item.getDefaultSpriteScale(), self.drop_item.getDefaultSpriteScale(), 1.0)

        panel_item_sprite = self.drop_item.getSprite()

        source.addFunction(self.attach_item.onFinalize)
        source.addFunction(self.attach_item.item_obj.setEnable, False)

        source.addPrint(" * START BEZIER ITEM ANIM")

        with source.addParallelTask(2) as (scale, move):
            scale.addTask("TaskNodeScaleTo",
                          Node=item_moving_node,
                          Easing=SCENE_ITEM_SCALE_EASING,
                          From=scale_from,
                          To=scale_to,
                          Time=SCENE_ITEM_SCALE_TIME)

            move.addTask("TaskNodeBezier2ScreenFollow",
                           Node=item_moving_node,
                           Easing=SCENE_ITEM_MOVE_EASING,
                           Follow=panel_item_sprite,
                           Time=SCENE_ITEM_MOVE_TIME)

        source.addPrint(" * END BEZIER ITEM ANIM")

        source.addTask("TaskNodeRemoveFromParent", Node=item_pure)
        source.addTask("TaskNodeDestroy", Node=item_pure)
        source.addTask("TaskNodeRemoveFromParent", Node=item_moving_node)
        source.addTask("TaskNodeDestroy", Node=item_moving_node)

    def validateDropPos(self, source):
        source.addFunction(self.returnDropItem)
        with source.addParallelTask(2) as (moving_item, add_item):
            moving_item.addScope(self.moveLevelItemToPanelItem)
            add_item.addScope(self.playAddPanelItemAnim)
        source.addScope(self.drop_item.setItemVisible, True)

    def itemDropSuccess(self):
        pass

    def itemDropFail(self):
        pass

    def addItem(self, item):
        pass

    def attachToCursor(self):
        arrow = Mengine.getArrow()
        arrow_node = arrow.getNode()

        self.attach_item = Item()
        self.attach_item.onInitialize(self, self.drop_item.item_obj, False)
        attach_item_root = self.attach_item.getRoot()

        ArrowManager.attachArrow(attach_item_root)
        arrow_node.addChildFront(attach_item_root)

    def scaleAttachItem(self, source):
        item_node = self.attach_item.sprite
        scale_from = self.attach_item.getSpriteScale()
        scale_to = (1.0, 1.0, 1.0)

        source.addTask("TaskNodeScaleTo",
                      Node=item_node,
                      Easing=SCENE_ITEM_SCALE_EASING,
                      From=scale_from,
                      To=scale_to,
                      Time=1000.0)
