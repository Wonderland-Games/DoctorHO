from Foundation.Initializer import Initializer
from Foundation.TaskManager import TaskManager
from Game.Entities.GameArea.SearchPanel.Hint.HintEffect import HintEffect


BUTTON_HINT = "Movie2Button_Hint"


class Hint(Initializer):
    def __init__(self):
        super(Hint, self).__init__()
        self._root = None
        self.tcs = []
        self.game = None
        self.button = None
        self.hint_item = None
        self.hint_effect = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game):
        super(Hint, self)._onInitialize()
        self.game = game

        self._createRoot()
        self._attachButton()
        self._initHintEffect()

        self._runTaskChains()

    def _onFinalize(self):
        super(Hint, self)._onFinalize()

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        if self.hint_effect is not None:
            self.hint_effect.onFinalize()
            self.hint_effect = None

        if self._root is not None:
            self._root.removeFromParent()
            Mengine.destroyNode(self._root)
            self._root = None

        self.game = None
        self.button = None
        self.hint_item = None

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

    # - HintEffect -----------------------------------------------------------------------------------------------------

    def _initHintEffect(self):
        self.hint_effect = HintEffect()
        self.hint_effect.onInitialize(self.game)
        self.hint_effect.attachTo(self.game.node)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base + "_" + name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        # hint logic
        with self._createTaskChain("Hint", Repeat=True) as tc:
            tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.button)
            tc.addPrint("CLICK HINT")
            tc.addScope(self._clickHint)

    def _clickHint(self, source):
        # get random panel item from search panel
        panel_item = self.game.search_panel.getRandomAvailableItem()
        if panel_item is None:
            return

        # save hint item
        self.hint_item = panel_item.item_obj

        # calc item hint point
        hint_point = self.hint_item.calcWorldHintPoint()

        # create temp hint node
        temp_hint_node = Mengine.createNode("Interender")
        temp_hint_node.setName("TempHintNode")

        # setting items position to temp node
        self.game.addChild(temp_hint_node)
        temp_hint_node.setWorldPosition(hint_point)

        # getting transformation from temp node
        hint_item_transformation = temp_hint_node.getTransformation()

        # destroy temp hint node
        temp_hint_node.removeFromParent()
        Mengine.destroyNode(temp_hint_node)

        # hint effect logic
        source.addFunction(self.game.search_panel.hint.button.setBlock, True)
        source.addFunction(self.game.search_panel.virtual_area.freeze, True)
        source.addFunction(self.game.search_level.virtual_area.freeze, True)

        source.addScope(self.hint_effect.show, hint_item_transformation)
        source.addListener(Notificator.onItemClick, Filter=lambda item: item == self.hint_item)
        source.addScope(self.hint_effect.hide, hint_item_transformation)

        source.addFunction(self._cleanHintItem)

        source.addFunction(self.game.search_panel.hint.button.setBlock, False)
        source.addFunction(self.game.search_panel.virtual_area.freeze, False)
        source.addFunction(self.game.search_level.virtual_area.freeze, False)

    def _cleanHintItem(self):
        self.hint_item = None
