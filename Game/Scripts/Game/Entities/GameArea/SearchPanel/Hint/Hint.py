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
        # get random item from search panel
        panel_item = self.game.search_panel.getRandomAvailableItem()
        if panel_item is None:
            return

        # get scene item by panel item
        scene_item = panel_item.item_obj

        # calc item hint point
        hint_point = scene_item.calcWorldHintPoint()

        # create temp hint node to get transformation later
        temp_hint_node = Mengine.createNode("Interender")
        temp_hint_node.setName("TempHintNode")

        # setting items position to temp node
        self.game.addChild(temp_hint_node)
        temp_hint_node.setWorldPosition(hint_point)

        # getting transformation from temp node
        hint_item_transformation = temp_hint_node.getTransformation()

        source.addFunction(self.game.search_panel.hint.button.setBlock, True)

        source.addScope(self.hint_effect.show, hint_item_transformation)
        source.addDelay(1000.0)
        source.addScope(self.hint_effect.hide, hint_item_transformation)

        source.addTask("TaskNodeRemoveFromParent", Node=temp_hint_node)
        source.addTask("TaskNodeDestroy", Node=temp_hint_node)

        source.addFunction(self.game.search_panel.hint.button.setBlock, False)
