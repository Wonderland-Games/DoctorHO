from UIKit.Entities.PopUp.PopUpContent import PopUpContent


SLOT_LOBBY = "Lobby"


class LevelWon(PopUpContent):
    content_id = "LevelWon"

    def __init__(self):
        super(LevelWon, self).__init__()

        self.buttons = {}

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self):
        super(LevelWon, self)._onInitializeContent()

        self._setupButtons()
        self._setupSlotsPositions()

        self._runTaskChains()

    def _onFinalizeContent(self):
        super(LevelWon, self)._onFinalizeContent()

        for button in self.buttons.values():
            button.onDestroy()
        self.buttons = {}

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupButtons(self):
        buttons = [SLOT_LOBBY]

        for name in buttons:
            container = self._generateContainter(name)
            if container is None:
                continue

            self._attachObjectToSlot(container, name)
            self.buttons[name] = container

    def _setupSlotsPositions(self):
        objects_list = []
        for (key, button) in self.buttons.items():
            objects_list.append({key: button})

        self.setupObjectsSlotsAsTable(objects_list)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _runTaskChains(self):
        button_lobby = self.buttons.get(SLOT_LOBBY)
        if button_lobby is not None:
            with self._createTaskChain(SLOT_LOBBY) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=button_lobby.movie)
                tc.addScope(self._scopeLobby)

    def _scopeLobby(self, source):
        source.addNotify(Notificator.onPopUpHide)
        source.addNotify(Notificator.onChangeScene, SLOT_LOBBY)
