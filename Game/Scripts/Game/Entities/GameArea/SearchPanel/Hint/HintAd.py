from Foundation.Initializer import Initializer
from UIKit.Managers.PrototypeManager import PrototypeManager


BUTTON_HINT = "Hint"
PROTOTYPE_ICON = "HintAdIcon"


class HintAd(Initializer):
    def __init__(self):
        super(HintAd, self).__init__()
        self._root = None
        self.game = None
        self.button = None
        self.ad_icon_bg = None
        self.ad_icon = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game):
        super(HintAd, self)._onInitialize()
        self.game = game

        self._createRoot()
        self._setupButton()
        self._setupAdIcon()

    def _onFinalize(self):
        super(HintAd, self)._onFinalize()

        if self.ad_icon is not None:
            self.ad_icon.onDestroy()
            self.ad_icon = None

        if self.ad_icon_bg is not None:
            self.ad_icon_bg.onDestroy()
            self.ad_icon_bg = None

        if self.button is not None:
            self.button.onDestroy()
            self.button = None

        if self._root is not None:
            self._root.removeFromParent()
            Mengine.destroyNode(self._root)
            self._root = None

        self.game = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self._root = Mengine.createNode("Interender")
        self._root.setName(self.__class__.__name__)

    def attachTo(self, node):
        self._root.removeFromParent()
        node.addChild(self._root)

    def getRoot(self):
        return self._root

    # - Button ---------------------------------------------------------------------------------------------------------

    def _setupButton(self):
        self.button = PrototypeManager.generateObjectContainerOnNode(self._root, BUTTON_HINT, BUTTON_HINT)
        self.button.setEnable(True)

    def getSize(self):
        button_size = self.button.getSize()
        return button_size

    # - Icon -----------------------------------------------------------------------------------------------------------

    def _setupAdIcon(self):
        self.ad_icon = PrototypeManager.generateObjectContainerOnNode(self._root, PROTOTYPE_ICON, PROTOTYPE_ICON)
        self.ad_icon.setEnable(True)

        button_size = self.getSize()
        self.ad_icon.attachTo(self._root)
        self.ad_icon.setLocalPosition(Mengine.vec2f(button_size.x / 2, - button_size.y / 2))
