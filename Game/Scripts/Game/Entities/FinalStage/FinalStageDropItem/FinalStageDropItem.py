from Foundation.Initializer import Initializer
from UIKit.Managers.PrototypeManager import PrototypeManager


PROTOTYPE_BOX = "ItemBox"
ITEM_SCALE_MULTIPLIER = 0.95

ITEM_REMOVE_SCALE_UP_TO = Mengine.vec3f(1.15, 1.15, 1.15)
ITEM_REMOVE_SCALE_UP_TIME = 100.0
ITEM_REMOVE_SCALE_DOWN_TO = Mengine.vec3f(0.0, 0.0, 0.0)
ITEM_REMOVE_SCALE_DOWN_TIME = 200.0
ITEM_REMOVE_ALPHA_TO = 0.0
ITEM_REMOVE_ALPHA_TIME = 150.0
ITEM_ADD_ALPHA_TO = 1.0

ITEM_CREATE_SCALE_FROM = Mengine.vec3f(0.0, 0.0, 0.0)
ITEM_CREATE_SCALE_TO = Mengine.vec3f(1.0, 1.0, 1.0)
ITEM_CREATE_SCALE_TIME = 200.0

ITEM_CREATE_ALPHA_FROM = 0.0
ITEM_CREATE_ALPHA_TO = 1.0
ITEM_CREATE_ALPHA_TIME = 150.0


class FinalStageDropItem(Initializer):
    def __init__(self):
        super(FinalStageDropItem, self).__init__()
        self._root = None
        self.panel = None
        self.sprite_object = None
        self.sprite = None
        self.box = None
        self.socket_node = None
        self.default_scale = None
        self.movie_info = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, panel, sprite_object, movie_info=None):
        self.panel = panel
        self.sprite_object = sprite_object
        self.sprite = self.sprite_object.entity.getSprite()
        self.movie_info = movie_info

        self._createRoot()
        self._createBox()
        self._setupSprite()
        self._createHotSpotPolygon()
        self._scaleSprite()
        self._positionSprite()

    def _onFinalize(self):
        if self.sprite is not None and self.sprite_object.isDestroy() is False:
            self.sprite_object.onDestroy()
            self.sprite_object = None
            self.sprite = None

        if self.box is not None:
            self.box.getEntityNode().removeFromParent()
            self.box.onDestroy()
            self.box = None

        if self._root is not None:
            self._root.removeFromParent()
            Mengine.destroyNode(self._root)
            self._root = None

        if self.socket_node is not None:
            self.socket_node.removeFromParent()
            Mengine.destroyNode(self.socket_node)
            self.socket_node = None

        self.panel = None
        self.default_scale = None
        self.movie_info = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self._root = Mengine.createNode("Interender")
        root_name = self.sprite.getName()
        self._root.setName(root_name)

    def attachTo(self, node):
        self._root.removeFromParent()
        node.addChild(self._root)

    def getRoot(self):
        return self._root

    def getSocket(self):
        return self.socket_node

    def getMovieInfo(self):
        return self.movie_info

    def getQuestItemName(self):
        sprite_object_name_raw = self.sprite_object.getName()
        sprite_object_name = sprite_object_name_raw.replace("Sprite_", "")
        return sprite_object_name

    def getRootWorldPosition(self):
        node_screen_position = Mengine.getNodeScreenAdaptPosition(self._root)

        # panel here is FinalStage; use its DropPanel for size/position
        panel_root = self.panel.drop_panel.getRoot()
        panel_size = self.panel.drop_panel.getSize()
        panel_pos = panel_root.getWorldPosition()

        world_position_x = (panel_pos.x - panel_size.x/2) + panel_size.x * node_screen_position.x
        world_position_y = (panel_pos.y - panel_size.y/2) + panel_size.y * node_screen_position.y
        world_position = Mengine.vec2f(world_position_x, world_position_y)

        return world_position

    def setLocalPositionX(self, position):
        curr_position = self._root.getLocalPosition()
        self._root.setLocalPosition(Mengine.vec2f(position, curr_position.y))

    def getLocalPosition(self):
        return self._root.getLocalPosition()

    # - Box ------------------------------------------------------------------------------------------------------------

    def _createBox(self):
        self.box = PrototypeManager.generateObjectUnique(PROTOTYPE_BOX)
        self.box.setEnable(True)
        self._root.addChild(self.box.getEntityNode())

    def getSize(self):
        box_bounds = self.box.getCompositionBounds()
        box_size = Utils.getBoundingBoxSize(box_bounds)
        return box_size

    # - Sprite ---------------------------------------------------------------------------------------------------------

    def _setupSprite(self):
        self._root.addChild(self.sprite)
        self.sprite.enable()

    def _createHotSpotPolygon(self):
        self.socket_node = Mengine.createNode("HotSpotPolygon")
        self.socket_node.setName("Socket_{}".format(self.sprite_object.getName()))

        width, height = self.getSize()[0], self.getSize()[1]
        hw, hh = width / 2, height / 2

        self.socket_node.setPolygon([
            (-hw, -hh), (hw, -hh),
            (hw, hh), (-hw, hh),
        ])

        # Attach socket to root node (same parent as sprite and box) so that
        # its size matches the box and is not additionally affected by sprite scaling.
        self._root.addChild(self.socket_node)

    def _scaleSprite(self):
        if self.box is None:
            return

        box_size = self.getSize()
        box_size_max = max(box_size.x, box_size.y)

        #sprite_scale = self._getSpriteScale()
        #self.item_sprite.setScale(sprite_scale)
        #sprite_size = self._getSpriteSize()

        sprite_size = self.sprite.getSurfaceSize()
        sprite_size_max = max(sprite_size.x, sprite_size.y)

        scale_perc = (box_size_max / sprite_size_max) * ITEM_SCALE_MULTIPLIER
        self.default_scale = scale_perc
        self.sprite.setScale((scale_perc, scale_perc))
        #self.socket_node.setScale((scale_perc, scale_perc))

    def getSpriteScale(self):
        return self.sprite.getWorldScale()

    def getDefaultSpriteScale(self):
        return self.default_scale

    def getSprite(self):
        return self.sprite

    def _positionSprite(self):
        sprite_scale = self.sprite.getScale()
        sprite_size_base = self.sprite.getSurfaceSize()
        sprite_size_scaled = Mengine.vec2f(sprite_size_base.x * sprite_scale.x, sprite_size_base.y * sprite_scale.y)
        sprite_position = Mengine.vec2f(-(sprite_size_scaled.x * 0.5), -(sprite_size_scaled.y * 0.5))
        self.sprite.setLocalPosition(sprite_position)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def playItemDestroyAnim(self, source):
        source.addPrint(" * START REMOVE ITEM ANIM")

        # scale up sprite slightly relative to its current local scale (works even if parent scale changes)
        current_scale = self.sprite.getScale()
        up_scale = Mengine.vec3f(
            current_scale.x * ITEM_REMOVE_SCALE_UP_TO.x,
            current_scale.y * ITEM_REMOVE_SCALE_UP_TO.y,
            current_scale.z * ITEM_REMOVE_SCALE_UP_TO.z,
        )

        source.addTask("TaskNodeScaleTo", Node=self.sprite, To=up_scale, Time=ITEM_REMOVE_SCALE_UP_TIME)

        with source.addParallelTask(2) as (scale, alpha):
            scale.addTask("TaskNodeScaleTo", Node=self._root, To=ITEM_REMOVE_SCALE_DOWN_TO, Time=ITEM_REMOVE_SCALE_DOWN_TIME)
            alpha.addTask("TaskNodeAlphaTo", Node=self._root, To=ITEM_REMOVE_ALPHA_TO, Time=ITEM_REMOVE_ALPHA_TIME)

        source.addPrint(" * END REMOVE ITEM ANIM")

    def playItemCreateAnim(self, source):
        source.addPrint(" * START CREATE ITEM ANIM")

        with source.addParallelTask(2) as (scale, alpha):
            scale.addTask("TaskNodeScaleTo", Node=self._root, To=ITEM_CREATE_SCALE_TO, Time=ITEM_CREATE_SCALE_TIME)
            alpha.addTask("TaskNodeAlphaTo", Node=self._root, To=ITEM_CREATE_ALPHA_TO, Time=ITEM_CREATE_ALPHA_TIME)

        source.addPrint(" * END CREATE ITEM ANIM")

    def setSpriteEnable(self, source, value):
        if value is True:
            def _enable():
                # always restore sprite scale to default when we re-enable it
                if self.default_scale is not None:
                    self.sprite.setScale((self.default_scale, self.default_scale))
                self.sprite.enable()

            source.addFunction(_enable)
        else:
            source.addFunction(self.sprite.disable)
