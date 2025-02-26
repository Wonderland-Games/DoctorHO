from UIKit.Entities.PopUp.PopUpContent import PopUpContent
from UIKit.Managers.PrototypeManager import PrototypeManager


SLOT_SOUND = "sound"
SLOT_MUSIC = "music"
SLOT_VIBRATION = "vibration"
SLOT_LANGUAGES = "languages"
SLOT_SUPPORT = "support"
SLOT_CREDITS = "credits"
SLOT_VERSION = "version"


class Settings(PopUpContent):
    popup_id = "Settings"
    title_text_id = "ID_PopUpTitle_Settings"
    content_movie_name = "Movie2_Content_" + popup_id

    def __init__(self):
        super(Settings, self).__init__()

        self.checkboxes = {}
        self.buttons = {}

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self):
        super(Settings, self)._onInitializeContent()

        self._fillCheckboxes()
        self._fillButtons()
        self._setupSlotsPositions()

        self._runTaskChains()

    def _onFinalizeContent(self):
        super(Settings, self)._onFinalizeContent()

        for button in self.buttons.values():
            button.onDestroy()
        self.buttons = {}

        for button in self.checkboxes.values():
            button.onDestroy()
        self.checkboxes = {}

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _generateContainter(self, name):
        container = PrototypeManager.generateObjectContainer("Settings", Size=name)
        if container is None:
            return None

        container.setTextAliasEnvironment(name)
        container.setEnable(True)

        return container

    def _attachObjectToSlot(self, obj, name):
        object_node = obj.getEntityNode()
        slot = self.content.getMovieSlot(name)
        slot.addChild(object_node)

    def _fillCheckboxes(self):
        checkboxes = [SLOT_SOUND, SLOT_MUSIC, SLOT_VIBRATION]

        for name in checkboxes:
            container = self._generateContainter(name)
            if container is None:
                continue

            self._attachObjectToSlot(container, name)
            self.checkboxes[name] = container

    def _fillButtons(self):
        buttons = [SLOT_LANGUAGES, SLOT_SUPPORT, SLOT_CREDITS]

        for name in buttons:
            container = self._generateContainter(name)
            if container is None:
                continue

            self._attachObjectToSlot(container, name)
            self.buttons[name] = container

    def _setupSlotsPositions(self):
        pass

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _runTaskChains(self):
        checkbox_sound = self.checkboxes.get(SLOT_SOUND)
        if checkbox_sound is not None:
            with self._createTaskChain(SLOT_SOUND, Repeat=True) as tc:
                with tc.addRaceTask(2) as (true, false):
                    true.addTask("TaskMovie2CheckBox", Movie2CheckBox=checkbox_sound.movie, Value=True)
                    true.addScope(self._scopeSound, checkbox_sound.movie, True)

                    false.addTask("TaskMovie2CheckBox", Movie2CheckBox=checkbox_sound.movie, Value=False)
                    false.addScope(self._scopeSound, checkbox_sound.movie, False)

        checkbox_music = self.checkboxes.get(SLOT_MUSIC)
        if checkbox_music is not None:
            with self._createTaskChain(SLOT_MUSIC, Repeat=True) as tc:
                with tc.addRaceTask(2) as (true, false):
                    true.addTask("TaskMovie2CheckBox", Movie2CheckBox=checkbox_music.movie, Value=True)
                    true.addScope(self._scopeMusic, checkbox_music.movie, True)

                    false.addTask("TaskMovie2CheckBox", Movie2CheckBox=checkbox_music.movie, Value=False)
                    false.addScope(self._scopeMusic, checkbox_music.movie, False)

        checkbox_vibration = self.checkboxes.get(SLOT_VIBRATION)
        if checkbox_vibration is not None:
            with self._createTaskChain(SLOT_VIBRATION, Repeat=True) as tc:
                with tc.addRaceTask(2) as (true, false):
                    true.addTask("TaskMovie2CheckBox", Movie2CheckBox=checkbox_vibration.movie, Value=True)
                    true.addScope(self._scopeVibration, checkbox_vibration.movie, True)

                    false.addTask("TaskMovie2CheckBox", Movie2CheckBox=checkbox_vibration.movie, Value=False)
                    false.addScope(self._scopeVibration, checkbox_vibration.movie, False)

        button_languages = self.buttons.get(SLOT_LANGUAGES)
        if button_languages is not None:
            with self._createTaskChain(SLOT_LANGUAGES) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=button_languages.movie)
                tc.addScope(self._scopeLanguages)

        button_support = self.buttons.get(SLOT_SUPPORT)
        if button_support is not None:
            with self._createTaskChain(SLOT_SUPPORT) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=button_support.movie)
                tc.addScope(self._scopeSupport)

        button_credits = self.buttons.get(SLOT_CREDITS)
        if button_credits is not None:
            with self._createTaskChain(SLOT_CREDITS) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=button_credits.movie)
                tc.addScope(self._scopeCredits)

    def _scopeSound(self, source, checkbox, value):
        source.addPrint("{}".format(SLOT_SOUND))

    def _scopeMusic(self, source, checkbox, value):
        source.addPrint("{}".format(SLOT_MUSIC))

    def _scopeVibration(self, source, checkbox, value):
        source.addPrint("{}".format(SLOT_VIBRATION))

    def _scopeLanguages(self, source):
        source.addNotify(Notificator.onPopUpShow, "Languages")

    def _scopeSupport(self, source):
        source.addNotify(Notificator.onPopUpShow, "Support")

    def _scopeCredits(self, source):
        source.addNotify(Notificator.onPopUpShow, "Credits")
