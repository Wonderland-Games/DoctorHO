from Foundation.Initializer import Initializer


class FinalStageAttachItem(Initializer):
    SCALE = 0.312500071526

    def __init__(self):
        super(FinalStageAttachItem, self).__init__()
        self.root = None
        self.sprite_object = None
        self.sprite = None

    def _onInitialize(self, sprite_object):
        self.sprite_object = sprite_object
        self.sprite = self.sprite_object.entity.getSprite()

        self._createSpriteNode()
        self._setupSprite()
        self._scaleSprite()
        self._positionSprite()

    def _onFinalize(self):
        if self.sprite is not None and self.sprite_object.isDestroy() is False:
            self.sprite_object.onDestroy()
            self.sprite_object = None
            self.sprite = None

        if self.root is not None:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

    def getRoot(self):
        return self.root

    def getSpriteScale(self):
        return self.sprite.getWorldScale()

    def getSprite(self):
        return self.sprite

    def _createSpriteNode(self):
        self.root = Mengine.createNode("Interender")
        sprite_name = self.sprite_object.getName()
        self.root.setName(sprite_name)

    def _setupSprite(self):
        self.root.addChild(self.sprite)
        self.sprite.enable()

    def _scaleSprite(self):
        self.sprite.setScale((self.SCALE, self.SCALE))

    def _positionSprite(self):
        sprite_size_base = self.sprite.getSurfaceSize()
        sprite_size_scaled = Mengine.vec2f(sprite_size_base.x * self.SCALE, sprite_size_base.y * self.SCALE)
        sprite_position = Mengine.vec2f(-(sprite_size_scaled.x * 0.5), -(sprite_size_scaled.y * 0.5))
        self.sprite.setLocalPosition(sprite_position)

    def setSpriteEnable(self, source, value):
        if value is True:
            source.addFunction(self.sprite.enable)
        else:
            source.addFunction(self.sprite.disable)

    def getNodeCenter(self):
        point = self.sprite.getLocalPosition()
        size = self.sprite.getSurfaceSize()
        point.x += size.x / 2
        point.y += size.y / 2
        return point
