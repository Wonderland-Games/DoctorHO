from UIKit.Entities.PopUp.PopUpContent import PopUpContent


class Credits(PopUpContent):
    content_id = "Credits"

    def __init__(self):
        super(Credits, self).__init__()

        self.buttons = {}

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self):
        super(Credits, self)._onInitializeContent()

        self._setupButtons()
        self._setupSlotsPositions()

        self._runTaskChains()

    def _onFinalizeContent(self):
        super(Credits, self)._onFinalizeContent()

        for button in self.buttons.values():
            button.onDestroy()
        self.buttons = {}

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupButtons(self):
        buttons = []

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
        pass
