from Foundation.Initializer import Initializer
from Foundation.TaskManager import TaskManager
from UIKit.Managers.PrototypeManager import PrototypeManager


PROTOTYPE_BUTTON = "Settings"


class Settings(Initializer):
    def __init__(self):
        super(Settings, self).__init__()
        self.tcs = []
        self.root = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self):
        super(Settings, self)._onInitialize()
        self._createRoot()
        self._createButton()

        self._runTaskChains()

    def _onFinalize(self):
        super(Settings, self)._onFinalize()

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        if self.button is not None:
            self.button.onDestroy()
            self.button = None

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

    # - Button ---------------------------------------------------------------------------------------------------------

    def _createButton(self):
        self.button = PrototypeManager.generateObjectContainer(PROTOTYPE_BUTTON, PROTOTYPE_BUTTON)
        self.button.setEnable(True)

        button_node = self.button.getEntityNode()
        self.root.addChild(button_node)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc = TaskManager.createTaskChain(Name=self.__class__.__name__ + "_" + name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        with self._createTaskChain("Button", Repeat=True) as tc:
            tc.addTask("TaskMovie2ButtonClick", Movie2Button=self.button.movie)
            tc.addNotify(Notificator.onPopUpShow, "Settings")
