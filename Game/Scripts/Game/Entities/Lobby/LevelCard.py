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

PROTOTYPE_QUEST_INDICATOR = "Movie2_QuestIndicator"
SLOT_QUEST_INDICATOR = "QuestIndicator"

PROTOTYPE_QUEST_PROGRESS_BAR = "Movie2ProgressBar_Quest"
TEXT_QUEST_PROGRESS_BAR = "ID_LevelCard_QuestProgress"
SLOT_QUEST_PROGRESS_BAR = "QuestProgressBar"
QUEST_PROGRESS_BAR_FOLLOW_SPEED = 0.05


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
        self.quest_indicator = None
        self.quest_progress_bar = None
        self.quest_progress_value_follower = None

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
        self._setupQuestIndicator()
        self._setupQuestProgressBar()

    def _onFinalize(self):
        super(LevelCard, self)._onFinalize()

        self._destroyCurrentStateMovie()

        if self.movie is not None:
            self.movie.onDestroy()
            self.movie = None

        if self.quest_indicator is not None:
            self.quest_indicator.onDestroy()
            self.quest_indicator = None

        self.destroyQuestProgressBar()

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

    def _setupQuestIndicator(self):
        player_data = GameManager.getPlayerGameData()
        current_chapter_data = player_data.getCurrentChapterData()
        level_data = current_chapter_data.getLevelData(self.level_id)
        if level_data.getActive() is False:
            return

        chapter_id = current_chapter_data.getChapterId()
        current_quest_index = current_chapter_data.getCurrentQuestIndex()
        quest_params = GameManager.getQuestParamsWithChapterIdAndQuestIndex(chapter_id, current_quest_index)

        if quest_params is None:
            return

        if quest_params.LevelId != self.level_id:
            return

        self.quest_indicator = GroupManager.generateObjectUnique(PROTOTYPE_QUEST_INDICATOR, GROUP_LEVEL_CARDS, PROTOTYPE_QUEST_INDICATOR)
        self.quest_indicator.setEnable(True)

        quest_indicator_node = self.quest_indicator.getEntityNode()
        quest_indicator_slot = self.movie.getMovieSlot(SLOT_QUEST_INDICATOR)
        quest_indicator_slot.addChild(quest_indicator_node)

    # - Quest Progress Bar ---------------------------------------------------------------------------------------------

    def _setupQuestProgressBar(self):
        player_data = GameManager.getPlayerGameData()
        current_chapter_data = player_data.getCurrentChapterData()
        blocked_levels_data = current_chapter_data.getBlockedLevelsData()

        if self.level_id not in blocked_levels_data.keys():
            return

        level_params = GameManager.getLevelParams(self.level_id)
        level_qp_to_unlock = level_params.QuestPointsToUnlock

        current_level_data = current_chapter_data.getLevelData(self.level_id)
        current_level_qp = current_level_data.getQuestPoints()

        if current_level_qp >= level_qp_to_unlock:
            return

        quest_progress_percent = float(current_level_qp) / float(level_qp_to_unlock) * 100.0

        self.quest_progress_bar = GroupManager.generateObjectUnique(PROTOTYPE_QUEST_PROGRESS_BAR, GROUP_LEVEL_CARDS, PROTOTYPE_QUEST_PROGRESS_BAR)
        self.quest_progress_bar.setEnable(True)
        self.quest_progress_bar.setValue(quest_progress_percent)
        self.quest_progress_bar.setText_ID(TEXT_QUEST_PROGRESS_BAR)

        quest_progress_bar_node = self.quest_progress_bar.getEntityNode()
        quest_progress_bar_slot = self.movie.getMovieSlot(SLOT_QUEST_PROGRESS_BAR)
        quest_progress_bar_slot.addChild(quest_progress_bar_node)

        self._setupQuestProgressBarFollower(quest_progress_percent)

    def updateQuestProgressBar(self, value):
        if self.quest_progress_bar is not None:
            self.quest_progress_bar.setValue(value)

    def _setupQuestProgressBarFollower(self, current_progress_value=0.0):
        self.quest_progress_value_follower = Mengine.createValueFollowerLinear(
            current_progress_value,
            QUEST_PROGRESS_BAR_FOLLOW_SPEED,
            self.updateQuestProgressBar
        )

    def addQuestProgress(self, progress):
        current_value = self.quest_progress_value_follower.getFollow()
        new_value = current_value + progress

        self.setQuestProgress(new_value)

    def setQuestProgress(self, progress):
        self.quest_progress_value_follower.setFollow(progress)

    def destroyQuestProgressBar(self):
        if self.quest_progress_bar is not None:
            self.quest_progress_bar.onDestroy()
            self.quest_progress_bar = None

        if self.quest_progress_value_follower is not None:
            Mengine.destroyValueFollower(self.quest_progress_value_follower)
            self.quest_progress_value_follower = None

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

    def scopeProgressOnQuestBar(self, source, new_qp):
        level_params = GameManager.getLevelParams(self.level_id)
        level_qp_to_unlock = level_params.QuestPointsToUnlock

        progress_value = float(new_qp) / float(level_qp_to_unlock) * 100.0

        current_value = self.quest_progress_value_follower.getFollow()
        future_value = current_value + progress_value

        player_data = GameManager.getPlayerGameData()
        current_chapter_data = player_data.getCurrentChapterData()
        current_level_data = current_chapter_data.getLevelData(self.level_id)

        source.addFunction(current_level_data.addQuestPoints, new_qp)
        source.addFunction(self.addQuestProgress, progress_value)

        with source.addIfTask(lambda: future_value >= 100.0) as (unlock, _):
            unlock.addFunction(current_level_data.setActive, True)
            unlock.addScope(self.scopeUnlockLevelCardAnim)

    def scopeUnlockLevelCardAnim(self, source):
        quest_indicator_node = self.quest_progress_bar.getEntityNode()

        with source.addParallelTask(2) as (scale, alpha):
            scale.addTask("TaskNodeScaleTo", Node=quest_indicator_node, To=(0.0, 0.0, 0.0), Time=500.0)
            alpha.addTask("TaskNodeAlphaTo", Node=quest_indicator_node, To=0.0, Time=500.0)

        source.addFunction(self.destroyQuestProgressBar)

        source.addScope(self.scopeChangeLevelState, self.STATE_UNLOCKING)

        source.addFunction(self._setupQuestIndicator)
        source.addScope(self.scopeQuestIndicatorAnim)

    def scopeQuestIndicatorAnim(self, source):
        if self.quest_indicator is None:
            return
        quest_indicator_node = self.quest_indicator.getEntityNode()

        with source.addParallelTask(2) as (scale, alpha):
            scale.addTask("TaskNodeScaleTo", Node=quest_indicator_node, From=(0.0, 0.0, 0.0), To=(1.0, 1.0, 1.0), Time=250.0)
            alpha.addTask("TaskNodeAlphaTo", Node=quest_indicator_node, From=0.0, To=1.0, Time=250.0)
