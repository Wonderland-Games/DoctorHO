from Foundation.Initializer import Initializer
from Game.Managers.GameManager import GameManager


class FinalStageAttachItem(Initializer):
    def __init__(self):
        super(FinalStageAttachItem, self).__init__()
        self.root = None
        self.sprite = None
        self.item_name = None
        self.item_scale = None

    def _onInitialize(self, item_name, item_scale):
        self.item_name = item_name
        self.item_scale = item_scale

        self._createSpriteNode()
        self._setupSprite()
        self._scaleSprite()
        self._positionSprite()

    def _onFinalize(self):
        if self.sprite is not None:
            Mengine.destroyNode(self.sprite)
            self.sprite = None

        if self.root is not None:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

        self.item_name = None
        self.item_scale = None

    def getRoot(self):
        return self.root

    def getItemName(self):
        return self.item_name

    def getSpriteScale(self):
        return self.sprite.getWorldScale()

    def getSprite(self):
        return self.sprite

    def _createSpriteNode(self):
        self.root = Mengine.createNode("Interender")
        item_name = self.getItemName()
        self.root.setName(item_name)

    def _setupSprite(self):
        self.sprite = GameManager.generateQuestItemNode(self.getItemName())
        self.root.addChild(self.sprite)
        self.sprite.enable()

    def _scaleSprite(self):
        self.sprite.setScale(self.item_scale)

    def _getScaledSpriteSize(self):
        sprite_size_base = self.sprite.getSurfaceSize()
        return Mengine.vec2f(sprite_size_base.x * self.item_scale.x, sprite_size_base.y * self.item_scale.y)

    def _positionSprite(self):
        sprite_size_scaled = self._getScaledSpriteSize()
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
