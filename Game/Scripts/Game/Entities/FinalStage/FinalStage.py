from Foundation.Entity.BaseEntity import BaseEntity
from Foundation.TaskManager import TaskManager
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils


SLOT_DROP_LEVEL = "drop_level"
SLOT_DROP_PANEL = "drop_panel"


class FinalStage(BaseEntity):

    def __init__(self):
        super(FinalStage, self).__init__()
        self.content = None
        self.tcs = []
        self.miss_click = None
        self.search_level = None
        self.search_panel = None

    # - Object ----------------------------------------------------------------------------------------------------

    @staticmethod
    def declareORM(Type):
        BaseEntity.declareORM(Type)

    def _appendFoundItems(self, id, item):
        print("FOUND ITEMS".format(self.FoundItems))

    def _updateFoundItems(self, list):
        pass

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self, obj):
        super(FinalStage, self)._onInitialize(obj)
        pass

    def _onFinalize(self):
        super(FinalStage, self)._onFinalize()
        pass

    # - BaseEntity -----------------------------------------------------------------------------------------------------

    def _onPreparation(self):
        super(FinalStage, self)._onPreparation()
        pass

    def _onActivate(self):
        super(FinalStage, self)._onActivate()

        '''
        self._initSearchPanel()
        self._initSearchLevel()

        self.search_panel.onInitialize2()

        self._attachSearchLevel()
        self._attachSearchPanel()

        self._runTaskChains()
        self._handleCheats()
        '''

    def _onDeactivate(self):
        super(FinalStage, self)._onDeactivate()
        '''
        for tc in self.tcs:
            tc.cancel()
        self.tcs = []

        if self.search_panel is not None:
            self.search_panel.onFinalize()
            self.search_panel = None

        if self.search_level is not None:
            self.search_level.onFinalize()
            self.search_level = None

        '''

    # - SearchLevel ----------------------------------------------------------------------------------------------------

    def _initSearchLevel(self):
        search_panel_size = self.search_panel.getSize()
        _, _, header_height, banner_height, viewport, _, _ = AdjustableScreenUtils.getMainSizesExt()

        frame_begin_x = viewport.begin.x
        frame_begin_y = viewport.begin.y + header_height
        frame_end_x = viewport.end.x
        frame_end_y = viewport.end.y - banner_height - search_panel_size.y
        frame_points = Mengine.vec4f(frame_begin_x, frame_begin_y, frame_end_x, frame_end_y)

        self.search_level = SearchLevel()
        self.search_level.onInitialize(self, frame_points)

    def _attachSearchLevel(self):
        _, _, header_height, _, viewport, x_center, _ = AdjustableScreenUtils.getMainSizesExt()

        search_level_size = self.search_level.getSize()
        pos_y = viewport.begin.y + header_height + search_level_size.y / 2

        search_level_slot = self.content.getMovieSlot(SLOT_DROP_LEVEL)
        search_level_slot.setWorldPosition(Mengine.vec2f(x_center, pos_y))
        self.search_level.attachTo(search_level_slot)

    # - SearchPanel ----------------------------------------------------------------------------------------------------

    def _initSearchPanel(self):
        self.search_panel = SearchPanel()
        self.search_panel.onInitialize(self)

    def _attachSearchPanel(self):
        _, game_height, _, banner_height, _, x_center, _ = AdjustableScreenUtils.getMainSizesExt()

        search_panel_size = self.search_panel.getSize()
        pos_y = game_height - banner_height - search_panel_size.y / 2

        search_panel_slot = self.content.getMovieSlot(SLOT_DROP_PANEL)
        search_panel_slot.setWorldPosition(Mengine.vec2f(x_center, pos_y))
        self.search_panel.attachTo(search_panel_slot)

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _createTaskChain(self, name, **params):
        tc_base = self.__class__.__name__
        tc = TaskManager.createTaskChain(Name=tc_base+"_"+name, **params)
        self.tcs.append(tc)
        return tc
