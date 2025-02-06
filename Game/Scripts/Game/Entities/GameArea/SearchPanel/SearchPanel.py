from Foundation.Initializer import Initializer
from Foundation.Entities.MovieVirtualArea.VirtualArea import VirtualArea
from Game.Entities.GameArea.SearchPanel.Item import Item


MOVIE_PANEL = "Movie2_SearchPanel"
PANEL_VA = "virtual_area"
ITEMS_OFFSET_BETWEEN = 25.0

ITEMS_NODE_MOVE_TIME = 350.0
ITEMS_MOVE_TIME = 250.0
ITEMS_MOVE_EASING = "easyLinear"   # easyBackOut, easyBounceOut,


class SearchPanel(Initializer):
    def __init__(self):
        super(SearchPanel, self).__init__()
        self.game = None
        self.virtual_area = None
        self.root = None
        self.movie_panel = None
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
        self._calcVirtualAreaContentSize()

        self._calcItemsRange()
        self._updateAvailableItems()

        # always set VA to the middle of items
        self.virtual_area.set_percentage(0.5, 0.0)
        return True

    def _onFinalize(self):
        self.movie_panel = None
        self.items_range = None
        self.available_items = []
        self.print_available_items = True

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

    def _cbVirtualAreaDragStart(self):
        self.print_available_items = False

    def _cbVirtualAreaDrag(self, x, y):
        self._updateAvailableItems()

    def _cbVirtualAreaDragEnd(self):
        self.print_available_items = True

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

    def getRoot(self):
        return self.root

    def getSize(self):
        panel_bounds = self.movie_panel.getCompositionBounds()
        panel_size = Utils.getBoundingBoxSize(panel_bounds)
        return panel_size

    def _attachPanel(self):
        self.movie_panel = self.game.object.getObject(MOVIE_PANEL)
        movie_panel_node = self.movie_panel.getEntityNode()
        self.root.addChild(movie_panel_node)

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

        # calculate items_node local position (middle)
        item_size = self.items[0].getSize()
        panel_size = self.getSize()
        items_count = len(self.items)

        items_node_pos_x = ((items_count * item_size.x) + ((items_count - 1) * ITEMS_OFFSET_BETWEEN)) / 2
        self.items_node.setLocalPosition(Mengine.vec2f(items_node_pos_x, panel_size.y / 2))

        # set items local position
        for i, item in enumerate(self.items):
            item.setLocalPositionX(-items_node_pos_x + item_size.x / 2 + ITEMS_OFFSET_BETWEEN * i + item_size.x * i)

    def _calcItemsRange(self):
        panel_size = self.getSize()

        border_node = Mengine.createNode("Interender")
        self.virtual_area.add_node(border_node)

        border_node.setLocalPosition(Mengine.vec2f(0, panel_size.y / 2))
        range_left = Mengine.getNodeScreenPosition(border_node)

        border_node.setLocalPosition(Mengine.vec2f(panel_size.x, panel_size.y / 2))
        range_right = Mengine.getNodeScreenPosition(border_node)

        self.items_range = Mengine.vec2f(range_left.x, range_right.x)

        border_node.removeFromParent()
        Mengine.destroyNode(border_node)

    def getAvailableItems(self):
        return self.available_items

    def playRemovePanelItemAnim(self, source, item_obj):
        # find item by object
        item_to_remove = None
        for item in self.items:
            if item.item_obj is not item_obj:
                continue

            item_to_remove = item
            break

        # get info about items to the sides
        items_before = list(self.items[:self.items.index(item_to_remove)])
        items_after = list(self.items[self.items.index(item_to_remove) + 1:])
        items_before_len, items_after_len = len(items_before), len(items_after)

        # remove item
        self.items.remove(item_to_remove)
        items_node_pos = self.items_node.getLocalPosition()

        # play destroy panel item anim
        source.addScope(item_to_remove.playItemDestroyAnim)
        source.addFunction(item_to_remove.onFinalize)

        # move items in parallel with condition of sides
        for item, tc in source.addParallelTaskList(self.items):
            item_size = item.getSize()
            item_pos = item.getRoot().getLocalPosition()

            if items_before_len > items_after_len:
                if item not in items_before:
                    continue

                # item.setLocalPositionX(item_pos.x + (item_size.x + ITEMS_OFFSET_BETWEEN))
                item_move_pos = Mengine.vec2f(item_pos.x + (item_size.x + ITEMS_OFFSET_BETWEEN), item_pos.y)
                items_node_pos_new = Mengine.vec2f(items_node_pos.x - item_size.x - ITEMS_OFFSET_BETWEEN,
                                                   items_node_pos.y)

            elif items_before_len < items_after_len:
                if item not in items_after:
                    continue

                # item.setLocalPositionX(item_pos.x - (item_size.x + ITEMS_OFFSET_BETWEEN))
                item_move_pos = Mengine.vec2f(item_pos.x - (item_size.x + ITEMS_OFFSET_BETWEEN), item_pos.y)
                items_node_pos_new = items_node_pos

            elif items_before_len == items_after_len:
                if item in items_before:
                    # item.setLocalPositionX(item_pos.x + (item_size.x + ITEMS_OFFSET_BETWEEN) / 2)
                    item_move_pos = Mengine.vec2f(item_pos.x + (item_size.x + ITEMS_OFFSET_BETWEEN) / 2, item_pos.y)

                    items_node_pos_new = Mengine.vec2f(items_node_pos.x + item_size.x / 2 - ITEMS_OFFSET_BETWEEN / 2,
                                                       items_node_pos.y)

                elif item in items_after:
                    # item.setLocalPositionX(item_pos.x - (item_size.x + ITEMS_OFFSET_BETWEEN) / 2)
                    item_move_pos = Mengine.vec2f(item_pos.x - (item_size.x + ITEMS_OFFSET_BETWEEN) / 2, item_pos.y)

                    items_node_pos_new = Mengine.vec2f(items_node_pos.x - item_size.x / 2 - ITEMS_OFFSET_BETWEEN / 2,
                                                       items_node_pos.y)

            tc.addFunction(self._calcVirtualAreaContentSize)

            with tc.addParallelTask(2) as(tc_item, tc_items_node):
                tc_item.addTask("TaskNodeMoveTo", Node=item.getRoot(), Time=ITEMS_MOVE_TIME, Easing=ITEMS_MOVE_EASING, To=item_move_pos)
                tc_items_node.addTask("TaskNodeMoveTo", Node=self.items_node, Time=ITEMS_NODE_MOVE_TIME, Easing=ITEMS_MOVE_EASING, To=items_node_pos_new)

            tc.addFunction(self._updateAvailableItems)
