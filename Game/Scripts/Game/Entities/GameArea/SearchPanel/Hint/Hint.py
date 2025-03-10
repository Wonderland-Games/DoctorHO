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
        button_size = self.button.getSize()
        return button_size

    def isAvailable(self):
        return self.game.HintCount > 0

    # - HintCounter ----------------------------------------------------------------------------------------------------

    def _setupHintCounter(self):
        self.hint_counter = HintCounter()
        self.hint_counter.onInitialize(self.game, self.game.HintCount)

        button_size = self.getSize()
        self.hint_counter.attachTo(self._root)
        self.hint_counter.setLocalPosition(Mengine.vec2f(button_size.x / 2, - button_size.y / 2))

    def incHintCount(self):
        hint_count = self.game.object.getParam("HintCount")
        self.game.object.setParam("HintCount", hint_count + 1)
        self.hint_counter.incHintCount()

    def decHintCount(self):
        hint_count = self.game.object.getParam("HintCount")
        self.game.object.setParam("HintCount", hint_count - 1)
        self.hint_counter.decHintCount()

    # - HintEffect -----------------------------------------------------------------------------------------------------

    def _initHintEffect(self):
        self.hint_effect = HintEffect()
        self.hint_effect.onInitialize(self.game)

        # self.hint_effect.attachTo(self.game.node)

        current_scene = SceneManager.getCurrentScene()
        current_scene_main_layer = current_scene.getMainLayer()
        scene_parent = current_scene_main_layer.getParent()

        self.hint_effect.attachTo(scene_parent)

    # - Tools ----------------------------------------------------------------------------------------------------------

    def cleanHintItem(self):
        self.hint_item = None
