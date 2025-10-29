from Foundation.Initializer import Initializer
from Foundation.GroupManager import GroupManager
from Foundation.SceneManager import SceneManager
from Foundation.DefaultManager import DefaultManager
from Foundation.Entities.MovieVirtualArea.VirtualArea import VirtualArea
from Game.Managers.GameManager import GameManager
from Game.Entities.GameArea.SearchLevel.MissClick import MissClick
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils


HARDCODED_LEVEL_WIDTH = 1170.0  # 9:19.5 aspect ratio game width
HARDCODED_LEVEL_HEIGHT = 1750.0  # 9:16 aspect ratio free space (game height - header - search panel - banner - 34.5)
LEVEL_ZONES = "LevelZones"


class SearchLevel(Initializer):
    def __init__(self):
        super(SearchLevel, self).__init__()
        self.game = None
        self.root = None
        self.virtual_area = None
        self.va_hotspot = None
        self.box_points = None
        self.items = []
        self.miss_click = None

        self.level_group = None
        self.level_size = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game):
        self.game = game

        self._createRoot()

        self._defineLevelGroup()
        self._calculateSize()
        self._defineBoxBoints()

        self._initVirtualArea()

        self._setupMissClick()
        self._setupVirtualArea()
        self._attachScene()
        self._attachLevelZones()
        self._fillItems()
        return True

    def _onFinalize(self):
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

        if self.miss_click is not None:
            self.miss_click.onFinalize()
            self.miss_click = None

        self.game = None
        self.box_points = None
        self.items = []

        self.level_group = None
        self.level_size = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__)

    def getRoot(self):
        return self.root

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    # - Miss Click -----------------------------------------------------------------------------------------------------

    def _setupMissClick(self):
        self.miss_click = MissClick()
        self.miss_click.onInitialize(self.game, self.box_points)
        self.miss_click.attachTo(self.root)

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
            content_size=(self.box_points.x, self.box_points.y, self.box_points.z, self.box_points.w),
            viewport=(self.box_points.x, self.box_points.y, self.box_points.z, self.box_points.w),
        )

    def _setupVirtualArea(self):
        # calculate hotspot polygon and center
        hotspot_polygon = [
            (self.box_points.x, self.box_points.y),
            (self.box_points.z, self.box_points.y),
            (self.box_points.z, self.box_points.w),
            (self.box_points.x, self.box_points.w)
        ]
        hotspot_polygon_center = (
            -((self.box_points.z - self.box_points.x) / 2 + self.box_points.x),
            -((self.box_points.w - self.box_points.y) / 2 + self.box_points.y)
        )

        # attach VA to root
        virtual_area_node = self.virtual_area.get_node()
        self.root.addChild(virtual_area_node)
        virtual_area_node.setLocalPosition(hotspot_polygon_center)

        # create hotspot to handle VA
        self.va_hotspot = Mengine.createNode("HotSpotPolygon")
        self.va_hotspot.setName(self.__class__.__name__ + "_" + "VirtualAreaSocket")

        self.va_hotspot.setPolygon(hotspot_polygon)
        self.va_hotspot.setDefaultHandle(False)

        # set hotspot to VA
        self.virtual_area.init_handlers(self.va_hotspot)

        # attach VA hotspot to root
        self.root.addChild(self.va_hotspot)
        self.va_hotspot.enable()
        self.va_hotspot.setLocalPosition(hotspot_polygon_center)

    # - Scene ----------------------------------------------------------------------------------------------------------

    def _defineLevelGroup(self):
        level_id = GameManager.getCurrentGameParam("LevelId")
        level_params = GameManager.getLevelParams(level_id)
        # level_group_name = level_params.GroupName # old way to get level group name
        level_scene_name = level_params.SceneName
        level_group_name = SceneManager.getSceneMainGroupName(level_scene_name)
        self.level_group = GroupManager.getGroup(level_group_name)

    def _calculateSize(self):
        level_group_main_layer = self.level_group.getMainLayer()
        level_group_main_layer_size = level_group_main_layer.getSize()

        game_width = AdjustableScreenUtils.getGameWidth()
        # game_height = AdjustableScreenUtils.getGameHeight()

        self.level_size = Mengine.vec2f(
            # min(game_width,  level_group_main_layer_size.x),
            # min(game_height, level_group_main_layer_size.y)
            HARDCODED_LEVEL_WIDTH,
            HARDCODED_LEVEL_HEIGHT  # hardcoded for now, because of the game design
        )

    def _defineBoxBoints(self):
        self.box_points = Mengine.vec4f(0, 0, self.level_size.x, self.level_size.y)

    def _attachScene(self):
        scene = self.level_group.getScene()
        scene_node = scene.getParent()

        self.virtual_area.add_node(scene_node)

        level_size = self.getSize()
        scene_main_layer = self.level_group.getMainLayer()
        scene_size = scene_main_layer.getSize()

        offset_x = (level_size.x - scene_size.x) / 2
        offset_y = (level_size.y - scene_size.y) / 2

        scene_node.setLocalPosition((offset_x, offset_y))

        scene.enable()

    def _attachLevelZones(self):
        checks = [
            _DEVELOPMENT,
            GroupManager.hasGroup(LEVEL_ZONES),
            GroupManager.hasObject(LEVEL_ZONES, "Sprite_{}".format(LEVEL_ZONES)),
        ]
        if not all(checks):
            return

        level_zones_sprite = GroupManager.getObject(LEVEL_ZONES, "Sprite_{}".format(LEVEL_ZONES))
        level_zones_sprite_node = level_zones_sprite.getEntityNode()

        self.virtual_area.add_node(level_zones_sprite_node)

        level_size = self.getSize()
        scene_main_layer = self.level_group.getMainLayer()
        scene_size = scene_main_layer.getSize()

        offset_x = (level_size.x - scene_size.x) / 2
        offset_y = (level_size.y - scene_size.y) / 2

        level_zones_sprite_node.setLocalPosition((offset_x, offset_y))

    def getSize(self):
        return self.level_size

    # - Items ----------------------------------------------------------------------------------------------------------

    def _fillItems(self):
        randomizer = GameManager.getRandomizer()

        chapter_id = GameManager.getCurrentGameParam("ChapterId")
        quest_index = GameManager.getCurrentGameParam("QuestIndex")
        if quest_index is not None:
            quest_params = GameManager.getQuestParamsWithChapterIdAndQuestIndex(chapter_id, quest_index)
            items_count = quest_params.ItemsCount
            quest_item_name = quest_params.QuestItem
        else:
            items_count = None
            quest_item_name = None

        level_group_objects = self.level_group.getObjects()

        if quest_item_name is not None:
            level_items = [obj for obj in level_group_objects if
                           obj.getEntityType() == "Item" and
                           obj not in self.game.FoundItems]
        else:
            level_items = [obj for obj in level_group_objects if
                           obj.getEntityType() == "Item" and
                           obj not in self.game.FoundItems and
                           "Quest" not in obj.getName()]

            quest_items = [obj for obj in level_group_objects if
                           "Quest" in obj.getName()]
            for item in quest_items:
                item.setEnable(False)

        for item in level_items:
            item.setEnable(False)

        if items_count is None:
            level_items_len = len(level_items)
            items_count = randomizer.getRandomRange(5, level_items_len)

        quest_item_random_index = randomizer.getRandom(items_count)
        for i in range(items_count):
            level_items_len = len(level_items)
            level_item_index = randomizer.getRandom(level_items_len)
            level_item = level_items[level_item_index]

            if quest_item_name is not None:
                quest_item = self.level_group.getObject(quest_item_name)
                if quest_item not in self.items and i == quest_item_random_index:
                    level_item = quest_item
                    quest_item_name = None

            level_item.setEnable(True)

            level_items.remove(level_item)
            self.items.append(level_item)
