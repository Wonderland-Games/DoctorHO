from Foundation.Initializer import Initializer
from UIKit.Managers.PrototypeManager import PrototypeManager
from UIKit.Managers.IconManager import IconManager


MOVIE_BG = "HintCounterBackground"
ICON_AD = "Advertising"
TEXT_ID = "ID_HintCounter"


class HintCounter(Initializer):
    def __init__(self):
        super(HintCounter, self).__init__()
        self.game = None
        self.count = None
        self.root = None
        self.background = None
        self.text = None
        self.ad_icon = None

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

        self._destroyAdIcon()

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

    # - Ad Icon --------------------------------------------------------------------------------------------------------

    def _setupAdIcon(self):
        self.ad_icon = IconManager.generateIconOnNode(self.root, ICON_AD)
        self.ad_icon.setEnable(True)

        icon_bounds = self.ad_icon.getCompositionBounds()
        icon_size = Utils.getBoundingBoxSize(icon_bounds)

        background_bounds = self.background.getCompositionBounds()
        background_size = Utils.getBoundingBoxSize(background_bounds)

        size_perc = background_size / icon_size
        max_dimension = max(size_perc.x, size_perc.y)
        new_scale = Mengine.vec2f(max_dimension, max_dimension)

        self.ad_icon.setScale(new_scale)

    def _destroyAdIcon(self):
        if self.ad_icon is not None:
            self.ad_icon.onDestroy()
            self.ad_icon = None

    # - Tools ----------------------------------------------------------------------------------------------------------

    def decHintCount(self):
        if self.count <= 0:
            return

        self.count -= 1
        self.updateTextArgs()

        if self.count == 0:
            self._setupAdIcon()
            self.text.disable()

    def incHintCount(self):
        self.count += 1
        self.updateTextArgs()

        if self.count >= 1:
            self._destroyAdIcon()
            self.text.enable()
