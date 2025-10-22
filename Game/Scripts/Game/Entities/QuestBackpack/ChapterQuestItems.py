from Foundation.Initializer import Initializer
from Game.Managers.GameManager import GameManager
from Game.Entities.QuestBackpack.QuestItem import QuestItem


CHAPTER_SLOTS = "QuestItem_{}"


class ChapterQuestItems(Initializer):
    def __init__(self):
        super(ChapterQuestItems, self).__init__()
        self.parent_entity = None
        self.root = None
        self.chapter_id = None
        self.items_slots_movie = None
        self.quest_items = {}

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, parent_entity, chapter_id):
        super(ChapterQuestItems, self)._onInitialize()
        self.parent_entity = parent_entity
        self.chapter_id = chapter_id

        self._createRoot()
        self.setupQuestItems()

    def _onFinalize(self):
        super(ChapterQuestItems, self)._onFinalize()

        for quest_item in self.quest_items.values():
            quest_item.onFinalize()
        self.quest_items = {}

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
        chapter_quest_items_slots = chapter_params.Slots

        self.items_slots_movie = self.parent_entity.object.generateObjectUnique(chapter_quest_items_slots, chapter_quest_items_slots)
        self.items_slots_movie.setEnable(True)
        items_slots_movie_node = self.items_slots_movie.getEntityNode()
        self.root.addChild(items_slots_movie_node)

        player_data = GameManager.getPlayerGameData()
        chapter_data = player_data.getCurrentChapterData()
        quest_index = chapter_data.getCurrentQuestIndex()
        if quest_index == 0:
            return

        chapter_quests_params = GameManager.getQuestParamsByChapter(self.chapter_id)
        for i, quest_param in enumerate(chapter_quests_params):
            # Temporary generating object
            quest_item_object = GameManager.generateQuestItem(quest_param.QuestItem)

            # Initializing QuestItem class
            quest_item_entity = quest_item_object.getEntity()

            quest_item = QuestItem()
            if i < quest_index:
                quest_item_state = quest_item.STATE_ACTIVE
            else:
                break

            quest_item.onInitialize(quest_item_entity, quest_item_state)

            quest_item_slot = self.items_slots_movie.getMovieSlot(CHAPTER_SLOTS.format(i + 1))
            quest_item.attachTo(quest_item_slot)

            self.quest_items[quest_param.QuestItem] = quest_item

            # Destroying used object
            quest_item_object.onDestroy()
