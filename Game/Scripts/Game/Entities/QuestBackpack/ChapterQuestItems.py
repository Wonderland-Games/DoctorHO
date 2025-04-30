from Foundation.Initializer import Initializer
from Game.Managers.GameManager import GameManager


CHAPTER_SLOTS = "QuestItem_{}"


class ChapterQuestItems(Initializer):
    def __init__(self):
        super(ChapterQuestItems, self).__init__()
        self.parent_entity = None
        self.root = None
        self.chapter_id = None
        self.items_slots_movie = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, parent_entity, chapter_id):
        super(ChapterQuestItems, self)._onInitialize()
        self.parent_entity = parent_entity
        self.chapter_id = chapter_id

        self._createRoot()
        self.setupQuestItems()

    def _onFinalize(self):
        super(ChapterQuestItems, self)._onFinalize()

        if self.items_slots_movie is not None:
            self.items_slots_movie.onDestroy()
            self.items_slots_movie = None

        if self.root is not None:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

        self.chapter_id = None
        self.parent_entity = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__ + "_" + str(self.chapter_id))

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    def getRoot(self):
        return self.root

    # - Setup ----------------------------------------------------------------------------------------------------------

    def setupQuestItems(self):
        # get levels from chapter data
        chapter_params = GameManager.getChapterParams(self.chapter_id)
        chapter_levels_id = chapter_params.LevelsId
        chapter_quest_items_slots = chapter_params.Slots

        self.items_slots_movie = self.parent_entity.object.generateObjectUnique(chapter_quest_items_slots, chapter_quest_items_slots)
        self.items_slots_movie.setEnable(True)
        items_slots_movie_node = self.items_slots_movie.getEntityNode()
        self.root.addChild(items_slots_movie_node)
