from UIKit.Entities.PopUp.PopUpContent import PopUpContent, LayoutBox
from Game.Managers.GameManager import GameManager


SLOT_ICON = "Icon"
SLOT_ADVERT = "Ad"
SLOT_RESTART = "Restart"
SLOT_LOBBY = "Lobby"


class LevelLost(PopUpContent):
    content_id = "LevelLost"

    def __init__(self):
        super(LevelLost, self).__init__()

        self.icon = None
        self.buttons = {}

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self):
        super(LevelLost, self)._onInitializeContent()

        self._setupIcon()
        self._setupButtons()
        self._setupLayoutBox()

        self._runTaskChains()

    def _onFinalizeContent(self):
        super(LevelLost, self)._onFinalizeContent()

        if self.icon is not None:
            self.icon.onDestroy()
            self.icon = None

        for button in self.buttons.values():
            button.onDestroy()
        self.buttons = {}

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupIcon(self):
        self.icon = self._generateContainter(SLOT_ICON)
        if self.icon is None:
            return

        self._attachObjectToSlot(self.icon, SLOT_ICON)

    def _setupButtons(self):
        buttons = [SLOT_ADVERT, SLOT_RESTART, SLOT_LOBBY]

        for name in buttons:
            container = self._generateContainter(name)
            if container is None:
                continue

            self._attachObjectToSlot(container, name)
            self.buttons[name] = container

    def _setupLayoutBox(self):
        with LayoutBox.BuilderVertical(self.layout_box) as vertical:
            vertical.addPadding(1)
            vertical.addFixedObject(self.icon)
            vertical.addPadding(1)
            vertical.addFixedObject(self.buttons[SLOT_ADVERT])
            vertical.addPadding(1)
            vertical.addFixedObject(self.buttons[SLOT_RESTART])
            vertical.addPadding(1)
            vertical.addFixedObject(self.buttons[SLOT_LOBBY])
            vertical.addPadding(1)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _runTaskChains(self):
        button_ad = self.buttons.get(SLOT_ADVERT)
        if button_ad is not None:
            with self._createTaskChain(SLOT_ADVERT) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=button_ad.movie)
                tc.addScope(self._scopeAdvertisement)

        button_restart = self.buttons.get(SLOT_RESTART)
        if button_restart is not None:
            with self._createTaskChain(SLOT_RESTART) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=button_restart.movie)
                tc.addScope(self._scopeRestart)

        button_lobby = self.buttons.get(SLOT_LOBBY)
        if button_lobby is not None:
            with self._createTaskChain(SLOT_LOBBY) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=button_lobby.movie)
                tc.addScope(self._scopeLobby)

    def _scopeAdvertisement(self, source):
        source.addNotify(Notificator.onPopUpHide)
        source.addNotify(Notificator.onCallRewardedAd, "Lives")

    def _scopeRestart(self, source):
        level_id = GameManager.getCurrentGameParam("LevelId")

        source.addNotify(Notificator.onPopUpHide)
        source.addFunction(GameManager.removeGame)
        source.addFunction(GameManager.prepareGame, level_id)
        source.addFunction(Mengine.restartCurrentScene, True, None)

    def _scopeLobby(self, source):
        source.addNotify(Notificator.onPopUpHide)
        source.addFunction(GameManager.removeGame)
        source.addNotify(Notificator.onChangeScene, SLOT_LOBBY)
