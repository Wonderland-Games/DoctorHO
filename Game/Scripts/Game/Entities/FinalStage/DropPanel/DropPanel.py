from Foundation.Initializer import Initializer
from Foundation.Entities.MovieVirtualArea.VirtualArea import VirtualArea
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils
from UIKit.Managers.PrototypeManager import PrototypeManager


MOVIE_PANEL = "Movie2_DropPanel"
ITEMS_NODE_MOVE_TIME = 300.0
PROTOTYPE_ITEMS_CORNER = "SearchItemsCorner"


class DropPanel(Initializer):
    def __init__(self):
        super(DropPanel, self).__init__()
        self.game = None
        self.virtual_area = None
        self.va_hotspot = None
        self.root = None
        self.movie_panel = None
        self.lives_counter = None
        self.items_counter = None
        self.items = []
        self.removing_items = []
        self.items_node = None
        self.items_scale_node = None
        self.va_range_points = None
        self.movie_items_corners = {}
        self.semaphore_allow_panel_items_move = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game):
        super(DropPanel, self)._onInitialize()
        self.game = game

        self._initVirtualArea()

        self._createRoot()
        self._attachPanel()

        return True

    def onInitialize2(self):
        self._initItems()

        self._setupItemsCounter()

        self._setupVirtualArea()
        self._calcVirtualAreaContentSize()

        self._setupItemsCorners()

        self.virtual_area.set_percentage(0.5, 0.0)  # on start always set VA to the middle of content
        self.semaphore_allow_panel_items_move = Semaphore(True, "AllowPanelItemsMove")

    def _onFinalize(self):
        super(DropPanel, self)._onFinalize()

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
            corner = PrototypeManager.generateObjectUnique(PROTOTYPE_ITEMS_CORNER, PROTOTYPE_ITEMS_CORNER,
                                                           Size=corner_type)
            corner.setEnable(True)

            corner_node = corner.getEntityNode()
            self.root.addChild(corner_node)

            va_hotspot_pos = self.va_hotspot.getLocalPosition()
            corner_bb = corner.getCompositionBounds()
            corner_size = Utils.getBoundingBoxSize(corner_bb)

            if corner_type is "Left":
                corner_pos = Mengine.vec2f(
                    va_hotspot_pos.x + corner_size.x / 2,
                    va_hotspot_pos.y + corner_size.y / 2
                )
            else:
                corner_pos = Mengine.vec2f(
                    -va_hotspot_pos.x - corner_size.x / 2,
                    va_hotspot_pos.y + corner_size.y / 2
                )
            corner_node.setLocalPosition(corner_pos)

            self.movie_items_corners[corner_type] = corner
