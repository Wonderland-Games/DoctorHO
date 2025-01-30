from Foundation.Initializer import Initializer


class Item(Initializer):
    def __init__(self):
        super(Item, self).__init__()
        self.root = None
        self.sprite = None

    def _onInitialize(self, item_obj):
        self._createRoot()

        self.sprite = item_obj.getEntity().generatePure()
        self.root.addChild(self.sprite)
        sprite_center = item_obj.getEntity().getSpriteCenter()
        self.sprite.setLocalPosition(Mengine.vec2f(-sprite_center[0], -sprite_center[1]))

    def _onFinalize(self):
        if self.root is not None:
            Mengine.destroyNode(self.root)
            self.root = None

        if self.sprite is not None:
            self.sprite.removeFromParent()
            Mengine.destroyNode(self.sprite)
            self.sprite = None

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__)

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)
