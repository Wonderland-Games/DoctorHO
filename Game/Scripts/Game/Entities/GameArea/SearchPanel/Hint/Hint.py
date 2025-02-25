from Foundation.Initializer import Initializer
from Foundation.SceneManager import SceneManager
from UIKit.Managers.PrototypeManager import PrototypeManager
from Game.Entities.GameArea.SearchPanel.Hint.HintEffect import HintEffect
from Game.Entities.GameArea.SearchPanel.Hint.HintCounter import HintCounter


PROTOTYPE_BUTTON = "Hint"


class Hint(Initializer):
    def __init__(self):
        super(Hint, self).__init__()
        self._root = None
        self.game = None
        self.button = None
        self.hint_counter = None
        self.hint_item = None
        self.hint_effect = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, game):
        super(Hint, self)._onInitialize()
        self.game = game

        self._createRoot()
        self._attachButton()
        self._setupHintCounter()
        self._initHintEffect()

    def _onFinalize(self):
        super(Hint, self)._onFinalize()

        if self.button is not None:
            self.button.onDestroy()
            self.button = None

        if self.hint_effect is not None:
            self.hint_effect.onFinalize()
            self.hint_effect = None

        if self.hint_counter is not None:
            self.hint_counter.onFinalize()
            self.hint_counter = None

        if self._root is not None:
            self._root.removeFromParent()
            Mengine.destroyNode(self._root)
            self._root = None

        self.game = None
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
        self.button = PrototypeManager.generateObjectContainerOnNode(self._root, PROTOTYPE_BUTTON, PROTOTYPE_BUTTON)
        self.button.setEnable(True)

    def getSize(self):
        button_bounding_box = self.button.getCompositionBounds()
        button_size = Utils.getBoundingBoxSize(button_bounding_box)
        return button_size

    def isAvailable(self):
        return self.hint_counter.count > 0

    # - HintCounter ----------------------------------------------------------------------------------------------------

    def _setupHintCounter(self):
        hint_count = 5
        self.hint_counter = HintCounter()
        self.hint_counter.onInitialize(self.game, hint_count)

        button_size = self.getSize()
        self.hint_counter.attachTo(self._root)
        self.hint_counter.setLocalPosition(Mengine.vec2f(button_size.x / 2, - button_size.y / 2))

    # - HintEffect -----------------------------------------------------------------------------------------------------

    def _initHintEffect(self):
        self.hint_effect = HintEffect()
        self.hint_effect.onInitialize(self.game)

        # self.hint_effect.attachTo(self.game.node)

        current_scene = SceneManager.getCurrentScene()
        current_scene_main_layer = current_scene.getMainLayer()
        scene_parent = current_scene_main_layer.getParent()

        self.hint_effect.attachTo(scene_parent)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def clickHint(self, source):
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
        source.addFunction(self.hint_counter.decHintCount)

        source.addFunction(self.game.search_panel.hint.button.movie.setBlock, True)
        source.addFunction(self.game.search_panel.virtual_area.freeze, True)
        source.addFunction(self.game.search_level.virtual_area.freeze, True)

        source.addScope(self.hint_effect.show, hint_item_transformation)
        source.addListener(Notificator.onItemClick, Filter=lambda item: item == self.hint_item)
        source.addScope(self.hint_effect.hide, hint_item_transformation)

        source.addFunction(self._cleanHintItem)

        source.addFunction(self.game.search_panel.hint.button.movie.setBlock, False)
        source.addFunction(self.game.search_panel.virtual_area.freeze, False)
        source.addFunction(self.game.search_level.virtual_area.freeze, False)

    def _cleanHintItem(self):
        self.hint_item = None
