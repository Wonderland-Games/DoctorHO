from Foundation.Initializer import Initializer
from Foundation.TaskManager import TaskManager
from Foundation.Entities.MovieVirtualArea.VirtualArea import VirtualArea
from Game.Entities.GameArea.SearchPanel.Item import Item


MOVIE_PANEL = "Movie2_SearchPanel"
PANEL_VA = "virtual_area"


class SearchPanel(Initializer):
    def __init__(self):
        super(SearchPanel, self).__init__()
        self.game = None
        self.virtual_area = None
        self.root = None
        self.movie_panel = None
        self.tcs = []
        self.items = []

    def _onInitialize(self, game):
        self.game = game

        self._initVirtualArea()

        self._createRoot()
        self._attachPanel()
        self._initItems()

        self._setupVirtualArea()
        return True

    def _onActivate(self):
        self.root.enable()
        self._runTaskChains()

    def _onFinalize(self):
        self.panel = None

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        for item in self.items:
            item.onFinalize()
        self.items = []

        if self.root is not None:
            Mengine.destroyNode(self.root)
            self.root = None

        if self.virtual_area is not None:
            self.virtual_area.onFinalize()
            self.virtual_area = None

    def _initVirtualArea(self):
        self.virtual_area = VirtualArea()
        self.virtual_area.onInitialize(
            dragging_mode="horizontal",
            enable_scale=False,
            disable_drag_if_invalid=False
        )

    def _setupVirtualArea(self):
        self.virtual_area.setup_with_movie(self.movie_panel, PANEL_VA, PANEL_VA)
        panel_bounds = self.movie_panel.getCompositionBounds()
        panel_size = Utils.getBoundingBoxSize(panel_bounds)

        self.virtual_area.setup_viewport(0, 0, panel_size.x, panel_size.y)
        self.virtual_area.set_content_size(0, 0, panel_size.x, panel_size.y)

        self.virtual_area._socket.setDefaultHandle(False)

        panel_entity = self.movie_panel.getEntity()
        panel_entity.setSocketHandle(PANEL_VA, "button", False)
        panel_entity.setSocketHandle(PANEL_VA, "enter", False)
        panel_entity.setSocketHandle(PANEL_VA, "move", False)

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__)

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    def getHeight(self):
        movie_panel = self.game.object.getObject(MOVIE_PANEL)
        movie_panel_bounds = movie_panel.getCompositionBounds()
        movie_panel_height = Utils.getBoundingBoxHeight(movie_panel_bounds)
        return movie_panel_height

    def _attachPanel(self):
        self.movie_panel = self.game.object.getObject(MOVIE_PANEL)
        movie_panel_node = self.movie_panel.getEntityNode()
        self.root.addChild(movie_panel_node)

    def _initItems(self):
        for item_obj in self.game.items:
            item = Item()
            item.onInitialize(self.game, item_obj)
            # item.attachTo(self.root)
            item.attachTo(self.virtual_area.get_node())
            self.items.append(item)

    def _createTaskChain(self, name, **params):
        tc = TaskManager.createTaskChain(Name=self.__class__.__name__+"_"+name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        pass
