from Foundation.Initializer import Initializer


TEXT_ID = "ID_ItemsCounter"


class ItemsCounter(Initializer):
    def __init__(self):
        super(ItemsCounter, self).__init__()
        self.items_count = None
        self.items_amount = None
        self.node = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, items_count, items_amount):
        self.items_count = items_count
        self.items_amount = items_amount

        self._createTextNode()

    def _onFinalize(self):
        self.items_count = None
        self.items_amount = None

        if self.node is not None:
            self.node.removeFromParent()
            Mengine.destroyNode(self.node)
            self.node = None

    # - Node -----------------------------------------------------------------------------------------------------------

    def _createTextNode(self):
        self.node = Mengine.createNode("TextField")
        self.node.setName(self.__class__.__name__)
        self.node.setVerticalCenterAlign()
        self.node.setHorizontalCenterAlign()
        self.node.setTextId(TEXT_ID)
        self.updateTextArgs()
        self.node.enable()

    def attachTo(self, node):
        self.node.removeFromParent()
        node.addChild(self.node)

    def setLocalPosition(self, pos):
        self.node.setLocalPosition(pos)

    # - Text -----------------------------------------------------------------------------------------------------------

    def updateTextArgs(self, value_1=None, value_2=None):
        if value_1 is None:
            value_1 = self.items_count

        if value_2 is None:
            value_2 = self.items_amount

        self.node.setTextFormatArgs(value_1, value_2)

    def incItemsCount(self):
        self.items_count += 1
        self.updateTextArgs()
