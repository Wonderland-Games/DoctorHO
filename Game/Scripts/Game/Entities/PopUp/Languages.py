from UIKit.Entities.PopUp.PopUpContent import PopUpContent
from UIKit.Managers.PrototypeManager import PrototypeManager
from Foundation.LanguagesManager import LanguagesManager
from Foundation.TaskManager import TaskManager


SLOT_BUTTONS = "Buttons"
ALIAS_BUTTON = "$UIButton"


class Languages(PopUpContent):
    content_id = "Languages"

    def __init__(self):
        super(Languages, self).__init__()

        self.buttons_list = {}

    # - PopUpContent ---------------------------------------------------------

    def _onInitializeContent(self):
        super(Languages, self)._onInitializeContent()

        self._setupButtons()
        self._setupSlotsPositions()

        self._runTaskChains()

    def _onFinalizeContent(self):
        super(Languages, self)._onFinalizeContent()

        for button in self.buttons_list.values():
            button.onDestroy()

        self.buttons_list = {}

    # - Setup ----------------------------------------------------------------

    def _setupButtons(self):
        current_locale = LanguagesManager.getLocale()
        enable_locales = LanguagesManager.getLocales()

        for locale_name in enable_locales:
            container = self._generateContainer(locale_name)
            if container is None:
                continue

            if current_locale == locale_name:
                container.movie.setBlock(True)

            self._attachObjectToSlot(container, SLOT_BUTTONS)
            self.buttons_list[locale_name] = container

    def _setupSlotsPositions(self):
        objects_list = []
        for (key, button) in self.buttons_list.items():
            objects_list.append({key: button})

        self.setupObjectsSlotsAsTable(objects_list, False)

    # - TaskChain ------------------------------------------------------------

    def _runTaskChains(self):
        with self._createTaskChain(SLOT_BUTTONS) as tc:
            for (lang, button), tc_race in tc.addRaceTaskList(self.buttons_list.items()):
                tc_race.addTask("TaskMovie2ButtonClick", Movie2Button=button.movie)
                tc_race.addFunction(self._changeLocale, lang)

    def _createTaskChain(self, name, **params):
        tc = TaskManager.createTaskChain(Name="Languages_"+name, **params)
        self.tcs.append(tc)
        return tc

    def _generateContainer(self, locale_name, **params):
        prototype_name = "{}_{}".format(self.__class__.__name__, SLOT_BUTTONS)
        env_name = "{}_{}_{}".format(self.__class__.__name__, SLOT_BUTTONS, locale_name)

        container = PrototypeManager.generateObjectContainer(prototype_name, **params)
        if container is None:
            return None

        container.setTextAliasEnvironment(env_name)
        container.setEnable(True)

        text_id = LanguagesManager.getLanguageTextId(locale_name)
        if text_id is None:
            return None

        Mengine.setTextAlias(env_name, ALIAS_BUTTON, text_id)

        return container

    def _changeLocale(self, locale):
        if LanguagesManager.getLocale() == locale:
            Trace.msg("Current locale {!r} is already set!".format(locale))
            return

        if LanguagesManager.hasLocale(locale) is False:
            Trace.msg("Can't set locale to {!r} - not exists in game".format(locale))
            return

        if Mengine.getCurrentScene() is None:
            LanguagesManager.setLocale(locale)
        else:
            def cbOnSceneRestartChangeLocale(scene, isActive, isError):
                if scene is None:
                    LanguagesManager.setLocale(locale)

            Mengine.restartCurrentScene(True, cbOnSceneRestartChangeLocale)
