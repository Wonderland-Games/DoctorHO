from Foundation.Initializer import Initializer
from UIKit.Managers.PrototypeManager import PrototypeManager


MOVIE_BG = "HintCounterBackground"
TEXT_ID = "ID_HintCounter"


class HintCounter(Initializer):
    def __init__(self):
        super(HintCounter, self).__init__()
        self.game = None
        self.count = None
        self.root = None
        self.background = None
        self.text = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game, count):
        super(HintCounter, self)._onInitialize()
        self.game = game
        self.count = count

        self._createRoot()

        self._setupBackground()
        self._setupText()

    def _onFinalize(self):
        super(HintCounter, self)._onFinalize()
        self.game = None
        self.count = None

        if self.text is not None:
            self.text.removeFromParent()
            Mengine.destroyNode(self.text)
            self.text = None

        if self.background is not None:
            self.background.onDestroy()
            self.background = None

        if self.root is not None:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__)

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    def setLocalPosition(self, pos):
        self.root.setLocalPosition(pos)

    # - Text -----------------------------------------------------------------------------------------------------------

    def _setupText(self):
        self.text = Mengine.createNode("TextField")
        self.text.setName(self.__class__.__name__)
        self.text.setVerticalCenterAlign()
        self.text.setHorizontalCenterAlign()
        self.text.setTextId(TEXT_ID)
        self.updateTextArgs()
        self.text.enable()

        self.root.addChild(self.text)

    def updateTextArgs(self, value=None):
        if value is None:
            value = self.count

        self.text.setTextFormatArgs(value)

    # - Background -----------------------------------------------------------------------------------------------------

    def _setupBackground(self):
        self.background = PrototypeManager.generateObjectUniqueOnNode(self.root, MOVIE_BG)
        self.background.setEnable(True)

    # - Tools ----------------------------------------------------------------------------------------------------------

    def decHintCount(self):
        if self.count <= 0:
            return

        self.count -= 1
        self.updateTextArgs()

    def incHintCount(self):
        self.count += 1
        self.updateTextArgs()
