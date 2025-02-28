from Foundation.Initializer import Initializer
from Foundation.Entities.MovieVirtualArea.VirtualArea import VirtualArea
from Game.Entities.GameArea.SearchPanel.Item import Item
from Game.Entities.GameArea.SearchPanel.ItemsCounter import ItemsCounter
from Game.Entities.GameArea.SearchPanel.Hint.Hint import Hint


MOVIE_PANEL = "Movie2_SearchPanel"
PANEL_VA = "virtual_area"
ITEMS_OFFSET_BETWEEN = 25.0

ITEMS_NODE_MOVE_TIME = 300.0
ITEMS_MOVE_TIME = 300.0
ITEMS_MOVE_EASING = "easyCubicInOut"   # easyLinear, easyBackInOut, easyBackOut, easyBounceOut, easyCubicOut, easyQuartOut


class SearchPanel(Initializer):
    def __init__(self):
        super(SearchPanel, self).__init__()
        self.game = None
        self.virtual_area = None
        self.root = None
        self.movie_panel = None
        self.lives_counter = None
        self.items_counter = None
        self.hint = None
        self.items = []
        self.removing_items = []
        self.items_node = None
        self.items_range = None
        self.semaphore_allow_panel_items_move = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game):
        super(SearchPanel, self)._onInitialize()
        self.game = game

        self._initVirtualArea()

        self._createRoot()
        self._attachPanel()
        self._initItems()

        self._setupItemsCounter()
        self._setupHint()

        self._setupVirtualArea()
        self._calcVirtualAreaContentSize()

        self._calcItemsRange()

        self.virtual_area.set_percentage(0.5, 0.0)  # on start always set VA to the middle of content
        self.semaphore_allow_panel_items_move = Semaphore(True, "AllowPanelItemsMove")
        return True

    def _onFinalize(self):
        super(SearchPanel, self)._onFinalize()

        if self.hint is not None:
            self.hint.onFinalize()
            self.hint = None

        if self.lives_counter is not None:
            self.lives_counter.onFinalize()
            self.lives_counter = None

        if self.items_counter is not None:
            self.items_counter.onFinalize()
            self.items_counter = None

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

        self.movie_panel = None
        self.items_range = None
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
        self.virtual_area.setup_with_movie(self.movie_panel, PANEL_VA, PANEL_VA)
        panel_bounds = self.getBounds()
        panel_size = self.getSize()

        self.virtual_area.setup_viewport(0, 0, panel_size.x, panel_size.y)
        self.virtual_area._socket.setDefaultHandle(True)

        panel_entity = self.movie_panel.getEntity()
        panel_entity.setSocketHandle(PANEL_VA, "button", False)
        panel_entity.setSocketHandle(PANEL_VA, "enter", False)
        panel_entity.setSocketHandle(PANEL_VA, "move", False)

        self.movie_panel.setInteractive(True)

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
        panel_bounds = self.getBounds()
        panel_size = Utils.getBoundingBoxSize(panel_bounds)
        return panel_size

    # - Hint -----------------------------------------------------------------------------------------------------------

    def _setupHint(self):
        self.hint = Hint()
        self.hint.onInitialize(self.game)
        self.hint.attachTo(self.root)

        panel_size = self.getSize()
        hint_node = self.hint.getRoot()
        hint_node.setLocalPosition(Mengine.vec2f(0, -panel_size.y / 2))

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

    def _calcItemsNodeLocalPosition(self, item):
        item_size = item.getSize()
        panel_size = self.getSize()
        items_count = len(self.items)

        items_node_pos_x = ((items_count * item_size.x) + ((items_count - 1) * ITEMS_OFFSET_BETWEEN)) / 2

        items_node_pos = Mengine.vec2f(items_node_pos_x, panel_size.y / 2)
        return items_node_pos

    def _calcItemLocalPosition(self, i, item):
        items_node_pos = self._calcItemsNodeLocalPosition(item)
        item_size = item.getSize()

        item_pos = Mengine.vec2f(-items_node_pos.x + item_size.x / 2 + ITEMS_OFFSET_BETWEEN * i + item_size.x * i, 0)
        return item_pos

    def _calcItemsRange(self):
        panel_size = self.getSize()

        border_node = Mengine.createNode("Interender")
        self.virtual_area.add_node(border_node)

        border_node.setLocalPosition(Mengine.vec2f(0, panel_size.y / 2))
        range_left = Mengine.getNodeScreenAdaptPosition(border_node)

        border_node.setLocalPosition(Mengine.vec2f(panel_size.x, panel_size.y / 2))
        range_right = Mengine.getNodeScreenAdaptPosition(border_node)

        self.items_range = (range_left.x, range_right.x)

        border_node.removeFromParent()
        Mengine.destroyNode(border_node)

    def getRandomAvailableItem(self):
        if len(self.items) is 0:
            return None

        available_items = []
        for item in self.items:
            item_node = item.getRoot()
            item_pos = Mengine.getNodeScreenAdaptPosition(item_node)

            if self.items_range[0] <= item_pos.x <= self.items_range[1]:
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
        self.items_counter.setLocalPosition(Mengine.vec2f((panel_size.x / 2) * 0.85, (panel_size.y / 2) * -0.75))

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
