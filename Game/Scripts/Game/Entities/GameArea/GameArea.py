from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.GroupManager import GroupManager


MOVIE_CONTENT = "Movie2_Content"
SLOT_LEVEL = "level"


class GameArea(BaseEntity):
    def __init__(self):
        super(GameArea, self).__init__()
        self.content = None
        self.tcs = []

    def _onPreparation(self):
        self.content = self.object.getObject(MOVIE_CONTENT)
        if self.content is None:
            return

        self.__attachLevelSceneToSlot("01_Forest")

    def __attachLevelSceneToSlot(self, level_name):
        level_slot = self.content.getMovieSlot(SLOT_LEVEL)
        level_group = GroupManager.getGroup(level_name)

        level_group_scene = level_group.getScene()
        level_group_scene_layer = level_group_scene.getParent()
        level_group_scene_layer_size = level_group_scene_layer.getSize()
        level_group_scene_layer_new_pos = Mengine.vec2f(-level_group_scene_layer_size.x / 2, -level_group_scene_layer_size.y / 2)

        level_slot.addChild(level_group_scene_layer)
        level_group_scene_layer.setLocalPosition(level_group_scene_layer_new_pos)

        level_group_scene.enable()

    def _onActivate(self):
        self._runTaskChains()

    def _onDeactivate(self):
        self.content = None

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base+"_"+name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        pass
