from Foundation.Initializer import Initializer
from UIKit.Managers.PrototypeManager import PrototypeManager
from Game.Managers.LevelCardManager import LevelCardManager


PROTOTYPE_CARD = "LevelCard"
SLOT_LEVEL = "Level"
ALIAS_TITLE = "$LevelCardTitle"
TEXT_TITLE = "ID_LevelCardTitle"


class LevelCard(Initializer):
    def __init__(self):
        super(LevelCard, self).__init__()
        self.level_name = None
        self.root = None
        self.button = None
        self.level = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, level_name):
        super(LevelCard, self)._onInitialize()
        self.level_name = level_name

        self._createRoot()

        self._setupButton()
        self._setupLevel()
        self._setupTitle()

    def _onFinalize(self):
        super(LevelCard, self)._onFinalize()

        if self.level is not None:
            self.level.onDestroy()
            self.level = None

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

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupButton(self):
        self.button = PrototypeManager.generateObjectUniqueOnNode(self.root, PROTOTYPE_CARD, PROTOTYPE_CARD)
        self.button.setEnable(True)

    def _setupLevel(self):
        self.level = LevelCardManager.generateLevelCard(self.level_name)
        self.level.setEnable(True)

        level_node = self.level.getEntityNode()
        self.button.addChildToSlot(level_node, SLOT_LEVEL)

    def _setupTitle(self):
        env = PROTOTYPE_CARD + "_" + self.level_name
        title_id = TEXT_TITLE + "_" + self.level_name
        title_text = Mengine.getTextFromId(title_id)

        self.button.setTextAliasEnvironment(env)

        Mengine.setTextAlias(env, ALIAS_TITLE, TEXT_TITLE)
        Mengine.setTextAliasArguments(env, ALIAS_TITLE, title_text)

    # - Utils ----------------------------------------------------------------------------------------------------------

    def getSize(self):
        button_bounds = self.button.getCompositionBounds()
        button_size = Utils.getBoundingBoxSize(button_bounds)
        return button_size
