from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from UIKit.Managers.PrototypeManager import PrototypeManager
from Game.Managers.GameManager import GameManager
from Game.Entities.Lobby.LevelCard import LevelCard


MOVIE_CONTENT = "Movie2_Content"
SLOT_PLAY = "Play"
SLOT_CARDS = "Cards"


class Lobby(BaseEntity):
    def __init__(self):
        super(Lobby, self).__init__()
        self.content = None
        self.tcs = []
        self.buttons = {}
        self.cards = {}

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        self.content = self.object.getObject(MOVIE_CONTENT)
        if self.content is None:
            return

        # self._setupButtons()
        self._setupCards()

    def _onActivate(self):
        self._runTaskChains()

    def _onDeactivate(self):
        self.content = None

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        for button in self.buttons.values():
            button.onDestroy()
        self.buttons = {}

        for card in self.cards.values():
            card.onFinalize()
        self.cards = {}

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupButtons(self):
        prototype_name = self.__class__.__name__ + "_" + SLOT_PLAY
        button = PrototypeManager.generateObjectContainer(prototype_name)
        if button is None:
            return None

        button.setTextAliasEnvironment(prototype_name)
        button.setEnable(True)

        button_node = button.getEntityNode()
        button_slot = self.content.getMovieSlot(SLOT_PLAY)
        button_slot.addChild(button_node)

        self.buttons[SLOT_PLAY] = button

    # - Cards ----------------------------------------------------------------------------------------------------------

    def _setupCards(self):
        levels = ["01_Forest", "02_Atlantis"]

        for i, level_name in enumerate(levels):
            card = LevelCard()
            card.onInitialize(level_name)
            self.cards[level_name] = card

            card_node = card.getRoot()
            card_slot = self.content.getMovieSlot(SLOT_CARDS)
            card_slot.addChild(card_node)

            card_size = card.getSize()
            offset_x = 0
            if i > 0:
                offset_x = 50
            card.setLocalPosition(Mengine.vec2f(card_size.x * i - card_size.x / len(levels) + offset_x, 0))

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base+"_"+name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        button_play = self.buttons.get(SLOT_PLAY)
        if button_play is not None:
            with self._createTaskChain(SLOT_PLAY) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=button_play.movie)
                tc.addScope(self._scopePlay, "01_Forest")

        with self._createTaskChain(SLOT_CARDS) as tc:
            for (level_name, card), race in tc.addRaceTaskList(self.cards.items()):
                race.addTask("TaskMovie2ButtonClick", Movie2Button=card.button)
                race.addScope(self._scopePlay, level_name)

    def _scopePlay(self, source, level_name):
        # source.addNotify(Notificator.onChangeScene, "GameArea")

        GameManager.removeGame()
        GameManager.prepareGame("HO", level_name)
        GameManager.runLevelStartAdvertisement()
