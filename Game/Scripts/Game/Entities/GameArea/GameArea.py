from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Game.Entities.GameArea.SearchLevel import SearchLevel
from Game.Entities.GameArea.SearchPanel.SearchPanel import SearchPanel


MOVIE_CONTENT = "Movie2_Content"
SLOT_LEVEL = "level"
SLOT_SEARCH_PANEL = "search_panel"

SCENE_ITEM_MOVE_EASING = "easyCubicIn"
SCENE_ITEM_MOVE_TIME = 1000.0
SCENE_ITEM_SCALE_EASING = "easyBackOut"
SCENE_ITEM_SCALE_TIME = 1000.0


class GameArea(BaseEntity):
    def __init__(self):
        super(GameArea, self).__init__()
        self.content = None
        self.tcs = []
        self.search_level = None
        self.search_panel = None

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, obj):
        super(GameArea, self)._onInitialize(obj)
        pass

    def _onFinalize(self):
        super(GameArea, self)._onFinalize()
        pass

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        super(GameArea, self)._onPreparation()

        self.content = self.object.getObject(MOVIE_CONTENT)
        if self.content is None:
            return

        # self._initSearchLevel("01_Forest")
        # self._initSearchPanel()
        #
        # self._attachSearchPanel()
        # self._attachSearchLevel()

    def _onActivate(self):
        super(GameArea, self)._onActivate()

        self._initSearchLevel("01_Forest")
        self._initSearchPanel()

        self._attachSearchPanel()
        self._attachSearchLevel()

        self._runTaskChains()

    def _onDeactivate(self):
        super(GameArea, self)._onDeactivate()

        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        if self.search_panel is not None:
            self.search_panel.onFinalize()
            self.search_panel = None

        if self.search_level is not None:
            self.search_level.onFinalize()
            self.search_level = None

        self.content = None

    # - SearchLevel ----------------------------------------------------------------------------------------------------

    def _initSearchLevel(self, level_name):
        frame = Mengine.getGameViewport()
        frame_points = Mengine.vec4f(frame.begin.x, frame.begin.y, frame.end.x, frame.end.y)

        self.search_level = SearchLevel()
        self.search_level.onInitialize(self, level_name, frame_points)

    def _attachSearchLevel(self):
        # from MobileKit.AdjustableScreenUtils import AdjustableScreenUtils
        game_viewport = Mengine.getGameViewport()
        game_width = game_viewport.end.x - game_viewport.begin.x
        game_height = game_viewport.end.y - game_viewport.begin.y
        game_center_x = game_viewport.begin.x + game_width / 2

        search_panel_size = self.search_panel.getSize()
        # Rework pos_y with SETTINGS json
        pos_y = game_viewport.begin.y + game_height / 2
        # pos_y = game_viewport.begin.y + game_height / 2 - search_panel_size.y / 2

        search_level_slot = self.content.getMovieSlot(SLOT_LEVEL)
        search_level_slot.setWorldPosition(Mengine.vec2f(game_center_x, pos_y))

        self.search_level.attachTo(search_level_slot)

        search_level_root = self.search_level.getRoot()
        search_level_root.setLocalPosition(Mengine.vec2f(-game_center_x, -pos_y))

    # - SearchPanel ----------------------------------------------------------------------------------------------------

    def _initSearchPanel(self):
        self.search_panel = SearchPanel()
        self.search_panel.onInitialize(self)

    def _attachSearchPanel(self):
        # from MobileKit.AdjustableScreenUtils import AdjustableScreenUtils
        viewport = Mengine.getGameViewport()
        game_width = viewport.end.x - viewport.begin.x
        game_height = viewport.end.y - viewport.begin.y
        x_center = viewport.begin.x + game_width / 2

        search_panel_size = self.search_panel.getSize()
        # Rework pos_y with SETTINGS json
        pos_y = game_height - search_panel_size.y / 2

        search_panel_slot = self.content.getMovieSlot(SLOT_SEARCH_PANEL)
        search_panel_slot.setWorldPosition(Mengine.vec2f(x_center, pos_y))

        self.search_panel.attachTo(search_panel_slot)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base+"_"+name, **params)
        self.tcs.append(tc)
        return tc

    def _runTaskChains(self):
        # search items in scene logic
        with self._createTaskChain("PickItems", Repeat=True) as tc:
            for item, parallel in tc.addParallelTaskList(self.search_level.items):
                parallel.addTask("TaskItemClick", Item=item, Filter=self._filterItemClick)
                parallel.addPrint(item.getName())
                parallel.addFunction(self.search_level.items.remove, item)
                parallel.addScope(self._playMoveSceneItemToPanelItem, item)
                parallel.addScope(self.search_panel.playRemovePanelItemAnim, item)

        # lives logic
        with self._createTaskChain("Lives", Repeat=True) as tc:
            tc.addEvent(self.search_level.miss_click_event)
            tc.addFunction(self.search_panel.lives_counter.decItemsCount)

        # TEST SETTINGS FEATURE
        with self._createTaskChain("TestColorSettings", Repeat=True) as tc:
            tc.addListener(Notificator.onSettingChange)
            for item, parallel in tc.addParallelTaskList(self.search_level.items):
                parallel.addFunction(self._changeItemColor, item)

    def _filterItemClick(self, scene_item):
        result = False

        available_items = self.search_panel.getAvailableItems()
        if len(available_items) is 0:
            return result

        for panel_item in available_items:
            if panel_item.item_obj is scene_item:
                result = True
                break

        return result

    def _changeItemColor(self, item):
        def cb(_, __, ___):
            pass

        color = SETTINGS.Test.color
        sprite = item.getEntity().getSprite()
        sprite.colorTo(500.0, color, "easyLinear", cb)

    def _playMoveSceneItemToPanelItem(self, source, scene_item):
        # generate scene item pure sprite
        item_entity = scene_item.getEntity()
        item_pure = item_entity.generatePure()
        item_pure.enable()

        # get scene item node with position data
        scene_item_node = scene_item.getEntityNode()
        scene_item_node_pos = scene_item_node.getWorldPosition()
        scene_item_node_center = scene_item.getEntity().getSpriteCenter()
        scene_item_node_pos_true = Mengine.vec2f(scene_item_node_pos.x + scene_item_node_center[0],
                                                 scene_item_node_pos.y + scene_item_node_center[1])

        # create attach node
        moving_node = Mengine.createNode("Interender")
        moving_node.setName("Temp")

        # attach scene item to attach node with position fix
        self.addChild(moving_node)
        moving_node.addChild(item_pure)
        moving_node.setWorldPosition(scene_item_node_pos_true)
        item_pure.setLocalPosition(Mengine.vec2f(-scene_item_node_center[0], -scene_item_node_center[1]))

        # find panel item by object
        panel_item = None
        for item in self.search_panel.items:
            if item.item_obj is not scene_item:
                continue

            panel_item = item
            break

        # prepare variables for tc
        panel_item_scale = panel_item.getSpriteScale()
        pos_from = scene_item_node_pos_true
        pos_to = panel_item.getRootWorldPosition()

        # destroy/disable scene item and run move animation
        source.addFunction(scene_item.setEnable, False)
        # source.addFunction(scene_item.onDestroy)

        source.addPrint("START SCENE ITEM ANIM")

        with source.addParallelTask(2) as (scale, move):
            scale.addTask("TaskNodeScaleTo", Node=moving_node, Easing=SCENE_ITEM_SCALE_EASING, To=panel_item_scale,
                          Time=SCENE_ITEM_SCALE_TIME)
            move.addTask("TaskNodeBezier2To", Node=moving_node, Easing=SCENE_ITEM_MOVE_EASING, From=pos_from, To=pos_to,
                         Time=SCENE_ITEM_MOVE_TIME)

        source.addPrint("END SCENE ITEM ANIM")

        source.addTask("TaskNodeRemoveFromParent", Node=item_pure)
        source.addTask("TaskNodeDestroy", Node=item_pure)
        source.addTask("TaskNodeRemoveFromParent", Node=moving_node)
        source.addTask("TaskNodeDestroy", Node=moving_node)
