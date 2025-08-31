from Foundation.Initializer import Initializer

class SpriteNode(Initializer):
    SCALE = 0.312500071526
    def __init__(self):
        super(SpriteNode, self).__init__()
        self.item_obj = None
        self.root = None
        self.sprite = None

    def _onInitialize(self, item_obj):
        self.item_obj = item_obj
        self._createSpriteNode()
        self._createSprite()
        self._scaleSprite()
        self._positionSprite()

    def _onFinalize(self):
        self.item_obj = None

        if self.sprite is not None:
            self.sprite.removeFromParent()
            Mengine.destroyNode(self.sprite)
            self.sprite = None

        if self.root is not None:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

    def getObj(self):
        return self.item_obj
    def getRoot(self):
        return self.root

    def getSpriteScale(self):
        return self.sprite.getWorldScale()

    def getSprite(self):
        return self.sprite

    def _createSpriteNode(self):
        self.root = Mengine.createNode("Interender")
        sprite_name = self.item_obj.getName()
        self.root.setName(sprite_name)

    def _createSprite(self):
        self.sprite = self.item_obj.getEntity().generatePure()
        self.root.addChild(self.sprite)

    def _scaleSprite(self):
        self.sprite.setScale((self.SCALE, self.SCALE))

    def _positionSprite(self):
        sprite_size_base = self.sprite.getSurfaceSize()
        sprite_size_scaled = Mengine.vec2f(sprite_size_base.x * self.SCALE, sprite_size_base.y * self.SCALE)
        sprite_position = Mengine.vec2f(-(sprite_size_scaled.x * 0.5), -(sprite_size_scaled.y * 0.5))
        self.sprite.setLocalPosition(sprite_position)

    def setItemVisible(self, source, visible):
        item_alpha = 0.0

        if visible is True:
            item_alpha = 1.0

        source.addTask("TaskNodeAlphaTo", Node=self.sprite, To=item_alpha, Time=0.001)
