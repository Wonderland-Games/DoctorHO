from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from Game.Entities.GameArea.SearchLevel.SearchLevel import SearchLevel
from Game.Entities.GameArea.SearchLevel.MissClick import MissClick
from Game.Entities.GameArea.SearchPanel.SearchPanel import SearchPanel
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils


MOVIE_CONTENT = "Movie2_Content"
SLOT_MISS_CLICK = "miss_click"
SLOT_SEARCH_LEVEL = "search_level"
SLOT_SEARCH_PANEL = "search_panel"

SCENE_ITEM_MOVE_EASING = "easyCubicIn"
SCENE_ITEM_MOVE_TIME = 1000.0
SCENE_ITEM_SCALE_EASING = "easyBackOut"
SCENE_ITEM_SCALE_TIME = 1000.0


class GameArea(BaseEntity):

    def __init__(self):
        super(GameArea, self).__init__()
        self.tcs = []
        self.miss_click = None
        self.search_level = None
        self.search_panel = None

    # - Object ----------------------------------------------------------------------------------------------------

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        Type.addAction(Type, "GameType")
        Type.addAction(Type, "LevelName")
        Type.addActionActivate(Type, "FoundItems", Append=GameArea._appendFoundItems, Update=GameArea._updateFoundItems)
        Type.addAction(Type, "HintCount")

    def _appendFoundItems(self, id, item):
        print "FOUND ITEMS", self.FoundItems

    def _updateFoundItems(self, list):
        pass

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
        pass

    def _onActivate(self):
        super(GameArea, self)._onActivate()

        self.content = self.object.getObject(MOVIE_CONTENT)
        if self.content is None:
            return

        self._initMissClick()
        self._initSearchLevel()
        self._initSearchPanel()

        self._attachMissClick()
        self._attachSearchLevel()
        self._attachSearchPanel()

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

        if self.miss_click is not None:
            self.miss_click.onFinalize()
            self.miss_click = None

    # - MissClick ------------------------------------------------------------------------------------------------------

    def _initMissClick(self):
        frame = Mengine.getGameViewport()
        frame_points = Mengine.vec4f(frame.begin.x, frame.begin.y, frame.end.x, frame.end.y)

        self.miss_click = MissClick()
        self.miss_click.onInitialize(self, frame_points)

    def _attachMissClick(self):
        _, _, _, _, _, x_center, y_center = AdjustableScreenUtils.getMainSizesExt()

        miss_click_slot = self.content.getMovieSlot(SLOT_MISS_CLICK)
        miss_click_slot.setWorldPosition(Mengine.vec2f(x_center, y_center))
        self.miss_click.attachTo(miss_click_slot)

    # - SearchLevel ----------------------------------------------------------------------------------------------------

    def _initSearchLevel(self):
        frame = Mengine.getGameViewport()
        frame_points = Mengine.vec4f(frame.begin.x, frame.begin.y, frame.end.x, frame.end.y)

        self.search_level = SearchLevel()
        self.search_level.onInitialize(self, self.LevelName, frame_points)

    def _attachSearchLevel(self):
        _, _, _, _, _, x_center, y_center = AdjustableScreenUtils.getMainSizesExt()

        search_level_slot = self.content.getMovieSlot(SLOT_SEARCH_LEVEL)
        search_level_slot.setWorldPosition(Mengine.vec2f(x_center, y_center))
        self.search_level.attachTo(search_level_slot)

    # - SearchPanel ----------------------------------------------------------------------------------------------------

    def _initSearchPanel(self):
        self.search_panel = SearchPanel()
        self.search_panel.onInitialize(self)

    def _attachSearchPanel(self):
        _, game_height, _, _, _, x_center, _ = AdjustableScreenUtils.getMainSizesExt()

        search_panel_size = self.search_panel.getSize()
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
        Notification.notify(Notificator.onLevelStart, self)

        # TEST SETTINGS FEATURE
        with self._createTaskChain("TestColorSettings", Repeat=True) as tc:
            tc.addListener(Notificator.onSettingChange)
            for item, parallel in tc.addParallelTaskList(self.search_level.items):
                parallel.addFunction(self._changeItemColor, item)

    def _changeItemColor(self, item):
        def cb(_, __, ___):
            pass

        color = SETTINGS.Test.color
        sprite = item.getEntity().getSprite()
        sprite.colorTo(500.0, color, "easyLinear", cb)

    def filterItemClick(self, scene_item):
        # check if hint activated and scene_item is hint_item
        hint_item = self.search_panel.hint.hint_item
        if hint_item is not None:
            if hint_item is scene_item:
                return True

            return False

        panel_item = None
        for item in self.search_panel.items:
            if item.item_obj is scene_item:
                panel_item = item
                break

        if panel_item is not None:
            panel_item_node = panel_item.getRoot()
            panel_item_pos = Mengine.getNodeScreenAdaptPosition(panel_item_node)
            if self.search_panel.items_range[0] <= panel_item_pos.x <= self.search_panel.items_range[1]:
                return True

        return False

    def filterUnavailableItemClick(self, scene_item):
        # check if hint is activated
        hint_item = self.search_panel.hint.hint_item
        if hint_item is not None:
            return False

        # check if scene_item is unavailable in search panel
        panel_item = None
        for item in self.search_panel.items:
            if item.item_obj is scene_item:
                panel_item = item
                break

        if panel_item is not None:
            panel_item_node = panel_item.getRoot()
            panel_item_pos = Mengine.getNodeScreenAdaptPosition(panel_item_node)
            if self.search_panel.items_range[0] <= panel_item_pos.x <= self.search_panel.items_range[1]:
                return False

        # check if scene_item is removing in search panel
        removing_items = self.search_panel.getRemovingItems()
        for panel_item in removing_items:
            if panel_item.item_obj is scene_item:
                return False

        return True

    def moveLevelItemToPanelItem(self, source, level_item):
        # generate level item pure sprite
        level_item_entity = level_item.getEntity()
        level_item_pure = level_item_entity.generatePure()
        level_item_pure.enable()

        # create moving node
        moving_node = Mengine.createNode("Interender")
        moving_node.setName("Temp")

        level_item_entity_sp = level_item_entity.getScreenPosition()
        moving_node.setScreenPosition(level_item_entity_sp, 0.0)

        moving_node.addChild(level_item_pure)

        # attach level item to moving node with position fix
        self.addChild(moving_node)

        # find panel item by object
        panel_item = None
        for item in self.search_panel.items:
            if item.item_obj is not level_item:
                continue

            panel_item = item
            break

        panel_item_root = panel_item.getRoot()

        # prepare variables for tc
        panel_item_scale = panel_item.getSpriteScale()

        # destroy/disable level item and run move animation
        source.addFunction(level_item.setEnable, False)
        # source.addFunction(scene_item.onDestroy)

        source.addPrint(" * START SCENE ITEM ANIM")

        with source.addParallelTask(2) as (scale, move):
            scale.addTask("TaskNodeScaleTo", Node=moving_node, Easing=SCENE_ITEM_SCALE_EASING, To=panel_item_scale,
                          Time=SCENE_ITEM_SCALE_TIME)
            move.addTask("TaskNodeBezier2ScreenFollow", Node=moving_node, Easing=SCENE_ITEM_MOVE_EASING, Follow=panel_item_root,
                         Time=SCENE_ITEM_MOVE_TIME)

        source.addPrint(" * END SCENE ITEM ANIM")

        source.addTask("TaskNodeRemoveFromParent", Node=level_item_pure)
        source.addTask("TaskNodeDestroy", Node=level_item_pure)
        source.addTask("TaskNodeRemoveFromParent", Node=moving_node)
        source.addTask("TaskNodeDestroy", Node=moving_node)

    def showHintEffect(self, source):
        # get random panel item from search panel
        panel_item = self.search_panel.getRandomAvailableItem()
        if panel_item is None:
            return

        # save hint item
        self.search_panel.hint.hint_item = panel_item.item_obj

        # calc item hint point
        hint_point = self.search_panel.hint.hint_item.calcWorldHintPoint()

        # create temp hint node
        temp_hint_node = Mengine.createNode("Interender")
        temp_hint_node.setName("TempHintNode")

        # setting items position to temp node
        self.addChild(temp_hint_node)
        temp_hint_node.setWorldPosition(hint_point)

        # getting transformation from temp node
        hint_item_transformation = temp_hint_node.getTransformation()

        # destroy temp hint node
        temp_hint_node.removeFromParent()
        Mengine.destroyNode(temp_hint_node)

        # hint effect logic
        source.addFunction(self.search_panel.hint.decHintCount)
        source.addFunction(self.search_panel.switchHints)

        source.addFunction(self.search_panel.hint.button.movie.setBlock, True)
        source.addFunction(self.search_panel.virtual_area.freeze, True)
        source.addFunction(self.search_level.virtual_area.freeze, True)

        source.addScope(self.search_panel.hint.hint_effect.show, hint_item_transformation)
        source.addListener(Notificator.onItemClick, Filter=lambda item: item == self.search_panel.hint.hint_item)
        source.addScope(self.search_panel.hint.hint_effect.hide, hint_item_transformation)

        source.addFunction(self.search_panel.hint.cleanHintItem)

        source.addFunction(self.search_panel.hint.button.movie.setBlock, False)
        source.addFunction(self.search_panel.virtual_area.freeze, False)
        source.addFunction(self.search_level.virtual_area.freeze, False)
