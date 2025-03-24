from Foundation.Initializer import Initializer
from Foundation.GroupManager import GroupManager

GROUP_LEVEL_CARDS = "LevelCards"
SLOT_LEVEL = "Level"
ALIAS_TITLE = "$LevelCardTitle"
TEXT_TITLE = "ID_LevelCardTitle"


class LevelCard(Initializer):
    def __init__(self):
        super(LevelCard, self).__init__()
        self.level_name = None
        self.root = None
        self.movie = None
        self.level = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, level_name):
        super(LevelCard, self)._onInitialize()
        self.level_name = level_name

        self._createRoot()

        self._setupMovie()
        self._setupLevel()

    def _onFinalize(self):
        super(LevelCard, self)._onFinalize()

        if self.level is not None:
            self.level.onDestroy()
            self.level = None

        if self.movie is not None:
            self.movie.onDestroy()
            self.movie = None

        if self.root is not None:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

        self.level_name = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__ + "_" + self.level_name)

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    def setLocalPosition(self, pos):
        self.root.setLocalPosition(pos)

    def getRoot(self):
        return self.root

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupMovie(self):
        # get movie card from chapter data
        movie_card_name = "Movie2_Card_1"
        self.movie = GroupManager.generateObjectUnique(movie_card_name, GROUP_LEVEL_CARDS, movie_card_name)
        self.movie.setEnable(True)

        movie_node = self.movie.getEntityNode()
        self.root.addChild(movie_node)

        env = movie_card_name + "_" + self.level_name
        title_id = TEXT_TITLE + "_" + self.level_name
        title_text = Mengine.getTextFromId(title_id)

        self.movie.setTextAliasEnvironment(env)

        Mengine.setTextAlias(env, ALIAS_TITLE, TEXT_TITLE)
        Mengine.setTextAliasArguments(env, ALIAS_TITLE, title_text)

    def _setupLevel(self):
        # get level from chapter data
        movie_level_name = "Movie2_{}".format(self.level_name)
        self.level = GroupManager.generateObjectUnique(movie_level_name, GROUP_LEVEL_CARDS, movie_level_name)
        self.level.setEnable(True)

        level_node = self.level.getEntityNode()
        level_slot = self.movie.getMovieSlot(SLOT_LEVEL)
        level_slot.addChild(level_node)

    # - Utils ----------------------------------------------------------------------------------------------------------

    def getSize(self):
        button_bounds = self.movie.getCompositionBounds()
        button_size = Utils.getBoundingBoxSize(button_bounds)
        return button_size
