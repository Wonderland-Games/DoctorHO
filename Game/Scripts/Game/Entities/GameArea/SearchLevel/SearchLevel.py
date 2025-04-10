from Foundation.Initializer import Initializer
from Foundation.GroupManager import GroupManager
from Foundation.DefaultManager import DefaultManager
from Foundation.Entities.MovieVirtualArea.VirtualArea import VirtualArea
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils
from Game.Managers.GameManager import GameManager


class SearchLevel(Initializer):
    def __init__(self):
        super(SearchLevel, self).__init__()
        self.root = None
        self.virtual_area = None
        self.va_hotspot = None
        self.game = None
        self.box_points = None
        self.items = []

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game, box_points):
        self.game = game
        self.box_points = box_points

        self._initVirtualArea()

        self._createRoot()
        self._setupVirtualArea()
        self._attachScene()
        self._fillItems()
        return True

    def _onFinalize(self):
        self.game = None
        self.box_points = None
        self.items = []

        if self.root is not None:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

        if self.virtual_area is not None:
            self.virtual_area.onFinalize()
            self.virtual_area = None

        if self.va_hotspot is not None:
            self.va_hotspot.removeFromParent()
            Mengine.destroyNode(self.va_hotspot)
            self.va_hotspot = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__)

    def getRoot(self):
        return self.root

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    # - VirtualArea ----------------------------------------------------------------------------------------------------

    def _initVirtualArea(self):
        if _DESKTOP is True:  # run on PC
            scale_factor = DefaultManager.getDefaultFloat("DesktopScaleFactor", 0.05)
        else:
            scale_factor = DefaultManager.getDefaultFloat("TouchpadScaleFactor", 0.005)

        self.virtual_area = VirtualArea()
        self.virtual_area.onInitialize(
            name="SearchLevelVirtualArea",
            dragging_mode="free",
            enable_scale=True,
            max_scale=DefaultManager.getDefaultFloat("TouchpadMaxScale", 2.0),
            scale_factor=scale_factor,
            disable_drag_if_invalid=False,
            allow_out_of_bounds=False,
            camera_name="SearchLevelVirtualCamera",
            viewport_name="SearchLevelViewport",
        )

    def _setupVirtualArea(self):
        # create hotspot to handle VA
        self.va_hotspot = Mengine.createNode("HotSpotPolygon")
        self.va_hotspot.setName(self.__class__.__name__ + "_" + "VirtualAreaSocket")

        hotspot_polygon = [
            (self.box_points.x, self.box_points.y),
            (self.box_points.z, self.box_points.y),
            (self.box_points.z, self.box_points.w),
            (self.box_points.x, self.box_points.w)
        ]
        hotspot_polygon_center = Mengine.vec2f(
            -((self.box_points.z - self.box_points.x) / 2 + self.box_points.x),
            -((self.box_points.w - self.box_points.y) / 2 + self.box_points.y)
        )

        self.va_hotspot.setPolygon(hotspot_polygon)
        self.va_hotspot.setDefaultHandle(False)

        self.root.addChild(self.va_hotspot)
        self.va_hotspot.enable()
        self.va_hotspot.setLocalPosition(hotspot_polygon_center)

        # set hotspot to VA
        self.virtual_area.setup_viewport(self.box_points.x, self.box_points.y, self.box_points.z, self.box_points.w)
        self.virtual_area.init_handlers(self.va_hotspot)
        self.virtual_area.set_content_size(self.box_points.x, self.box_points.y, self.box_points.z, self.box_points.w)

        # attach VA to root
        virtual_area_node = self.virtual_area.get_node()
        self.root.addChild(virtual_area_node)
        virtual_area_node.setLocalPosition(hotspot_polygon_center)

    # - Scene ----------------------------------------------------------------------------------------------------------

    def _attachScene(self):
        current_level_params = GameManager.getCurrentGameParams()
        scene_group_name = current_level_params.GroupName
        scene_group = GroupManager.getGroup(scene_group_name)

        scene = scene_group.getScene()
        scene_node = scene.getParent()
        self.virtual_area.add_node(scene_node)
        self.virtual_area.update_target()

        scene.enable()

        scene_layer = scene_group.getMainLayer()
        scene_size = scene_layer.getSize()
        box_size = self.getSize()

        # WORKING WRONG, BUT WHY?
        # scene_node.setLocalPosition(Mengine.vec2f(box_size.x / 2 - scene_size.x / 2, box_size.y / 2 - scene_size.y / 2))

        _, _, header_y, _, _, _, _ = AdjustableScreenUtils.getMainSizesExt()
        diff = box_size.y - scene_size.y
        pos_y = header_y + diff / 2
        scene_node.setLocalPosition(Mengine.vec2f(0, pos_y))

    def getSize(self):
        box_width = self.box_points.z - self.box_points.x
        box_height = self.box_points.w - self.box_points.y
        return Mengine.vec2f(box_width, box_height)

    # - Items ----------------------------------------------------------------------------------------------------------

    def _fillItems(self):
        randomizer = GameManager.getRandomizer()

        current_level_params = GameManager.getCurrentGameParams()
        level_group_name = current_level_params.GroupName
        level_items_count = current_level_params.ItemsCount
        level_quest_item_name = current_level_params.QuestItem

        level_group = GroupManager.getGroup(level_group_name)
        level_group_objects = level_group.getObjects()
        level_items = [obj for obj in level_group_objects if
                       obj.getEntityType() == "Item" and
                       obj not in self.game.FoundItems]

        random_index = randomizer.getRandom(level_items_count)
        for i in range(level_items_count):
            level_items_len = len(level_items)
            level_item_index = randomizer.getRandom(level_items_len)
            level_item = level_items[level_item_index]

            if level_quest_item_name is not None:
                quest_item = level_group.getObject(level_quest_item_name)
                if quest_item not in self.items and i == random_index:
                    level_item = quest_item
                    level_quest_item_name = None

            level_items.remove(level_item)
            self.items.append(level_item)

            level_item.setEnable(True)

        for item in level_items:
            item.setEnable(False)
