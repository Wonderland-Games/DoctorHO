from Foundation.Initializer import Initializer
from Foundation.Entities.MovieVirtualArea.VirtualArea import VirtualArea
from Game.Managers.GameManager import GameManager
from Game.Entities.FinalStage.FinalStageDropItem.FinalStageDropItem import FinalStageDropItem


MOVIE_PANEL = "Movie2_DropPanel"

ITEMS_OFFSET_BETWEEN = 25.0

ITEMS_MOVE_TIME = 300.0
ITEMS_MOVE_EASING = "easyCubicInOut"

SCENE_ANIMATION_TIME = 1000.0
SCENE_SCALE_EASING = "easyBackOut"

HARDCODED_PANEL_WIDTH = 1170.0  # 9:19.5 aspect ratio game width


class DropPanel(Initializer):
    def __init__(self):
        super(DropPanel, self).__init__()
        self.game = None
        self.virtual_area = None
        self.va_hotspot = None
        self.root = None
        self.movie_panel = None
        self.items = []
        self.removed_items = []
        self.items_node = None
        self.va_range_points = None
        self.semaphore_allow_panel_items_move = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game):
        super(DropPanel, self)._onInitialize()

        self.game = game
        self.movie_panel = self.game.object.getObject(MOVIE_PANEL)

        self._fillQuestItems()

        self._initVirtualArea()

        self._createRoot()
        self._attachPanel()

        self._initItems()

        self._setupVirtualArea()

        self.virtual_area.set_percentage(0.5, 0.0)  # on start always set VA to the middle of content
        self.semaphore_allow_panel_items_move = Semaphore(True, "AllowPanelItemsMove")

        return True

    def _onFinalize(self):
        super(DropPanel, self)._onFinalize()

        for item in self.items:
            item.onFinalize()
        self.items = []

        for item in self.removed_items:
            item.onFinalize()
        self.removed_items = []

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
        self.va_range_points = None
        self.semaphore_allow_panel_items_move = None
        self.game = None

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
        if not self.items:
            return

        content_size_x = sum(item.getSize().x for item in self.items) + (len(self.items) - 1) * ITEMS_OFFSET_BETWEEN
        panel_size = self.getSize()

        item_size = Mengine.vec2f(200.0, 200.0)
        center_panel_pos = Mengine.vec2f(panel_size.x / 2, item_size.y / 2)

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
        panel_bounds = self.getBounds()
        panel_bounds_size = Utils.getBoundingBoxSize(panel_bounds)
        return Mengine.vec2f(HARDCODED_PANEL_WIDTH, panel_bounds_size.y)

    # - Items ----------------------------------------------------------------------------------------------------------

    def _fillQuestItems(self):
        current_quest_index = GameManager.getCurrentQuestIndex()
        final_stage_params = GameManager.getCurrentFinalStageMappingParams()

        for i, param in enumerate(final_stage_params):
            if i >= current_quest_index:
                break

            movie_info = {
                "group": param.GroupName,
                "name": param.MovieName
            }

            item = FinalStageDropItem()
            item.onInitialize(self, param.ItemName, movie_info)
            self.items.append(item)

    def _initItems(self):
        # create items node
        self.items_node = Mengine.createNode("Interender")
        self.items_node.setName("Items")
        self.virtual_area.add_node(self.items_node)

        for item in self.items:
            item.attachTo(self.items_node)

        items_node_pos = self._calcItemsNodeLocalPosition()
        self.items_node.setLocalPosition(items_node_pos)

        # set items local position
        for i, item in enumerate(self.items):
            item_pos = self._calcItemLocalPosition(i)
            item.setLocalPositionX(item_pos.x)

    def findItemIndex(self, drop_item):
        index = None
        for i, item in enumerate(self.items):
            if item is drop_item:
                index = i
                break

        return index

    def _calcItemsNodeLocalPosition(self):
        if not self.items:
            return Mengine.vec2f(0.0, 0.0)

        content_width = sum(item.getSize().x for item in self.items) + (len(self.items) - 1) * ITEMS_OFFSET_BETWEEN

        content_height = self.items[0].getSize().y

        return Mengine.vec2f(content_width / 2.0, content_height / 2.0)

    def _calcItemLocalPosition(self, i):
        """
        Рахує локальну позицію айтема в межах items_node так, щоб:
        - увесь ряд був центрований відносно items_node (x = 0),
        - між айтемами зберігалася відстань ITEMS_OFFSET_BETWEEN,
        - враховувались реальні розміри айтемів.
        """

        if not self.items:
            return Mengine.vec2f(0.0, 0.0)

        items_node_pos = self._calcItemsNodeLocalPosition()

        # ліва межа контенту в локальних координатах items_node
        left_x = -items_node_pos.x
        current_x = left_x

        for index, item in enumerate(self.items):
            item_width = item.getSize().x
            item_center_x = current_x + item_width / 2.0

            if index == i:
                return Mengine.vec2f(item_center_x, 0.0)

            current_x += item_width + ITEMS_OFFSET_BETWEEN

        # fallback (не має траплятися, але щоб не падати)
        return Mengine.vec2f(0.0, 0.0)

    def returnDropItem(self, item, item_index):
        if item in self.items:
            return

        if self.items:
            self.items.insert(item_index, item)
        else:
            self.items.append(item)
        self.removeRemovedItems(item)

        item.attachTo(self.items_node)

    def appendRemovedItems(self, item):
        if item not in self.removed_items:
            self.removed_items.append(item)

    def removeRemovedItems(self, item):
        if item in self.removed_items:
            self.removed_items.remove(item)

    def _moveItemsToTargetPositions(self, source):
        """
        Анімація зміщення всіх айтемів у нові цільові позиції.
        Порядок та кількість айтемів береться з self.items.
        У результаті весь ряд центрований у межах панелі,
        а відстань між айтемами зберігається.
        """

        if not self.items:
            return

        for (i, item), parallel in source.addParallelTaskList(enumerate(self.items)):
            item_node = item.getRoot()
            target_local_pos = self._calcItemLocalPosition(i)

            # зберігаємо поточний Y, рухаємо лише по X
            current_pos = item_node.getLocalPosition()
            target_pos = Mengine.vec2f(target_local_pos.x, current_pos.y)

            parallel.addTask("TaskNodeMoveTo", Node=item_node, Time=ITEMS_MOVE_TIME, Easing=ITEMS_MOVE_EASING, To=target_pos)

    def _moveItemsNode(self, source):
        """
        Центрує вузол items_node відносно панелі (по X) плавною анімацією.
        Це доповнює зміщення окремих айтемів і гарантує,
        що весь ряд залишиться по центру панелі.
        """

        if self.items_node is None or not self.items:
            return

        panel_size = self.getSize()
        item_height = self.items[0].getSize().y

        target_pos = Mengine.vec2f(panel_size.x / 2.0, item_height / 2.0)
        current_pos = self.items_node.getLocalPosition()

        if current_pos == target_pos:
            return

        source.addTask("TaskNodeMoveTo", Node=self.items_node, Time=ITEMS_MOVE_TIME, Easing=ITEMS_MOVE_EASING, To=target_pos)

    def _updateVirtualArea(self):
        self._calcVirtualAreaContentSize()
        self.virtual_area.update_target()

    def playRemovePanelItemAnim(self, source, item, item_index):
        source.addScope(item.setSpriteEnable, False)
        source.addScope(item.playItemDestroyAnim)
        source.addFunction(self.items.remove, item)
        source.addFunction(self.appendRemovedItems, item)
        
        source.addSemaphore(self.semaphore_allow_panel_items_move, From=True, To=False)
        source.addPrint(" * START ITEMS REMOVE ANIM")

        source.addScope(self._moveItemsToTargetPositions)
        source.addScope(self._moveItemsNode)

        source.addFunction(self._updateVirtualArea)
        source.addSemaphore(self.semaphore_allow_panel_items_move, From=False, To=True)
        source.addPrint(" * END ITEMS REMOVE ANIM")

    def playAddPanelItemAnim(self, source, item):
        source.addSemaphore(self.semaphore_allow_panel_items_move, From=True, To=False)
        source.addPrint(" * START ITEMS ADD ANIM")

        source.addScope(item.setSpriteEnable, False)

        source.addScope(self._moveItemsToTargetPositions)
        source.addScope(self._moveItemsNode)

        source.addScope(item.playItemCreateAnim)
        source.addFunction(self._updateVirtualArea)

        source.addSemaphore(self.semaphore_allow_panel_items_move, From=False, To=True)
        source.addPrint(" * END ITEMS ADD ANIM")
