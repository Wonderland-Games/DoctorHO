from Foundation.Initializer import Initializer
from Foundation.TaskManager import TaskManager
from Foundation.Entities.MovieVirtualArea.VirtualArea import VirtualArea
from Game.Entities.GameArea.SearchPanel.Item import Item


MOVIE_PANEL = "Movie2_SearchPanel"
PANEL_VA = "virtual_area"
ITEMS_OFFSET_BETWEEN = 100.0


class SearchPanel(Initializer):
    def __init__(self):
        super(SearchPanel, self).__init__()
        self.game = None
        self.virtual_area = None
        self.root = None
        self.movie_panel = None
        self.tcs = []
        self.items = []
        self.available_items = []
        self.items_node = None
        self.items_range = None
        self.print_available_items = True

    def _onInitialize(self, game):
        self.game = game

        self._initVirtualArea()

        self._createRoot()
        self._attachPanel()
        self._initItems()

        self._setupVirtualArea()

        self._setBordersRange()
        self._updateAvailableItems()
        return True

    def _onActivate(self):
        self.root.enable()
        self._runTaskChains()

    def _onFinalize(self):
        self.movie_panel = None
        self.items_range = None
        self.available_items = []
        self.print_available_items = True

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

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

    def _initVirtualArea(self):
        self.virtual_area = VirtualArea()
        self.virtual_area.onInitialize(
            dragging_mode="horizontal",
            enable_scale=False,
            disable_drag_if_invalid=False
        )

    def _setupVirtualArea(self):
        self.virtual_area.setup_with_movie(self.movie_panel, PANEL_VA, PANEL_VA)
        panel_size = self.getSize()

        self.virtual_area.setup_viewport(0, 0, panel_size.x, panel_size.y)
        # self.virtual_area.set_content_size(0, 0, panel_size.x, panel_size.y)

        self.virtual_area._socket.setDefaultHandle(False)

        panel_entity = self.movie_panel.getEntity()
        panel_entity.setSocketHandle(PANEL_VA, "button", False)
        panel_entity.setSocketHandle(PANEL_VA, "enter", False)
        panel_entity.setSocketHandle(PANEL_VA, "move", False)

        self.movie_panel.setInteractive(True)

        # callbacks
        self.virtual_area.on_drag_start += self._cbVirtualAreaDragStart
        self.virtual_area.on_drag += self._cbVirtualAreaDrag
        self.virtual_area.on_drag_end += self._cbVirtualAreaDragEnd

    def _cbVirtualAreaDragStart(self):
        self.print_available_items = False
        pass

    def _cbVirtualAreaDrag(self, x, y):
        self._updateAvailableItems()

    def _cbVirtualAreaDragEnd(self):
        self.print_available_items = True
        pass

    def _updateAvailableItems(self):
        for item in self.items:
            item_pos = Mengine.getNodeScreenPosition(item.getRoot())

            if self.items_range.x <= item_pos.x <= self.items_range.y:
                if item not in self.available_items:
                    self.available_items.append(item)
            else:
                if item in self.available_items:
                    self.available_items.remove(item)

        if self.print_available_items is False:
            return

        print("Available items", [available_item.item_obj.getName() for available_item in self.available_items if
                                  available_item.item_obj is not None])

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__)

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    def getSize(self):
        panel_bounds = self.movie_panel.getCompositionBounds()
        panel_size = Utils.getBoundingBoxSize(panel_bounds)
        return panel_size

    def _attachPanel(self):
        self.movie_panel = self.game.object.getObject(MOVIE_PANEL)
        movie_panel_node = self.movie_panel.getEntityNode()
        self.root.addChild(movie_panel_node)

    def _initItems(self):
        self.items_node = Mengine.createNode("Interender")
        self.items_node.setName("Items")

        self.virtual_area.add_node(self.items_node)

        panel_size = self.getSize()
        self.items_node.setLocalPosition(Mengine.vec2f(0, panel_size.y / 2))

        content_size_x = 0

        for i, item_obj in enumerate(self.game.search_level.items):
            item = Item()
            item.onInitialize(self.game, item_obj)
            item.attachTo(self.items_node)
            item_size = item.getSize()
            item.setLocalPositionX(item_size.x / 2 + item_size.x * i + ITEMS_OFFSET_BETWEEN * i)
            content_size_x += item_size.x + ITEMS_OFFSET_BETWEEN
            self.items.append(item)

        content_size_x -= ITEMS_OFFSET_BETWEEN
        if content_size_x <= panel_size.x:
            self.virtual_area.set_content_size(0, 0, panel_size.x, panel_size.y)
        else:
            self.virtual_area.set_content_size(0, 0, content_size_x, panel_size.y)

    def _setBordersRange(self):
        panel_size = self.getSize()

        border_node = Mengine.createNode("Interender")
        self.virtual_area.add_node(border_node)

        border_node.setLocalPosition(Mengine.vec2f(0, panel_size.y / 2))
        range_left = Mengine.getNodeScreenPosition(border_node)

        border_node.setLocalPosition(Mengine.vec2f(panel_size.x, panel_size.y / 2))
        range_right = Mengine.getNodeScreenPosition(border_node)

        self.items_range = Mengine.vec2f(range_left.x, range_right.x)

        Mengine.destroyNode(border_node)

    def getAvailableItems(self):
        return self.available_items

    def removeItem(self, item_obj):
        removing_item = None

        # finalize removing item
        for item in self.items:
            if item.item_obj is not item_obj:
                continue

            removing_item = item
            item.onFinalize()
            # self.items.remove(item)
            break

        items_after = list(self.items[self.items.index(removing_item) + 1:])
        self.items.remove(removing_item)

        # remove items from right to left
        for item in items_after:
            item_size = item.getSize()
            item_pos = item.getRoot().getLocalPosition()
            item.setLocalPositionX(item_pos.x - (item_size.x + ITEMS_OFFSET_BETWEEN))

        # re-calculate VA content size
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

        self._updateAvailableItems()

    def _createTaskChain(self, name, **params):
        tc = TaskManager.createTaskChain(Name=self.__class__.__name__+"_"+name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        pass
