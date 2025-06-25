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
        self.content = None
        self.tcs = []
        self.miss_click = None
        self.search_level = None
        self.search_panel = None
        self.game_area_layout = None

        self.search_slot = {}
        self.layout_metrics = {
            "banner_height": 50.0,
            "header_height": 280.0,
            "frame_points_search_level": Mengine.vec4f(
                783.0,
                280.0,
                1953.0,
                1820.0
            ),
            "search_level": Mengine.vec2f(
                1170,
                1540
            ),
            "search_panel": Mengine.vec2f(
                1100.0,
                662.0
            ),
            "spacer_height": 3.0,
            "viewport": {
                "begin": Mengine.vec2f(783.0, 280.0),
                "end": Mengine.vec2f(1953.0, 1820.0)
            },
            "x_center": 1368.0,
        }

    # - Object ----------------------------------------------------------------------------------------------------

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)
        Type.addAction(Type, "ChapterId")
        Type.addAction(Type, "LevelId")
        Type.addAction(Type, "QuestIndex")
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

        self._initSearchPanel()
        self._initMissClick()
        self._initSearchLevel()
        self._initLayout()

        self.search_panel.onInitialize2()

        self._attachMissClick()

        self._runTaskChains()
        self._handleCheats()

    def _onDeactivate(self):
        super(GameArea, self)._onDeactivate()
        self.content = None

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
        self.miss_click = MissClick()
        self.miss_click.onInitialize(self, self.layout_metrics["frame_points_search_level"])

    def _attachMissClick(self):
        miss_click_size = self.miss_click.getSize()
        pos_y = self.layout_metrics["viewport"]["begin"].y + self.layout_metrics["header_height"] + miss_click_size.y / 2

        miss_click_slot = self.content.getMovieSlot(SLOT_MISS_CLICK)
        miss_click_slot.setWorldPosition(Mengine.vec2f(self.layout_metrics["x_center"], pos_y))
        self.miss_click.attachTo(miss_click_slot)

    # - SearchLevel ----------------------------------------------------------------------------------------------------

    def _initSearchLevel(self):
        self.search_level = SearchLevel()
        self.search_level.onInitialize(self, self.layout_metrics["frame_points_search_level"])
        self.search_slot[SLOT_SEARCH_LEVEL] = self.search_level

    # - SearchPanel ----------------------------------------------------------------------------------------------------

    def _initSearchPanel(self):
        self.search_panel = SearchPanel()
        self.search_panel.onInitialize(self)
        self.search_slot[SLOT_SEARCH_PANEL] = self.search_panel

    # - Layout ---------------------------------------------------------------------------------------------------------

    def _initLayout(self):
        self.game_area_layout = Mengine.createLayout()
        self.game_area_layout.setLayoutSizer(lambda: Mengine.getGameViewport().getHeight())

        layout_config = [
            ("Header", self.layout_metrics["header_height"]),
            ("Spacer_1", self.layout_metrics["spacer_height"]),
            (SLOT_SEARCH_LEVEL, "dynamic"),
            ("Spacer_2", self.layout_metrics["spacer_height"]),
            (SLOT_SEARCH_PANEL, "dynamic"),
            ("Spacer_3", self.layout_metrics["spacer_height"]),
            ("Banner", self.layout_metrics["banner_height"]),
        ]

        for name, value in layout_config:
            if value == "dynamic":
                self._addVisualLayoutElement(name)
            else:
                self._addLayoutOnlyElement(name, value)

    def _addVisualLayoutElement(self, element_name):
        height_getters = {
            SLOT_SEARCH_LEVEL: lambda: self.layout_metrics["search_level"].y,
            SLOT_SEARCH_PANEL: lambda: self.layout_metrics["search_panel"].y,
        }

        height_fn = height_getters.get(element_name)

        if height_fn is None:
            Trace.msg_err("GameArea: There is no {!r} element".format(element_name))

        self.game_area_layout.addLayoutElement(
            element_name,
            True,
            0.0,
            True,
            height_fn,
            lambda offset, size: self._setSearchElement(element_name, offset, size)
        )

    def _addLayoutOnlyElement(self, element_name, element_height):
        self.game_area_layout.addLayoutElement(
            element_name,
            True,
            0.0,
            True,
            lambda: element_height,
            lambda offset, size: None
        )

    def _setSearchElement(self, slot_name, offset, size):
        movie_slot = self.content.getMovieSlot(slot_name)
        pos_y = offset + size / 2.0

        movie_slot.setWorldPosition(Mengine.vec2f(self.layout_metrics["x_center"], pos_y))
        self.search_slot[slot_name].attachTo(movie_slot)

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

    def _handleCheats(self):
        if Mengine.hasOption("cheats") is False:
            return

        Trace.msg(" Game cheats ".center(50, "-"))
        Trace.msg(" W - win game")
        Trace.msg(" Q - lose game")
        Trace.msg("".center(50, "-"))

        with self._createTaskChain("CheatLevelEnd") as tc:
            with tc.addRaceTask(2) as (win, lose):
                win.addTask("TaskKeyPress", Keys=[Mengine.KC_W])
                win.addNotify(Notificator.onLevelEnd, True)
                lose.addTask("TaskKeyPress", Keys=[Mengine.KC_Q])
                lose.addNotify(Notificator.onLevelEnd, False)

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
            if self.search_panel.va_range_points[0].x <= panel_item_pos.x <= self.search_panel.va_range_points[1].x:
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
            if self.search_panel.va_range_points[0].x <= panel_item_pos.x <= self.search_panel.va_range_points[1].x:
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

        # prepare variables for tc
        panel_item_scale = panel_item.getSpriteScale()
        panel_item_sprite = panel_item.getSprite()

        scale_factor = 1.0 / self.search_level.virtual_area.get_scale_factor()
        display_item_scale = Mengine.vec3f(scale_factor, scale_factor, 1.0)

        # destroy/disable level item and run move animation
        source.addFunction(level_item.setEnable, False)
        # source.addFunction(scene_item.onDestroy)

        source.addPrint(" * START SCENE ITEM ANIM")

        with source.addParallelTask(2) as (scale, move):
            scale.addTask("TaskNodeScaleTo", Node=moving_node, Easing=SCENE_ITEM_SCALE_EASING, From=display_item_scale,
                          To=panel_item_scale, Time=SCENE_ITEM_SCALE_TIME)
            move.addTask("TaskNodeBezier2ScreenFollow", Node=moving_node, Easing=SCENE_ITEM_MOVE_EASING,
                         Follow=panel_item_sprite, Time=SCENE_ITEM_MOVE_TIME)

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
        source.addFunction(self.search_level.virtual_area.set_scale, 1.0)
        source.addFunction(self.search_panel.hint.decHintCount)
        source.addFunction(self.search_panel.switchHints)

        source.addFunction(self.search_panel.hint.button.movie.setBlock, True)
        source.addFunction(self.search_panel.virtual_area.freeze, True)
        source.addFunction(self.search_level.virtual_area.freeze, True)

        source.addScope(self.search_panel.hint.hint_effect.show, hint_item_transformation)
        source.addTask("TaskItemClick", Item=self.search_panel.hint.hint_item, AutoEnable=False)
        source.addScope(self.search_panel.hint.hint_effect.hide, hint_item_transformation)

        source.addFunction(self.search_panel.hint.cleanHintItem)

        source.addFunction(self.search_panel.hint.button.movie.setBlock, False)
        source.addFunction(self.search_panel.virtual_area.freeze, False)
        source.addFunction(self.search_level.virtual_area.freeze, False)
