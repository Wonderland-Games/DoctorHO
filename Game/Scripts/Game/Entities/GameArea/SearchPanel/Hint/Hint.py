from Foundation.Initializer import Initializer


BUTTON_HINT = "Movie2Button_Hint"


class Hint(Initializer):
    def __init__(self):
        super(Hint, self).__init__()
        self._root = None
        self.game = None
        self.button = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game):
        self.game = game

        self._createRoot()
        self._attachButton()

    def _onFinalize(self):
        if self._root is not None:
            self._root.removeFromParent()
            Mengine.destroyNode(self._root)
            self._root = None

        self.game = None
        self.button = None

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

    def _attachButton(self):
        self.button = self.game.object.getObject(BUTTON_HINT)
        button_node = self.button.getEntityNode()
        self._root.addChild(button_node)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def clickHint(self, source):
        source.addFunction(self.game.search_panel.hint.button.setBlock, True)

        source.addPrint("CLICKED HINT")

        source.addFunction(self.game.search_panel.hint.button.setBlock, False)
