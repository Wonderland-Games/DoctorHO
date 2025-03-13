from Foundation.Initializer import Initializer
from UIKit.Managers.PrototypeManager import PrototypeManager


MOVIE_BG = "HintCounter"
TEXT_ID = "ID_HintCounter"
ALIAS = "$HintCounter"


class HintCounter(Initializer):
    def __init__(self):
        super(HintCounter, self).__init__()
        self.game = None
        self.root = None
        self.movie = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game):
        super(HintCounter, self)._onInitialize()
        self.game = game

        self._createRoot()
        self._setupMovie()

    def _onFinalize(self):
        super(HintCounter, self)._onFinalize()
        self.game = None

        if self.movie is not None:
            self.movie.onDestroy()
            self.movie = None

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

    # - Movie ----------------------------------------------------------------------------------------------------------

    def _setupMovie(self):
        self.movie = PrototypeManager.generateObjectUniqueOnNode(self.root, MOVIE_BG)
        self.movie.setEnable(True)

        Mengine.setTextAlias("", ALIAS, TEXT_ID)
        Mengine.setTextAliasArguments("", ALIAS, self.game.search_panel.hint.getHintCount)
