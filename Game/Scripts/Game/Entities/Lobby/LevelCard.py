from Foundation.Initializer import Initializer
from Foundation.GroupManager import GroupManager
from Game.Managers.GameManager import GameManager

GROUP_LEVEL_CARDS = "LevelCards"
SLOT_LEVEL = "Level"
ALIAS_TITLE = "$LevelCardTitle"
TEXT_TITLE = "ID_LevelCardTitle"

MOVIE_STATE_BLOCKED = "Blocked"
MOVIE_STATE_UNLOCKING = "Unlocking"
MOVIE_STATE_ACTIVE = "Active"


class LevelCard(Initializer):
    STATE_BLOCKED = 0
    STATE_UNLOCKING = 1
    STATE_ACTIVE = 2

    def __init__(self):
        super(LevelCard, self).__init__()
        self.level_id = None
        self.root = None
        self.state = None
        self.movie = None
        self.level = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, level_id, state=None):
        super(LevelCard, self)._onInitialize()
        self.level_id = level_id

        self.state = self.STATE_BLOCKED
        if state is not None:
            self.state = state

        self._createRoot()

        self._setupMovie()
        self._setupLevel()

    def _onFinalize(self):
        super(LevelCard, self)._onFinalize()

        self._destroyCurrentStateMovie()

        if self.movie is not None:
            self.movie.onDestroy()
            self.movie = None

        if self.root is not None:
            self.root.removeFromParent()
            Mengine.destroyNode(self.root)
            self.root = None

        self.level_id = None
        self.state = None

    # - Root -----------------------------------------------------------------------------------------------------------

    def _createRoot(self):
        self.root = Mengine.createNode("Interender")
        self.root.setName(self.__class__.__name__ + "_" + str(self.level_id))

    def attachTo(self, node):
        self.root.removeFromParent()
        node.addChild(self.root)

    def setLocalPosition(self, pos):
        self.root.setLocalPosition(pos)

    def getRoot(self):
        return self.root

    # - State ----------------------------------------------------------------------------------------------------------

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def isActive(self):
        return self.state == self.STATE_ACTIVE

    def _createNewStateMovie(self):
        state_movie = {
            self.STATE_BLOCKED: MOVIE_STATE_BLOCKED,
            self.STATE_UNLOCKING: MOVIE_STATE_UNLOCKING,
            self.STATE_ACTIVE: MOVIE_STATE_ACTIVE,
        }

        level_params = GameManager.getLevelParams(self.level_id)
        level_movie_name = level_params.LevelMovie
        current_state_movie = state_movie.get(self.state)
        movie_level_state_name = level_movie_name + "_{}".format(current_state_movie)

        self.level = GroupManager.generateObjectUnique(movie_level_state_name, GROUP_LEVEL_CARDS, movie_level_state_name)
        self.level.setEnable(True)

        level_node = self.level.getEntityNode()
        level_slot = self.movie.getMovieSlot(SLOT_LEVEL)
        level_slot.addChild(level_node)

    def _destroyCurrentStateMovie(self):
        if self.level is not None:
            self.level.onDestroy()
            self.level = None

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupMovie(self):
        level_params = GameManager.getLevelParams(self.level_id)
        card_movie_name = level_params.CardMovie

        self.movie = GroupManager.generateObjectUnique(card_movie_name, GROUP_LEVEL_CARDS, card_movie_name)
        self.movie.setEnable(True)

        movie_node = self.movie.getEntityNode()
        self.root.addChild(movie_node)

        env = card_movie_name + "_" + str(self.level_id)
        card_text_id = level_params.LevelCardTextId
        if Mengine.existText(card_text_id) is True:
            title_text = Mengine.getTextFromId(card_text_id)
        else:
            Trace.msg_err("[{}] For card {!r} not found text {!r}".format(self.__class__.__name__, self.level_id, card_text_id))
            title_text = ""

        self.movie.setTextAliasEnvironment(env)

        Mengine.setTextAlias(env, ALIAS_TITLE, TEXT_TITLE)
        Mengine.setTextAliasArguments(env, ALIAS_TITLE, title_text)

    def _setupLevel(self):
        # get level from chapter data
        self._createNewStateMovie()

    # - Utils ----------------------------------------------------------------------------------------------------------

    def getSize(self):
        button_bounds = self.movie.getCompositionBounds()
        button_size = Utils.getBoundingBoxSize(button_bounds)
        return button_size

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def scopeChangeLevelState(self, source, state):
        self._destroyCurrentStateMovie()
        self.setState(state)
        self._createNewStateMovie()

        if self.state == self.STATE_UNLOCKING:
            source.addPlay(self.level)
            source.addFunction(self._destroyCurrentStateMovie)
            source.addFunction(self.setState, self.STATE_ACTIVE)
            source.addFunction(self._createNewStateMovie)
