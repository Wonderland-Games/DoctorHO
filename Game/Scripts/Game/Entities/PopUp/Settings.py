from UIKit.Entities.PopUp.PopUpContent import PopUpContent, LayoutBox
from Game.Managers.GameManager import GameManager
from Foundation.SceneManager import SceneManager


SLOT_SOUND = "Sound"
SLOT_MUSIC = "Music"
SLOT_VIBRATION = "Vibration"
SLOT_LANGUAGES = "Languages"
SLOT_SUPPORT = "Support"
SLOT_CREDITS = "Credits"
SLOT_LOBBY = "Lobby"
SLOT_QUEST_BACKPACK = "QuestBackpack"


class Settings(PopUpContent):
    content_id = "Settings"

    def __init__(self):
        super(Settings, self).__init__()

        self.checkboxes = {}
        self.buttons = {}

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self):
        super(Settings, self)._onInitializeContent()

        self._setupCheckBoxes()
        self._setupButtons()
        self._setupLayoutBox()

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

    def _setupCheckBoxes(self):
        checkboxes = [SLOT_SOUND, SLOT_MUSIC, SLOT_VIBRATION]

        for name in checkboxes:
            name_capital = name.capitalize()
            container = self._generateContainter(name_capital)
            if container is None:
                continue

            self._attachObjectToSlot(container, name)
            self.checkboxes[name] = container

        self._updateCheckBoxesValues()

    def _updateCheckBoxesValues(self):
        checkbox_sound = self.checkboxes.get(SLOT_SOUND)
        sound_value = Mengine.getCurrentAccountSettingBool("MuteSound")
        if None not in [checkbox_sound, sound_value]:
            checkbox_sound.movie.setParam("Value", sound_value)

        checkbox_music = self.checkboxes.get(SLOT_MUSIC)
        music_value = Mengine.getCurrentAccountSettingBool("MuteMusic")
        if None not in [checkbox_music, music_value]:
            checkbox_music.movie.setParam("Value", music_value)

        checkbox_vibration = self.checkboxes.get(SLOT_VIBRATION)
        if checkbox_vibration is not None:
            if _DEVELOPMENT is True:
                vibration_value = Mengine.getCurrentAccountSettingBool("MuteVibration")
            else:
                vibration_value = Mengine.androidMethod("Vibrator", "isMute")

            if vibration_value is not None:
                checkbox_vibration.movie.setParam("Value", vibration_value)

    def _setupButtons(self):
        buttons = [SLOT_LANGUAGES, SLOT_SUPPORT, SLOT_CREDITS]

        self._addOptionalButtons(buttons)

        for name in buttons:
            container = self._generateContainter(name)
            if container is None:
                continue

            self._attachObjectToSlot(container, name)
            self.buttons[name] = container

    def _setupLayoutBox(self):
        checkbox_slots = [SLOT_SOUND, SLOT_MUSIC, SLOT_VIBRATION]

        # calculate the maximum height of horizontal checkboxes
        checkbox_horizontal_height = 0.0
        for checkbox_slot in checkbox_slots:
            checkbox = self.checkboxes.get(checkbox_slot)
            checkbox_size = checkbox.getSize()
            if checkbox_size.y > checkbox_horizontal_height:
                checkbox_horizontal_height = checkbox_size.y

        button_slots = [SLOT_LANGUAGES, SLOT_SUPPORT, SLOT_CREDITS]
        if SLOT_LOBBY in self.buttons.keys():
            button_slots.append(SLOT_LOBBY)
        if SLOT_QUEST_BACKPACK in self.buttons.keys():
            button_slots.append(SLOT_QUEST_BACKPACK)

        # setup layout
        with LayoutBox.BuilderVertical(self.layout_box) as vertical:
            # top padding
            vertical.addPadding(0.75)

            # add horizontal checkboxes
            with vertical.addLayoutHorizontal(checkbox_horizontal_height) as horizontal:
                horizontal.addPadding(1)
                for checkbox_slot in checkbox_slots:
                    checkbox = self.checkboxes.get(checkbox_slot)
                    horizontal.addFixedObject(checkbox)
                    horizontal.addPadding(1)

            # padding between checkboxes and buttons
            vertical.addPadding(1.75)

            # add vertical buttons
            for index, button_slot in enumerate(button_slots):
                button = self.buttons.get(button_slot)
                vertical.addFixedObject(button)

                if index != len(button_slots) - 1:
                    vertical.addPadding(1)
                else:
                    # bot padding
                    vertical.addPadding(1.5)

    def _addOptionalButtons(self, buttons):
        current_level_id = GameManager.getCurrentGameParam("LevelId")
        if current_level_id is not None and _DEVELOPMENT is True:
            buttons.append(SLOT_LOBBY)

        # If current scene is FinalStage we can return to QuestBackpack
        if SceneManager.isCurrentSceneFinal() and _DEVELOPMENT:
            buttons.append(SLOT_QUEST_BACKPACK)

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
                tc.addScope(self._scopeButton, "Languages")

        button_support = self.buttons.get(SLOT_SUPPORT)
        if button_support is not None:
            with self._createTaskChain(SLOT_SUPPORT) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=button_support.movie)
                tc.addScope(self._scopeButton, "Support")

        button_credits = self.buttons.get(SLOT_CREDITS)
        if button_credits is not None:
            with self._createTaskChain(SLOT_CREDITS) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=button_credits.movie)
                tc.addScope(self._scopeButton, "Credits")

        button_lobby = self.buttons.get(SLOT_LOBBY)
        if button_lobby is not None:
            with self._createTaskChain(SLOT_LOBBY) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=button_lobby.movie)
                tc.addScope(self._scopeLobby)

        button_quest_backpack = self.buttons.get(SLOT_QUEST_BACKPACK)
        if button_quest_backpack is not None:
            with self._createTaskChain(SLOT_QUEST_BACKPACK) as tc:
                tc.addTask("TaskMovie2ButtonClick", Movie2Button=button_quest_backpack.movie)
                tc.addScope(self._scopeQuestBackpack)

    def _scopeSound(self, source, checkbox, value):
        source.addFunction(checkbox.setParam, "Value", value)
        source.addFunction(Mengine.changeCurrentAccountSetting, "MuteSound", unicode(value))

    def _scopeMusic(self, source, checkbox, value):
        source.addFunction(checkbox.setParam, "Value", value)
        source.addFunction(Mengine.changeCurrentAccountSetting, "MuteMusic", unicode(value))

    def _scopeVibration(self, source, checkbox, value):
        source.addFunction(checkbox.setParam, "Value", value)
        if _DEVELOPMENT is True:
            source.addFunction(Mengine.changeCurrentAccountSetting, "MuteVibration", unicode(value))
        else:
            source.addFunction(Mengine.androidMethod, "Vibrator", "mute", value)

    def _scopeButton(self, source, content_id):
        source.addNotify(Notificator.onPopUpShow, content_id)

    def _scopeLobby(self, source):
        source.addNotify(Notificator.onPopUpHide)
        source.addFunction(GameManager.removeGame)
        source.addNotify(Notificator.onChangeScene, SLOT_LOBBY)

    def _scopeQuestBackpack(self, source):
        source.addNotify(Notificator.onPopUpHide)
        source.addFunction(GameManager.removeGame)
        source.addNotify(Notificator.onChangeScene, SLOT_QUEST_BACKPACK)