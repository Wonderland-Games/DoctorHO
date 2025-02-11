from Foundation.Initializer import Initializer


TEXT_ID = "ID_SearchPanel_LivesCounter"


class LivesCounter(Initializer):
    def __init__(self):
        super(LivesCounter, self).__init__()
        self.count = None
        self.root = None
        self.icon = None
        self.text = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, count):
        super(LivesCounter, self)._onInitialize()
        self.count = count

        self._createRoot()

        self._setupIcon()
        self._setupText()

    def _onFinalize(self):
        super(LivesCounter, self)._onFinalize()
        self.count = None

        if self.icon is not None:
            self.icon.onDestroy()
            self.icon = None

        if self.text is not None:
            self.text.removeFromParent()
            Mengine.destroyNode(self.text)
            self.text = None

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
        self.root.addChild(self.text)
        self.text.enable()

    def updateTextArgs(self, value=None):
        if value is None:
            value = self.count

        self.text.setTextFormatArgs(value)

    def decItemsCount(self):
        self.count -= 1
        self.updateTextArgs()

    # - Icon -----------------------------------------------------------------------------------------------------------

    def _setupIcon(self):
        pass
