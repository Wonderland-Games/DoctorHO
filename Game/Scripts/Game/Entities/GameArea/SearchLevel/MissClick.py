from Foundation.Initializer import Initializer


class MissClick(Initializer):
    def __init__(self):
        super(MissClick, self).__init__()
        self.root = None
        self.game = None
        self.hotspot_points = None
        self.miss_click_hotspot = None
        self.miss_click_data = {}

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game, hotspot_points):
        super(MissClick, self)._onInitialize()
        self.game = game
        self.hotspot_points = hotspot_points

        self._createRoot()
        self._setupMissClickHotSpot()

        return True

    def _onFinalize(self):
        super(MissClick, self)._onFinalize()

        if self.miss_click_hotspot is not None:
            self.miss_click_hotspot.removeFromParent()
            Mengine.destroyNode(self.miss_click_hotspot)
            self.miss_click_hotspot = None

        if self.root is not None:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

        self.game = None
        self.hotspot_points = None
        self.miss_click_data = {}

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__)

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    def getRoot(self):
        return self.root

    # - HotSpot --------------------------------------------------------------------------------------------------------

    def _setupMissClickHotSpot(self):
        # create hotspot to handle miss clicks
        self.miss_click_hotspot = Mengine.createNode("HotSpotPolygon")
        self.miss_click_hotspot.setName(self.__class__.__name__ + "_" + "HotSpot")

        hotspot_polygon = [
            (self.hotspot_points.x, self.hotspot_points.y),
            (self.hotspot_points.z, self.hotspot_points.y),
            (self.hotspot_points.z, self.hotspot_points.w),
            (self.hotspot_points.x, self.hotspot_points.w)
        ]
        hotspot_polygon_center = Mengine.vec2f(
            -((self.hotspot_points.z - self.hotspot_points.x) / 2 + self.hotspot_points.x),
            -((self.hotspot_points.w - self.hotspot_points.y) / 2 + self.hotspot_points.y)
        )

        self.miss_click_hotspot.setPolygon(hotspot_polygon)

        self.root.addChild(self.miss_click_hotspot)
        self.miss_click_hotspot.enable()
        self.miss_click_hotspot.setLocalPosition(hotspot_polygon_center)

        self.miss_click_hotspot.setEventListener(onHandleMouseButtonEvent=self._onMissClickButtonEvent)

    def _onMissClickButtonEvent(self, touchId, x, y, button, pressure, isDown, isPressed):
        last_click_data = self.miss_click_data
        self.miss_click_data = {
            "x": x,
            "y": y,
        }

        if self.game.search_panel.hint.hint_item is not None:
            return False

        if touchId != Mengine.TC_TOUCH0:
            return False

        if button != 0 or isDown is True:
            return False

        if len(last_click_data) != 0:
            if x != last_click_data["x"] or y != last_click_data["y"]:
                return False

            Notification.notify(Notificator.onLevelMissClicked)

        return False
