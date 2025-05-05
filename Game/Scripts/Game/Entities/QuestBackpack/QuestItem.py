from Foundation.Initializer import Initializer


ITEM_SCALE_MODIFIER = 0.75


class QuestItem(Initializer):
    STATE_BLOCKED = 0
    STATE_ACTIVE = 1

    def __init__(self):
        super(QuestItem, self).__init__()
        self.ref_item_entity = None
        self.item_sprite = None
        self.root = None
        self.state = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, ref_item_entity, state=STATE_BLOCKED):
        super(QuestItem, self)._onInitialize()
        self.ref_item_entity = ref_item_entity

        self.state = state
        if self.state is self.STATE_BLOCKED:
            return

        self._createRoot()
        self._setupItemSprite()

    def _onFinalize(self):
        super(QuestItem, self)._onFinalize()

        if self.item_sprite is not None:
            Mengine.destroyNode(self.item_sprite)
            self.item_sprite = None

        if self.root is not None:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

        self.ref_item_entity = None
        self.state = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        ref_item_name = self.ref_item_entity.getName()
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__ + "_" + str(ref_item_name))

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    def setLocalPosition(self, pos):
        self.root.setLocalPosition(pos)

    def getRoot(self):
        return self.root

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupItemSprite(self):
        self.item_sprite = self.ref_item_entity.generatePure()
        self.item_sprite.enable()

        self.root.addChild(self.item_sprite)
        item_sprite_center = self.ref_item_entity.getSpriteCenter()
        self.item_sprite.setScale((ITEM_SCALE_MODIFIER, ITEM_SCALE_MODIFIER, 1.0))
        self.item_sprite.setLocalPosition(Mengine.vec2f(-item_sprite_center[0] * ITEM_SCALE_MODIFIER,
                                                        -item_sprite_center[1] * ITEM_SCALE_MODIFIER))

    # - State ----------------------------------------------------------------------------------------------------------

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state
