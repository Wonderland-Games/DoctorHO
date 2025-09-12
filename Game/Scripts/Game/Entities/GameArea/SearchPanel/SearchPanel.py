from Foundation.Initializer import Initializer
from Foundation.Entities.MovieVirtualArea.VirtualArea import VirtualArea
from Game.Entities.GameArea.SearchPanel.Item import Item
from Game.Entities.GameArea.SearchPanel.ItemsCounter import ItemsCounter
from Game.Entities.GameArea.SearchPanel.Hint.Hint import Hint
from Game.Entities.GameArea.SearchPanel.Hint.HintAd import HintAd
from UIKit.Managers.PrototypeManager import PrototypeManager
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils


MOVIE_PANEL = "Movie2_SearchPanel"
ITEMS_OFFSET_BETWEEN = 25.0

ITEMS_NODE_MOVE_TIME = 300.0
ITEMS_MOVE_TIME = 300.0
ITEMS_MOVE_EASING = "easyCubicInOut"   # easyLinear, easyBackInOut, easyBackOut, easyBounceOut, easyCubicOut, easyQuartOut

PROTOTYPE_ITEMS_CORNER = "SearchItemsCorner"


class SearchPanel(Initializer):
    def __init__(self):
        super(SearchPanel, self).__init__()
        self.game = None
        self.virtual_area = None
        self.va_hotspot = None
        self.root = None
        self.movie_panel = None
        self.lives_counter = None
        self.items_counter = None
        self.hint = None
        self.hint_ad = None
        self.items = []
        self.removing_items = []
        self.items_node = None
        self.items_scale_node = None
        self.va_range_points = None
        self.movie_items_corners = {}
        self.semaphore_allow_panel_items_move = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game):
        super(SearchPanel, self)._onInitialize()
        self.game = game

        self._initVirtualArea()

        self._createRoot()
        self._createHint()
        self._attachPanel()

        return True

    def onInitialize2(self):
        self._initItems()

        self._setupItemsCounter()
        self._setupHint()
        self._setupHintAd()
        self.switchHints()

        self._setupVirtualArea()

        self._calcItemsRange()
        self._setupItemsCorners()
        self._setupItemsAffector()

        self.virtual_area.set_percentage(0.5, 0.0)  # on start always set VA to the middle of content
        self.semaphore_allow_panel_items_move = Semaphore(True, "AllowPanelItemsMove")

    def _onFinalize(self):
        super(SearchPanel, self)._onFinalize()

        self.destroyHint()
        self.destroyHintAd()

        if self.lives_counter is not None:
            self.lives_counter.onFinalize()
            self.lives_counter = None

        if self.items_counter is not None:
            self.items_counter.onFinalize()
            self.items_counter = None

        for corner in self.movie_items_corners.values():
            if corner is not None:
                corner.onDestroy()
        self.movie_items_corners = {}

        for item in self.items:
            item.onFinalize()
        self.items = []

        if self.items_node is not None:
            Mengine.destroyNode(self.items_node)
            self.items_node = None

        if self.items_scale_node is not None:
            Mengine.destroyNode(self.items_scale_node)
            self.items_scale_node = None

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
        self.va_range_points = None
        self.removing_items = []
        self.semaphore_allow_panel_items_move = None

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
            name="SearchPanelVirtualArea",
            dragging_mode="horizontal",
            enable_scale=False,
            disable_drag_if_invalid=False,
            camera_name="SearchPanelVirtualCamera",
            viewport_name="SearchPanelViewport",
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
        hotspot_polygon_center = (
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
        self._calcVirtualAreaContentSize()

        # attach VA to root
        virtual_area_node = self.virtual_area.get_node()
        self.root.addChild(virtual_area_node)
        virtual_area_node.setLocalPosition(hotspot_polygon_center)

    def _calcVirtualAreaContentSize(self):
        content_size_x = 0

        for item in self.items:
            item_size = item.getSize()
            content_size_x += item_size.x + ITEMS_OFFSET_BETWEEN
        content_size_x -= ITEMS_OFFSET_BETWEEN

        panel_size = self.getSize()
        if content_size_x <= panel_size.x:
            self.virtual_area.set_content_size(0, 0, panel_size.x, panel_size.y)
        else:
            self.virtual_area.set_content_size(0, 0, content_size_x, panel_size.y)

    # - Panel ----------------------------------------------------------------------------------------------------------

    def _attachPanel(self):
        self.movie_panel = self.game.object.getObject(MOVIE_PANEL)
        self.movie_panel.setInteractive(True)
        movie_panel_node = self.movie_panel.getEntityNode()
        self.root.addChild(movie_panel_node)

    def getSize(self):
        game_width = AdjustableScreenUtils.getGameWidth()
        panel_bounds = self.movie_panel.getCompositionBounds()
        panel_bounds_size = Utils.getBoundingBoxSize(panel_bounds)
        return Mengine.vec2f(game_width, panel_bounds_size.y)

    def getSizeFull(self):
        panel_size = self.getSize()
        hint_size = self.hint.getSize()
        return Mengine.vec2f(panel_size.x, panel_size.y + hint_size.y/2)

    # - Hint -----------------------------------------------------------------------------------------------------------

    def _createHint(self):
        self.hint = Hint()
        self.hint.onInitialize(self.game)
        self.hint.attachTo(self.root)

    def _setupHint(self):
        panel_size = self.getSize()
        hint_size = self.hint.getSize()
        hint_node = self.hint.getRoot()

        hint_pos_y = -panel_size.y / 2 + hint_size.y / 2
        hint_node.setLocalPosition((0, hint_pos_y))

    def destroyHint(self):
        if self.hint is not None:
            self.hint.onFinalize()
            self.hint = None

    # - HintAd ---------------------------------------------------------------------------------------------------------

    def _setupHintAd(self):
        self.hint_ad = HintAd()
        self.hint_ad.onInitialize(self.game)
        self.hint_ad.attachTo(self.root)

        panel_size = self.getSize()
        hint_size = self.hint.getSize()
        hint_node = self.hint_ad.getRoot()

        hint_pos_y = -panel_size.y / 2 + hint_size.y / 2
        hint_node.setLocalPosition((0, hint_pos_y))

    def destroyHintAd(self):
        if self.hint_ad is not None:
            self.hint_ad.onFinalize()
            self.hint_ad = None

    # - Hint Tools -----------------------------------------------------------------------------------------------------

    def switchHints(self):
        hint_available = self.hint.isAvailable()
        hint_node = self.hint.getRoot()
        hint_ad_node = self.hint_ad.getRoot()

        if hint_available:
            hint_node.enable()
            hint_ad_node.disable()
        else:
            hint_ad_node.enable()
            hint_node.disable()

    # - Items ----------------------------------------------------------------------------------------------------------

    def _initItems(self):
        # create items node
        self.items_node = Mengine.createNode("Interender")
        self.items_node.setName("Items")
        self.virtual_area.add_node(self.items_node)

        # init items
        for i, item_obj in enumerate(self.game.search_level.items):
            item = Item()
            item.onInitialize(self.game, item_obj)
            item.attachTo(self.items_node)
            self.items.append(item)

        items_node_pos = self._calcItemsNodeLocalPosition(self.items[0])
        self.items_node.setLocalPosition(items_node_pos)

        # set items local position
        for i, item in enumerate(self.items):
            item_pos = self._calcItemLocalPosition(i, item)
            item.setLocalPositionX(item_pos.x)

    def _setupItemsCorners(self):
        corner_types = ["Left", "Right"]

        for corner_type in corner_types:
            corner = PrototypeManager.generateObjectUnique(PROTOTYPE_ITEMS_CORNER, PROTOTYPE_ITEMS_CORNER, Size=corner_type)
            corner.setEnable(True)

            corner_node = corner.getEntityNode()
            self.root.addChild(corner_node)

            va_hotspot_pos = self.va_hotspot.getLocalPosition()
            corner_bb = corner.getCompositionBounds()
            corner_size = Utils.getBoundingBoxSize(corner_bb)

            if corner_type is "Left":
                corner_pos = (
                    va_hotspot_pos.x + corner_size.x / 2,
                    va_hotspot_pos.y + corner_size.y / 2
                )
            else:
                corner_pos = (
                    -va_hotspot_pos.x - corner_size.x / 2,
                    va_hotspot_pos.y + corner_size.y / 2
                )
            corner_node.setLocalPosition(corner_pos)

            self.movie_items_corners[corner_type] = corner

    def _calcItemsNodeLocalPosition(self, item):
        item_size = item.getSize()
        items_count = len(self.items)

        items_node_pos_x = ((items_count * item_size.x) + ((items_count - 1) * ITEMS_OFFSET_BETWEEN)) / 2
        items_node_pos_y = item_size.y / 2

        items_node_pos = Mengine.vec2f(items_node_pos_x, items_node_pos_y)
        return items_node_pos

    def _calcItemLocalPosition(self, i, item):
        items_node_pos = self._calcItemsNodeLocalPosition(item)
        item_size = item.getSize()

        item_pos = Mengine.vec2f(-items_node_pos.x + item_size.x / 2 + ITEMS_OFFSET_BETWEEN * i + item_size.x * i, 0)
        return item_pos

    def _calcItemsRange(self):
        va_hotspot_bb = Mengine.getHotSpotPolygonBoundingBox(self.va_hotspot)
        va_hotspot_size = Utils.getBoundingBoxSize(va_hotspot_bb)

        border_node = Mengine.createNode("Interender")
        self.virtual_area.add_node(border_node)

        border_node.setLocalPosition((0, 0))
        range_left_top = Mengine.getNodeScreenAdaptPosition(border_node)

        border_node.setLocalPosition((va_hotspot_size.x, va_hotspot_size.y))
        range_right_bot = Mengine.getNodeScreenAdaptPosition(border_node)

        self.va_range_points = (range_left_top, range_right_bot)

        border_node.removeFromParent()
        Mengine.destroyNode(border_node)

    # old logic (can be deleted)
    def _handleItemsScale(self, source=None):
        range_middle_x = (self.va_range_points[1].x - self.va_range_points[0].x) / 2
        range_middle_y = (self.va_range_points[1].y - self.va_range_points[0].y) / 2
        middle_pos = Mengine.vec2f(range_middle_x, range_middle_y)

        for item in self.items:
            item_node = item.getRoot()
            item_pos = Mengine.getNodeScreenAdaptPosition(item_node)

            distance = Mengine.length_v2_v2(middle_pos, item_pos)

            scale_perc = 1.0 - distance
            if scale_perc < 0.0:
                scale_perc = 0.0

            item_node.setScale((scale_perc, scale_perc, 1.0))

    def _setupItemsAffector(self):
        self.items_scale_node = Mengine.createNode("Interender")
        self.items_scale_node.setName("TargetAffectorUIWheelOfFortune")

        self.root.addChild(self.items_scale_node)

        va_hotspot_pos = self.va_hotspot.getLocalPosition()
        self.items_scale_node.setLocalPosition((0, va_hotspot_pos.y))

        coeff = 1.0
        for item in self.items:
            item_node = item.getRoot()
            Mengine.affectorUIWheelOfFortune(item_node, self.items_scale_node, coeff)

    def getRandomAvailableItem(self):
        if len(self.items) is 0:
            return None

        available_items = []
        for item in self.items:
            item_node = item.getRoot()
            item_pos = Mengine.getNodeScreenAdaptPosition(item_node)

            if self.va_range_points[0].x <= item_pos.x <= self.va_range_points[1].x:
                if item not in self.removing_items:
                    available_items.append(item)

        item_index = Mengine.range_rand(0, len(available_items))
        return available_items[item_index]

    def addRemovingItem(self, item_obj):
        for item in self.items:
            if item.item_obj is item_obj:
                self.removing_items.append(item)
                break

        print("Removing items", [removing_item.item_obj.getName() for removing_item in self.removing_items if
                                 removing_item.item_obj is not None])

    def getRemovingItems(self):
        return self.removing_items

    # - ItemsCounter ---------------------------------------------------------------------------------------------------

    def _setupItemsCounter(self):
        items_count = len(self.items)
        self.items_counter = ItemsCounter()
        self.items_counter.onInitialize(0, items_count)

        panel_size = self.getSize()
        self.items_counter.attachTo(self.root)
        self.items_counter.setLocalPosition(((panel_size.x / 2) * 0.75, (panel_size.y / 2) * -0.35))

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def playRemovePanelItemAnim(self, source, item_obj):
        # find item by object
        item_to_remove = None
        for item in self.items:
            if item.item_obj is not item_obj:
                continue

            item_to_remove = item
            break

        # remove item
        self.removing_items.remove(item_to_remove)
        self.items.remove(item_to_remove)
        self.items_counter.incItemsCount()

        # play destroy panel item anim
        source.addScope(item_to_remove.playItemDestroyAnim)
        source.addFunction(item_to_remove.onFinalize)

        # re-calc VA content size
        source.addFunction(self._calcVirtualAreaContentSize)

        # block other movements of items
        source.addSemaphore(self.semaphore_allow_panel_items_move, From=True, To=False)
        source.addPrint(" * START ITEMS MOVE ANIM")

        # move items in parallel with condition of sides
        for (i, item), tc in source.addParallelTaskList(enumerate(self.items)):
            item_node = item.getRoot()
            items_node_pos = self._calcItemsNodeLocalPosition(item)
            item_pos = self._calcItemLocalPosition(i, item)

            with tc.addParallelTask(2) as(tc_item, tc_items_node):
                tc_item.addTask("TaskNodeMoveTo", Node=item_node, Time=ITEMS_MOVE_TIME, Easing=ITEMS_MOVE_EASING, To=item_pos)
                with tc_items_node.addIfTask(lambda: items_node_pos.x >= self.virtual_area.get_content_size()[3]) as (move, _):
                    move.addTask("TaskNodeMoveTo", Node=self.items_node, Time=ITEMS_NODE_MOVE_TIME, Easing=ITEMS_MOVE_EASING, To=items_node_pos)

        # fix VA after removing 1 item and moving all items
        source.addFunction(self.virtual_area.update_target)

        # allow other movements of items
        source.addSemaphore(self.semaphore_allow_panel_items_move, From=False, To=True)
        source.addPrint(" * END ITEMS MOVE ANIM")
