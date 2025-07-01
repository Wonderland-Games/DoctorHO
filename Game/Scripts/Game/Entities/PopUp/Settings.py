from UIKit.Entities.PopUp.PopUpContent import PopUpContent
from Game.Managers.GameManager import GameManager
from Foundation.LayoutBox import LayoutBox


SLOT_SOUND = "Sound"
SLOT_MUSIC = "Music"
SLOT_VIBRATION = "Vibration"
SLOT_LANGUAGES = "Languages"
SLOT_SUPPORT = "Support"
SLOT_CREDITS = "Credits"
SLOT_LOBBY = "Lobby"

LAYOUT_SPACER = "Spacer_{}"


class Settings(PopUpContent):
    content_id = "Settings"

    def __init__(self):
        super(Settings, self).__init__()

        self.checkboxes = {}
        self.buttons = {}

        self.layout = None

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self):
        super(Settings, self)._onInitializeContent()

        # self._setupCheckBoxes()
        self._setupButtons()
        
        # self._setupSlotsPositions()
        # self._adjustLayout()
        self._adjustLayoutBox()

        self._runTaskChains()

    def _onFinalizeContent(self):
        super(Settings, self)._onFinalizeContent()

        for button in self.buttons.values():
            button.onDestroy()
        self.buttons = {}

        for button in self.checkboxes.values():
            button.onDestroy()
        self.checkboxes = {}

        if self.layout is not None:
            Mengine.destroyLayout(self.layout)
            self.layout = None

    # - Layout ---------------------------------------------------------------------------------------------------------

    def _adjustLayout(self):
        self.layout = Mengine.createLayout()

        def _getContentSizeY():
            content_size = self.pop_up_base.getContentSize()
            print "[= layout.setLayoutSizer:", content_size.y
            return content_size.y

        self.layout.setLayoutSizer(_getContentSizeY)

        print "[= Buttons:", self.buttons.keys()
        buttons_list = self.buttons.items()
        buttons_list_length = len(buttons_list)
        spacers_count = buttons_list_length + 1
        spacer_percent = 1.0 / (float(spacers_count) + float(buttons_list_length))

        for i, (slot_name, button) in enumerate(buttons_list):
            def _getButtonSizeY():
                button_size = button.getSize()
                return button_size.y

            def _cbSetOffsetPosY(_slot_name):
                return lambda offset, size: self._setButtonOffsetPosY(_slot_name, offset, size)

            print "[= layout.addLayoutElement:", "Spacer_{}".format(i)
            self.layout.addLayoutElement(
                LAYOUT_SPACER.format(i),
                False,
                spacer_percent,
                True,
                lambda: 0.0,
                None
            )

            print "[= layout.addLayoutElement:", slot_name
            self.layout.addLayoutElement(
                slot_name,
                True,
                0.0,
                True,
                _getButtonSizeY,
                _cbSetOffsetPosY(slot_name)
            )

            if i == buttons_list_length - 1:
                print "[= layout.addLayoutElement:", "Spacer_{}".format(i+1)
                self.layout.addLayoutElement(
                    LAYOUT_SPACER.format(i+1),
                    False,
                    spacer_percent,
                    True,
                    lambda: 0.0,
                    None
                )

    def _setButtonOffsetPosY(self, slot_name, offset, button_size):
        print "[= _setButtonOffsetPosY:", slot_name, offset, button_size

        slot_button = self.content.getMovieSlot(slot_name)
        content_size = self.pop_up_base.getContentSize()
        slot_button.setLocalPosition(Mengine.vec2f(0.0, -content_size.y/2 + offset + button_size/2))
        print slot_button.getLocalPosition()

    def _adjustLayoutBox(self):
        class BoxElement(object):
            def __init__(self, name, w, h):
                self.name = name
                self.x = 0
                self.y = 0
                self.w = w
                self.h = h

            def getLayoutSize(self):
                return (self.w, self.h)

            def setLayoutOffset(self, offset):
                print "Element: ", self, self.name, " setLayoutOffset", offset
                self.x = offset[0]
                self.y = offset[1]

            def setLayoutSize(self, size):
                self.w = size[0]
                self.h = size[1]

        # element_1 = BoxElement("element_1", 1024, 128)
        # element_2 = BoxElement("element_2", 1024, 128)
        # element_3 = BoxElement("element_3", 1024, 128)
        #
        # print "element_1", element_1
        # print "element_2", element_2
        # print "element_3", element_3
        #
        # def __sizer():
        #     # return (1024, 1024)
        #     content_size = self.pop_up_base.getContentSize()
        #     return (content_size.x, content_size.y)
        #
        # layout_box = LayoutBox(__sizer)
        #
        # with LayoutBox.BuilderVertical(layout_box) as vertical:
        #     vertical.addFixedObject(element_1)
        #     vertical.addPadding(100)
        #     vertical.addFixedObject(element_2)
        #     vertical.addPadding(100)
        #     vertical.addFixedObject(element_3)
        #
        # self.layout_box = layout_box

        def __getContentSize():
            # return (1024, 1024)
            content_size = self.pop_up_base.getContentSize()
            return (content_size.x, content_size.y)

        layout_box = LayoutBox(__getContentSize)
        self.layout_box = layout_box

        buttons_list = self.buttons.items()
        buttons_list_length = len(buttons_list)

        for i, (slot_name, button) in enumerate(buttons_list):
            button_size = button.getSize()
            box_element = BoxElement(slot_name, button_size.x, button_size.y)

            with LayoutBox.BuilderVertical(layout_box) as vertical:
                if i == 0:
                    vertical.addPadding(25)

                vertical.addFixedObject(box_element)

                if i == buttons_list_length - 1:
                    vertical.addPadding(25)
                else:
                    vertical.addPadding(100)

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

        current_level_id = GameManager.getCurrentGameParam("LevelId")
        if current_level_id is not None and _DEVELOPMENT is True:
            buttons.append(SLOT_LOBBY)

        for name in buttons:
            container = self._generateContainter(name)
            if container is None:
                continue

            self._attachObjectToSlot(container, name)
            self.buttons[name] = container

    def _setupSlotsPositions(self):
        objects_list = []

        # add checkboxes to objects list
        if len(self.checkboxes) > 0:
            objects_list.append(self.checkboxes)

        # add buttons to objects list
        for (key, button) in self.buttons.items():
            objects_list.append({key: button})

        self.setupObjectsSlotsAsTable(objects_list)

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
