from Foundation.Initializer import Initializer
from Foundation.GroupManager import GroupManager
from Game.Managers.GameManager import GameManager
from Game.Entities.Lobby.LevelCard import LevelCard


GROUP_LEVEL_CARDS = "LevelCards"
CHAPTER_SLOTS = "Card_{}"


class ChapterLevels(Initializer):
    def __init__(self):
        super(ChapterLevels, self).__init__()
        self.root = None
        self.chapter_id = None
        self.level_slots_movie = None
        self.level_cards = {}

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, chapter_id):
        super(ChapterLevels, self)._onInitialize()
        self.chapter_id = chapter_id

        self._createRoot()
        self._setupLevelCards()

    def _onFinalize(self):
        super(ChapterLevels, self)._onFinalize()

        if self.level_slots_movie is not None:
            self.level_slots_movie.onDestroy()
            self.level_slots_movie = None

        for level_card in self.level_cards.values():
            level_card.onFinalize()
        self.level_cards.clear()

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

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupLevelCards(self):
        # get levels from chapter data
        chapter_params = GameManager.getChapterParams(self.chapter_id)
        chapter_levels_id = chapter_params.LevelsId
        chapter_slots = chapter_params.Slots

        self.level_slots_movie = GroupManager.generateObjectUnique(chapter_slots, GROUP_LEVEL_CARDS, chapter_slots)
        self.level_slots_movie.setEnable(True)
        level_slots_movie_node = self.level_slots_movie.getEntityNode()
        self.root.addChild(level_slots_movie_node)

        player_game_data = GameManager.getPlayerGameData()
        current_chapter_data = player_game_data.getCurrentChapterData()
        active_levels_id = current_chapter_data.getCurrentLevelsId()

        # init and attach level cards to slots movie
        for i, level_id in enumerate(chapter_levels_id):
            card = LevelCard()

            if level_id in active_levels_id:
                card.onInitialize(level_id, card.STATE_ACTIVE)
            else:
                card.onInitialize(level_id)

            self.level_cards[level_id] = card

            card_node = card.getRoot()
            card_slot = self.level_slots_movie.getMovieSlot(CHAPTER_SLOTS.format(i + 1))
            card_slot.addChild(card_node)
