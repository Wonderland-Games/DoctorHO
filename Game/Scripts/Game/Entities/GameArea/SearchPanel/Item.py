from Foundation.Initializer import Initializer
from UIKit.Managers.PrototypeManager import PrototypeManager


PROTOTYPE_BOX = "ItemBox"
ITEM_SCALE_MULTIPLIER = 0.8

ITEM_REMOVE_SCALE_UP_TO = Mengine.vec3f(1.15, 1.15, 1.15)
ITEM_REMOVE_SCALE_UP_TIME = 100.0
ITEM_REMOVE_SCALE_DOWN_TO = Mengine.vec3f(0.0, 0.0, 0.0)
ITEM_REMOVE_SCALE_DOWN_TIME = 200.0
ITEM_REMOVE_ALPHA_TO = 0.0
ITEM_REMOVE_ALPHA_TIME = 150.0


class Item(Initializer):
    def __init__(self):
        super(Item, self).__init__()
        self._root = None
        self.game = None
        self.item_obj = None
        self.sprite_node = None
        self.sprite = None
        self.box = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game, item_obj):
        self.game = game
        self.item_obj = item_obj

        self._createRoot()
        self._createBox()
        self._createSpriteNode()
        self._createSprite()
        self._scaleSprite()
        self._positionSprite()

    def _onFinalize(self):
        if self.sprite is not None:
            self.sprite.removeFromParent()
            Mengine.destroyNode(self.sprite)
            self.sprite = None

        if self.sprite_node is not None:
            self.sprite_node.removeFromParent()
            Mengine.destroyNode(self.sprite_node)
            self.sprite_node = None

        if self.box is not None:
            self.box.getEntityNode().removeFromParent()
            self.box.onDestroy()
            self.box = None

        if self._root is not None:
            self._root.removeFromParent()
            Mengine.destroyNode(self._root)
            self._root = None

        self.item_obj = None
        self.game = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self._root = Mengine.createNode("Interender")
        root_name = self.item_obj.getName()
        self._root.setName(root_name)

    def attachTo(self, node):
        self._root.removeFromParent()
        node.addChild(self._root)

    def getRoot(self):
        return self._root

    def getRootWorldPosition(self):
        node_screen_position = Mengine.getNodeScreenAdaptPosition(self._root)

        panel_pos = self.game.search_panel.getRoot().getWorldPosition()
        panel_size = self.game.search_panel.getSize()

        world_position_x = (panel_pos.x - panel_size.x/2) + panel_size.x * node_screen_position.x
        world_position_y = (panel_pos.y - panel_size.y/2) + panel_size.y * node_screen_position.y
        world_position = Mengine.vec2f(world_position_x, world_position_y)

        return world_position

    def setLocalPositionX(self, position):
        curr_position = self._root.getLocalPosition()
        self._root.setLocalPosition(Mengine.vec2f(position, curr_position.y))

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

    def _createSpriteNode(self):
        self.sprite_node = Mengine.createNode("Interender")
        self.sprite_node.setName("SpriteNode")
        self._root.addChild(self.sprite_node)

    def _createSprite(self):
        self.sprite = self.item_obj.getEntity().generatePure()
        self.sprite_node.addChild(self.sprite)

    def _scaleSprite(self):
        if self.box is None:
            return

        box_size = self.getSize()
        box_size_max = max(box_size.x, box_size.y)

        sprite_size = self.sprite.getSurfaceSize()
        sprite_size_max = max(sprite_size.x, sprite_size.y)

        scale_perc = (box_size_max/sprite_size_max) * ITEM_SCALE_MULTIPLIER
        self.sprite.setScale(Mengine.vec2f(scale_perc, scale_perc))

    def getSpriteScale(self):
        return self.sprite.getScale()

    def _positionSprite(self):
        sprite_scale = self.sprite.getScale()
        sprite_size_base = self.sprite.getSurfaceSize()
        sprite_size_scaled = Mengine.vec2f(sprite_size_base.x * sprite_scale.x, sprite_size_base.y * sprite_scale.y)
        sprite_position = Mengine.vec2f(-(sprite_size_scaled.x * 0.5), -(sprite_size_scaled.y * 0.5))
        self.sprite.setLocalPosition(sprite_position)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def playItemDestroyAnim(self, source):
        source.addPrint(" * START REMOVE ITEM ANIM")

        source.addTask("TaskNodeScaleTo", Node=self.sprite_node, To=ITEM_REMOVE_SCALE_UP_TO, Time=ITEM_REMOVE_SCALE_UP_TIME)

        with source.addParallelTask(2) as (scale, alpha):
            scale.addTask("TaskNodeScaleTo", Node=self._root, To=ITEM_REMOVE_SCALE_DOWN_TO, Time=ITEM_REMOVE_SCALE_DOWN_TIME)
            alpha.addTask("TaskNodeAlphaTo", Node=self._root, To=ITEM_REMOVE_ALPHA_TO, Time=ITEM_REMOVE_ALPHA_TIME)

        source.addPrint(" * END REMOVE ITEM ANIM")
