from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.GroupManager import GroupManager
from Game.Entities.GameArea.SearchPanel import SearchPanel


MOVIE_CONTENT = "Movie2_Content"
SLOT_LEVEL = "level"
SLOT_SEARCH_PANEL = "search_panel"


class GameArea(BaseEntity):
    def __init__(self):
        super(GameArea, self).__init__()
        self.content = None
        self.tcs = []
        self.search_panel = None

    def _onPreparation(self):
        self.content = self.object.getObject(MOVIE_CONTENT)
        if self.content is None:
            return

        self.__attachLevelSceneToSlot("01_Forest")
        self._initSearchPanel()

    def __attachLevelSceneToSlot(self, level_name):
        # from MobileKit.AdjustableScreenUtils import AdjustableScreenUtils
        viewport = Mengine.getGameViewport()
        game_width = viewport.end.x - viewport.begin.x
        game_height = viewport.end.y - viewport.begin.y
        x_center = viewport.begin.x + game_width / 2
        y_center = viewport.begin.y + game_height / 2

        level_slot = self.content.getMovieSlot(SLOT_LEVEL)
        level_slot.setWorldPosition(Mengine.vec2f(x_center, y_center))

        level_group = GroupManager.getGroup(level_name)
        level_group_scene = level_group.getScene()
        level_group_scene_layer = level_group_scene.getParent()
        level_group_scene_layer_size = level_group_scene_layer.getSize()
        level_group_scene_layer_new_pos = Mengine.vec2f(-level_group_scene_layer_size.x / 2, -level_group_scene_layer_size.y / 2)

        level_slot.addChild(level_group_scene_layer)
        level_group_scene_layer.setLocalPosition(level_group_scene_layer_new_pos)

        level_group_scene.enable()

        self.test_item = level_group.getObject("Item_Heart")

        level_group_objects = level_group.getObjects()
        items = [item for item in level_group_objects if item.getEntityType() is "Item"]
        print([item.getName() for item in items])

    def _initSearchPanel(self):
        self.search_panel = SearchPanel()
        self.search_panel.onInitialize(self)

        self._attachSearchPanel()

    def _attachSearchPanel(self):
        # from MobileKit.AdjustableScreenUtils import AdjustableScreenUtils
        viewport = Mengine.getGameViewport()
        game_width = viewport.end.x - viewport.begin.x
        game_height = viewport.end.y - viewport.begin.y
        x_center = viewport.begin.x + game_width / 2

        search_panel_height = self.search_panel.getHeight()

        search_panel_slot = self.content.getMovieSlot(SLOT_SEARCH_PANEL)
        search_panel_slot.setWorldPosition(Mengine.vec2f(
            x_center,
            game_height - search_panel_height/2
        ))

        self.search_panel.attachTo(search_panel_slot)

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
        with self._createTaskChain("PickHeart") as tc:
            tc.addTask("TaskItemClick", Item=self.test_item)
            tc.addPrint("Pick item Heart")
            tc.addTask("TaskItemPick", Item=self.test_item)
        pass
