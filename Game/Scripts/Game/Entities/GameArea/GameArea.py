from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Foundation.GroupManager import GroupManager
from Game.Entities.GameArea.SearchPanel.SearchPanel import SearchPanel


MOVIE_CONTENT = "Movie2_Content"
SLOT_LEVEL = "level"
SLOT_SEARCH_PANEL = "search_panel"


class GameArea(BaseEntity):
    def __init__(self):
        super(GameArea, self).__init__()
        self.content = None
        self.tcs = []
        self.search_panel = None
        self.items = []
        self.level_group = None

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

        self.level_group = GroupManager.getGroup(level_name)
        level_group_scene = self.level_group.getScene()
        level_group_scene_layer = level_group_scene.getParent()
        level_group_scene_layer_size = level_group_scene_layer.getSize()
        level_group_scene_layer_new_pos = Mengine.vec2f(-level_group_scene_layer_size.x / 2, -level_group_scene_layer_size.y / 2)

        level_slot.addChild(level_group_scene_layer)
        level_group_scene_layer.setLocalPosition(level_group_scene_layer_new_pos)

        level_group_scene.enable()

        self.test_item = self.level_group.getObject("Item_Heart")

        level_group_objects = self.level_group.getObjects()

        self.items = [item for item in level_group_objects if item.getEntityType() is "Item"]
        print([item.getName() for item in self.items])

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

        search_panel_size = self.search_panel.getSize()

        search_panel_slot = self.content.getMovieSlot(SLOT_SEARCH_PANEL)
        search_panel_slot.setWorldPosition(Mengine.vec2f(
            x_center,
            game_height - search_panel_size.y/2
        ))

        self.search_panel.attachTo(search_panel_slot)

    def _onActivate(self):
        self._runTaskChains()

    def _onDeactivate(self):
        self.content = None

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        if self.search_panel is not None:
            self.search_panel.onFinalize()
            self.search_panel = None

        self.items = []
        self.level_group = None

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base+"_"+name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        # with self._createTaskChain("PickHeart") as tc:
        #     tc.addTask("TaskItemClick", Item=self.test_item)
        #     tc.addPrint("Pick item Heart")
        #     tc.addTask("TaskItemPick", Item=self.test_item)

        with self._createTaskChain("PickItems", Repeat=True) as tc:
            for item, race in tc.addRaceTaskList(self.items):
                race.addTask("TaskItemClick", Item=item)
                race.addPrint(item.getName())
                with race.addParallelTask(2) as (scene, panel):
                    scene.addTask("TaskItemPick", Item=item)
                    scene.addFunction(self.items.remove, item)
                    panel.addFunction(self.search_panel.removeItem, item)

        # with self._createTaskChain("Test") as tc:
        #     tc.addDelay(2000)
        #     tc.addPrint("disable interactive for {}".format(self.items[0].getName()))
        #     tc.addPrint("{}".format(self.items[0].getInteractive()))
        #     tc.addFunction(self.items[0].setInteractive, False)
