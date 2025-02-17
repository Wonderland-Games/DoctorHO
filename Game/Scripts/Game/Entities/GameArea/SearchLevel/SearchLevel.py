from Foundation.Initializer import Initializer
from Foundation.GroupManager import GroupManager
from Foundation.DefaultManager import DefaultManager
from Foundation.Entities.MovieVirtualArea.VirtualArea import VirtualArea


class SearchLevel(Initializer):
    def __init__(self):
        super(SearchLevel, self).__init__()
        self.root = None
        self.virtual_area = None
        self.va_hotspot = None
        self.game = None
        self.level_name = None
        self.box_points = None
        self.items = []

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game, level_name, box_points):
        self.game = game
        self.level_name = level_name
        self.box_points = box_points

        self._initVirtualArea()

        self._createRoot()
        self._setupVirtualArea()
        self._attachScene()
        self._fillItems()
        return True

    def _onFinalize(self):
        self.game = None
        self.level_name = None
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
            dragging_mode="free",
            enable_scale=True,
            max_scale=DefaultManager.getDefaultFloat("TouchpadMaxScale", 2.0),
            scale_factor=scale_factor,
            disable_drag_if_invalid=False,
            allow_out_of_bounds=False
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
        scene_group = GroupManager.getGroup(self.level_name)

        scene = scene_group.getScene()
        scene_node = scene.getParent()
        self.virtual_area.add_node(scene_node)
        self.virtual_area.update_target()

        scene.enable()

        scene_layer = scene_group.getMainLayer()
        scene_size = scene_layer.getSize()
        box_size = self.getBoxSize()

        # WORKING WRONG, BUT WHY?
        # scene_node.setLocalPosition(Mengine.vec2f(box_size.x / 2 - scene_size.x / 2, box_size.y / 2 - scene_size.y / 2))

    def getBoxSize(self):
        box_width = self.box_points.z - self.box_points.x
        box_height = self.box_points.w - self.box_points.y
        return Mengine.vec2f(box_width, box_height)

    # - Items ----------------------------------------------------------------------------------------------------------

    def _fillItems(self):
        scene_group = GroupManager.getGroup(self.level_name)
        scene_objects = scene_group.getObjects()

        for obj in scene_objects:
            if obj.getEntityType() is not "Item":
                continue

            self.items.append(obj)
            obj.setEnable(True)
