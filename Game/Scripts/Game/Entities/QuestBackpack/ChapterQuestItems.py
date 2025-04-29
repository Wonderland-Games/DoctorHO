from Foundation.Initializer import Initializer


class ChapterQuestItems(Initializer):
    def __init__(self):
        super(ChapterQuestItems, self).__init__()
        self.root = None
        self.chapter_id = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, chapter_id):
        super(ChapterQuestItems, self)._onInitialize()
        self.chapter_id = chapter_id

        self._createRoot()

    def _onFinalize(self):
        super(ChapterQuestItems, self)._onFinalize()

        if self.root is not None:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

        self.chapter_id = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__ + "_" + str(self.chapter_id))

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    def getRoot(self):
        return self.root
