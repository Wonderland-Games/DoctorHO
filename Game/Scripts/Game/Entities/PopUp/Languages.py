from UIKit.Entities.PopUp.PopUpContent import PopUpContent
from Foundation.LanguagesManager import LanguagesManager
from Foundation.SystemManager import SystemManager

SLOT_BUTTONS = "Buttons"


class Languages(PopUpContent):
    content_id = "Languages"

    def __init__(self):
        super(Languages, self).__init__()

        self.buttons = {}

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self):
        super(Languages, self)._onInitializeContent()

        self._setupButtons()
        self._setupSlotsPositions()

        self._runTaskChains()

    def _onFinalizeContent(self):
        super(Languages, self)._onFinalizeContent()

        for button in self.buttons.values():
            button.onDestroy()
        self.buttons = {}

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupButtons(self):
        #self._changeLocale("en")
        locales = LanguagesManager.getLocales()
        print(locales)

        for name in locales:
            container = self._generateContainter(SLOT_BUTTONS)
            if container is None:
                continue

            text_id = LanguagesManager.getLanguageTextId(name)
            button_text = Mengine.getTextFromId(text_id)
            print(button_text)
            container.setTextAliasEnvironment(button_text)

            self._attachObjectToSlot(container, SLOT_BUTTONS)
            self.buttons[name] = container

    def _setupSlotsPositions(self):
        objects_list = []
        for (key, button) in self.buttons.items():
            objects_list.append({key: button})

        self.setupObjectsSlotsAsTable(objects_list)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _runTaskChains(self):
        pass

    def _changeLocale(self, locale):
        if SystemManager.hasSystem("SystemAutoLanguage"):
            Mengine.changeCurrentAccountSetting("SelectedLanguage", unicode(locale))
            SystemManager.getSystem("SystemAutoLanguage").disable()

        def cbOnSceneRestartChangeLocale(scene, isActive, isError):
            print("Scene: ", scene)
            if scene is None:
                Mengine.setLocale(locale)
                Trace.msg("Locale changed to {!r}".format(locale))

        Mengine.restartCurrentScene(True, cbOnSceneRestartChangeLocale)
