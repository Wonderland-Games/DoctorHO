from Foundation.Initializer import Initializer
from Game.Managers.GameManager import GameManager

ITEM_SCALE_MODIFIER = 0.75

class QuestItem(Initializer):
    STATE_BLOCKED = 0
    STATE_ACTIVE = 1

    def __init__(self):
        super(QuestItem, self).__init__()
        self.item_name = None
        self.item_sprite = None
        self.hotspot = None
        self.root = None
        self.state = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, quest_item_name, state=STATE_BLOCKED):
        super(QuestItem, self)._onInitialize()
        self.item_name = quest_item_name

        self.state = state
        if self.state is self.STATE_BLOCKED:
            return

        self._createRoot()
        self._setupItemSprite()
        self._setupHotspot()

    def _onFinalize(self):
        super(QuestItem, self)._onFinalize()

        if self.hotspot is not None:
            Mengine.destroyNode(self.hotspot)
            self.hotspot = None

        if self.item_sprite is not None:
            Mengine.destroyNode(self.item_sprite)
            self.item_sprite = None

        if self.root is not None:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

        self.item_name = None
        self.state = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__ + "_" + str(self.item_name))

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    def setLocalPosition(self, pos):
        self.root.setLocalPosition(pos)

    def getRoot(self):
        return self.root

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupItemSprite(self):
        self.item_sprite = GameManager.generateQuestItemNode(self.item_name)
        self.root.addChild(self.item_sprite)

        item_sprite_center = self.item_sprite.getLocalImageCenter()
        self.item_sprite.setScale((ITEM_SCALE_MODIFIER, ITEM_SCALE_MODIFIER, 1.0))
        self.item_sprite.setLocalPosition(Mengine.vec2f(-item_sprite_center[0] * ITEM_SCALE_MODIFIER,
                                                        -item_sprite_center[1] * ITEM_SCALE_MODIFIER))

    def _setupHotspot(self):
        hotspot_name = self.item_name + "_HotSpot"
        self.hotspot = Utils.createBBSpriteHotspot(hotspot_name, self.item_sprite)
        self.root.addChild(self.hotspot)

        item_sprite_center = self.item_sprite.getLocalImageCenter()
        self.hotspot.setScale((ITEM_SCALE_MODIFIER, ITEM_SCALE_MODIFIER, 1.0))
        self.hotspot.setLocalPosition(Mengine.vec2f(-item_sprite_center[0] * ITEM_SCALE_MODIFIER,
                                                    -item_sprite_center[1] * ITEM_SCALE_MODIFIER))

        self.hotspot.setEventListener(onHandleMouseButtonEvent=self._onClick)

    # - State ----------------------------------------------------------------------------------------------------------

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    # - Utils ----------------------------------------------------------------------------------------------------------

    def _onClick(self, context, event):
        if event.touchId != Mengine.TC_TOUCH0:
            return False

        if event.button != 0 or event.isDown is not False:
            return False

        Notification.notify(Notificator.onQuestItemClicked, self.item_name)

        return False
