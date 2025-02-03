from Foundation.Initializer import Initializer


MOVIE_BOX = "Movie2_ItemBox"


class Item(Initializer):
    def __init__(self):
        super(Item, self).__init__()
        self.root = None
        self.game = None
        self.item_obj = None
        self.sprite = None
        self.box = None

    def _onInitialize(self, game, item_obj):
        self.game = game
        self.item_obj = item_obj

        self._createRoot()

        self._createBox()

        self._createSprite()
        self._scaleSprite()
        self._positionSprite()

    def _onFinalize(self):
        self.game = None
        self.item_obj = None

        if self.sprite is not None:
            self.sprite.removeFromParent()
            Mengine.destroyNode(self.sprite)
            self.sprite = None

        if self.box is not None:
            self.box.getEntityNode().removeFromParent()
            self.box.onDestroy()
            self.box = None

        if self.root is not None:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__)

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    def setLocalPositionX(self, position):
        curr_position = self.root.getLocalPosition()
        self.root.setLocalPosition(Mengine.vec2f(position, curr_position.y))

    def _createBox(self):
        self.box = self.game.object.generateObjectUnique(MOVIE_BOX, MOVIE_BOX)
        self.box.setEnable(True)
        self.root.addChild(self.box.getEntityNode())

    def getSize(self):
        box_bounds = self.box.getCompositionBounds()
        box_size = Utils.getBoundingBoxSize(box_bounds)
        return box_size

    def _createSprite(self):
        self.sprite = self.item_obj.getEntity().generatePure()
        self.root.addChild(self.sprite)

    def _scaleSprite(self):
        if self.box is None:
            return

        box_size = self.getSize()
        box_size_max = max(box_size.x, box_size.y)

        sprite_size = self.sprite.getSurfaceSize()
        sprite_size_max = max(sprite_size.x, sprite_size.y)

        scale_perc = box_size_max/sprite_size_max
        self.sprite.setScale(Mengine.vec2f(scale_perc, scale_perc))

    def _positionSprite(self):
        sprite_scale = self.sprite.getScale()
        sprite_size_base = self.sprite.getSurfaceSize()
        sprite_size_scaled = Mengine.vec2f(sprite_size_base.x * sprite_scale.x, sprite_size_base.y * sprite_scale.y)
        sprite_position = Mengine.vec2f(-(sprite_size_scaled.x * 0.5), -(sprite_size_scaled.y * 0.5))
        self.sprite.setLocalPosition(sprite_position)
