from UIKit.Entities.PopUp.PopUpContent import PopUpContent
from UIKit.Managers.PrototypeManager import PrototypeManager
from Foundation.LanguagesManager import LanguagesManager
from Foundation.SystemManager import SystemManager
from Foundation.DefaultManager import DefaultManager
from Foundation.TaskManager import TaskManager


SLOT_BUTTONS = "Buttons"
ALIAS_BUTTON = "$UIButton"

LANG_OFFSET_X = DefaultManager.getDefaultFloat("LanguagesOffsetX", 270.0)
LANG_OFFSET_Y = DefaultManager.getDefaultFloat("LanguagesOffsetY", 180.0)


class Languages(PopUpContent):
    content_id = "Languages"

    def __init__(self):
        super(Languages, self).__init__()

        self.buttons_list = {}

    # - PopUpContent ---------------------------------------------------------------------------------------------------

    def _onInitializeContent(self):
        super(Languages, self)._onInitializeContent()

        self._setupButtons()
        self._setupSlotsPositions()
        #self._setButtonsPosition_2()

        self._runTaskChains()

    def _onFinalizeContent(self):
        super(Languages, self)._onFinalizeContent()

        for button in self.buttons_list.values():
            button.onDestroy()

        self.buttons_list = {}

    # - Setup ----------------------------------------------------------------------------------------------------------

    def _setupButtons(self):
        #self._changeLocale(locale)
        locales = LanguagesManager.getLocales()
        print(locales)

        for name in locales:

            container = self._generateContainer(name)
            if container is None:
                continue

            self._attachObjectToSlot(container, SLOT_BUTTONS)
            self.buttons_list[name] = container

    def _setupSlotsPositions(self):
        objects_list = []
        for (key, button) in self.buttons_list.items():
            objects_list.append({key: button})

        self._setButtonsPosition(objects_list)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _runTaskChains(self):
        with self._createTaskChain(SLOT_BUTTONS) as tc:
            for (lang, button), tc_race in tc.addRaceTaskList(self.buttons_list.items()):
                tc_race.addTask("TaskMovie2ButtonClick", Movie2Button=button.movie)
                tc_race.addFunction(self._changeLocale, lang)

    def _createTaskChain(self, name, **params):
        tc = TaskManager.createTaskChain(Name="Languages_"+name, **params)
        self.tcs.append(tc)
        return tc

    def _generateContainer(self, name, **params):
        prototype_name = "{}_{}".format(self.__class__.__name__, SLOT_BUTTONS)
        env_name = "{}_{}_{}".format(self.__class__.__name__, SLOT_BUTTONS, name)

        container = PrototypeManager.generateObjectContainer(prototype_name, **params)
        if container is None:
            return None

        container.setTextAliasEnvironment(env_name)
        container.setEnable(True)

        text_id = LanguagesManager.getLanguageTextId(name)
        if text_id is None:
            return None

        Mengine.setTextAlias(env_name, ALIAS_BUTTON, text_id)

        return container


    def _setButtonsPosition(self, objects_list):
        # prepare variables
        content_size = self.pop_up_base.getContentSize()
        start_pos = Mengine.vec2f(0, 0)
        start_pos -= content_size / 2

        # setup objects between each other
        current_size_y = 0
        objects_len_y = len(objects_list)
        for row in objects_list:

            current_size_x = 0
            maximum_size_y = 0

            for key, obj in row.items():
                obj_pos = obj.getLocalPosition()
                obj_pos += start_pos

                obj_size = obj.getSize()
                obj_pos += obj_size / 2

                obj_pos.x += current_size_x
                obj_pos.y += current_size_y

                obj_slot = obj.getEntityNode()
                obj_slot.setLocalPosition(obj_pos)

                current_size_x += obj_size.x
                if maximum_size_y < obj_size.y:
                    maximum_size_y = obj_size.y

            current_size_y += maximum_size_y

        # calc offset y
        available_space_y = content_size.y - current_size_y
        offset_y = available_space_y / (objects_len_y + 1)

        # adding offsets between objects
        for y, row in enumerate(objects_list):
            current_size_x = 0
            objects_len_x = len(row.items())

            # add offset y
            for key, obj in row.items():
                old_pos = obj.getLocalPosition()
                new_pos = Mengine.vec2f(old_pos.x, old_pos.y + offset_y * (y + 1))
                obj.setLocalPosition(new_pos)

                obj_size = obj.getSize()
                current_size_x += obj_size.x

            # calc offset x
            available_space_x = content_size.x - current_size_x
            offset_x = available_space_x / (objects_len_x + 1)

            # add offset x
            for x, (key, obj) in enumerate(row.items()):
                old_pos = obj.getLocalPosition()
                new_pos = Mengine.vec2f(old_pos.x + offset_x * (x + 1), old_pos.y)
                obj.setLocalPosition(new_pos)

    def _changeLocale(self, locale):
        if LanguagesManager.getLocale() == locale:
            # already set to this locale
            return

        if LanguagesManager.hasLocale(locale) is False:
            Trace.log("System", 2, "Can't set locale to {} - not exists in game".format(locale))
            return

        if Mengine.getCurrentScene() is None:
            LanguagesManager.setLocale(locale)
        else:
            def cbOnSceneRestartChangeLocale(scene, isActive, isError):
                if scene is None:
                    LanguagesManager.setLocale(locale)

            Mengine.restartCurrentScene(True, cbOnSceneRestartChangeLocale)
