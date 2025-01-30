from Foundation.Initializer import Initializer
from Foundation.TaskManager import TaskManager


MOVIE_PANEL = "Movie2_SearchPanel"


class SearchPanel(Initializer):
    def __init__(self):
        super(SearchPanel, self).__init__()
        self._game = None
        self.root = None
        self.movie_panel = None
        self.tcs = []

    def _onInitialize(self, game):
        self._game = game
        self._createRoot()
        self._attachPanel()
        return True

    def _onActivate(self):
        self.root.enable()
        self._runTaskChains()

    def _onFinalize(self):
        self.panel = None

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        if self.root is not None:
            Mengine.destroyNode(self.root)
            self.root = None

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__)

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    def _attachPanel(self):
        self.movie_panel = self._game.object.getObject(MOVIE_PANEL)
        movie_panel_node = self.movie_panel.getEntityNode()
        self.root.addChild(movie_panel_node)

    def getHeight(self):
        movie_panel = self._game.object.getObject(MOVIE_PANEL)
        movie_panel_bounds = movie_panel.getCompositionBounds()
        movie_panel_height = Utils.getBoundingBoxHeight(movie_panel_bounds)
        return movie_panel_height

    def _createTaskChain(self, name, **params):
        tc = TaskManager.createTaskChain(Name=self.__class__.__name__+"_"+name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        pass
