from Foundation.Initializer import Initializer
from Foundation.GroupManager import GroupManager
from Foundation.SceneManager import SceneManager
from Foundation.DefaultManager import DefaultManager
from Foundation.Entities.MovieVirtualArea.VirtualArea import VirtualArea


HARDCODED_LEVEL_WIDTH = 1170.0  # 9:19.5 aspect ratio game width
HARDCODED_LEVEL_HEIGHT = 1750.0  # 9:16 aspect ratio free space (game height - header - search panel - banner - 34.5)


class DropLevel(Initializer):
    def __init__(self):
        super(DropLevel, self).__init__()
        self.root = None
        self.virtual_area = None
        self.va_hotspot = None
        self.box_points = None
        self.level_group = None
        self.level_size = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, scene_name):
        self._createRoot()

        self._defineLevelGroup(scene_name)
        self._calculateSize()
        self._defineBoxPoints()

        self._initVirtualArea()
        self._setupVirtualArea()
        self._attachScene()

        return True

    def _onFinalize(self):
        self.box_points = None

        if self.root:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

        if self.virtual_area:
            self.virtual_area.onFinalize()
            self.virtual_area = None

        if self.va_hotspot:
            self.va_hotspot.removeFromParent()
            Mengine.destroyNode(self.va_hotspot)
            self.va_hotspot = None

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

    # - VirtualArea ----------------------------------------------------------------------------------------------------

    def _initVirtualArea(self):
        if _DESKTOP is True:  # run on PC
            scale_factor = DefaultManager.getDefaultFloat("DesktopScaleFactor", 0.05)
        else:
            scale_factor = DefaultManager.getDefaultFloat("TouchpadScaleFactor", 0.005)

        self.virtual_area = VirtualArea()
        self.virtual_area.onInitialize(
            name="DropLevelVirtualArea",
            dragging_mode="free",
            enable_scale=True,
            max_scale=DefaultManager.getDefaultFloat("TouchpadMaxScale", 2.0),
            scale_factor=scale_factor,
            disable_drag_if_invalid=False,
            allow_out_of_bounds=False,
            camera_name="DropLevelVirtualCamera",
            viewport_name="DropLevelViewport",
            content_size=(self.box_points.x, self.box_points.y, self.box_points.z, self.box_points.w),
            viewport=(self.box_points.x, self.box_points.y, self.box_points.z, self.box_points.w),
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

    def _defineLevelGroup(self, scene_name):
        level_group_name = SceneManager.getSceneMainGroupName(scene_name)
        self.level_group = GroupManager.getGroup(level_group_name)

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

    def getSize(self):
        return self.level_size

    def _calculateSize(self):
        self.level_size = Mengine.vec2f(
            HARDCODED_LEVEL_WIDTH,
            HARDCODED_LEVEL_HEIGHT
        )

    def _defineBoxPoints(self):
        self.box_points = Mengine.vec4f(0, 0, self.level_size.x, self.level_size.y)
