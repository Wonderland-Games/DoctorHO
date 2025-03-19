from Foundation.Initializer import Initializer
from UIKit.Managers.PrototypeManager import PrototypeManager


PROTOTYPE_CARD = "LevelCard"
SLOT_LEVEL = "Level"


class LevelCard(Initializer):
    def __init__(self):
        super(LevelCard, self).__init__()
        self.level_name = None
        self.root = None
        self.button = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, level_name):
        super(LevelCard, self)._onInitialize()
        self.level_name = level_name

        self._createRoot()
        self._setupButton()

    def _onFinalize(self):
        super(LevelCard, self)._onFinalize()

        if self.button is not None:
            self.button.onDestroy()
            self.button = None

        if self.root is not None:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

        self.level_name = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__ + "_" + self.level_name)

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    def setLocalPosition(self, pos):
        self.root.setLocalPosition(pos)

    def getRoot(self):
        return self.root

    # - Button ---------------------------------------------------------------------------------------------------------

    def _setupButton(self):
        self.button = PrototypeManager.generateObjectUniqueOnNode(self.root, PROTOTYPE_CARD, PROTOTYPE_CARD)
        self.button.setEnable(True)

    def getSize(self):
        button_bounds = self.button.getCompositionBounds()
        button_size = Utils.getBoundingBoxSize(button_bounds)
        return button_size
