from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from UIKit.Managers.PrototypeManager import PrototypeManager


MOVIE_CONTENT = "Movie2_Content"
SLOT_PLAY = "Play"


class Lobby(BaseEntity):
    def __init__(self):
        super(Lobby, self).__init__()
        self.content = None
        self.tcs = []
        self.buttons = {}

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        self.content = self.object.getObject(MOVIE_CONTENT)
        if self.content is None:
            return

        self._setupButtons()

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
                tc.addScope(self._scopePlay)

    def _scopePlay(self, source):
        source.addNotify(Notificator.onChangeScene, "GameArea")
