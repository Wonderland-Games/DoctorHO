from Foundation.Initializer import Initializer
from MobileKit.IconManager import IconManager


ICON_PROTOTYPE = "Heart"
MOVIE_ICON = "Movie2_LivesCounterIcon"
TEXT_ID = "ID_LivesCounter"


class LivesCounter(Initializer):
    def __init__(self):
        super(LivesCounter, self).__init__()
        self.game = None
        self.count = None
        self.root = None
        self.icon = None
        self.text = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game, count):
        super(LivesCounter, self)._onInitialize()
        self.game = game
        self.count = count

        self._createRoot()

        self._setupIcon()
        self._setupText()

    def _onFinalize(self):
        super(LivesCounter, self)._onFinalize()
        self.game = None
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
        self.text.enable()

        self.root.addChild(self.text)

    def updateTextArgs(self, value=None):
        if value is None:
            value = self.count

        self.text.setTextFormatArgs(value)

    def decItemsCount(self):
        if self.count <= 0:
            return

        self.count -= 1
        self.updateTextArgs()
        Notification.notify(Notificator.onLevelLivesChanged, self.count)

    # - Icon -----------------------------------------------------------------------------------------------------------

    def _setupIcon(self):
        # self.icon = self.game.object.generateObjectUnique(MOVIE_ICON, MOVIE_ICON)
        self.icon = IconManager.generateIcon(ICON_PROTOTYPE)
        self.icon.setEnable(True)
        icon_node = self.icon.getEntityNode()
        self.root.addChild(icon_node)
