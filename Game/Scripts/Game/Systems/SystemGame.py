from Foundation.System import System
from Foundation.DemonManager import DemonManager


class SystemGame(System):
    def __init__(self):
        super(SystemGame, self).__init__()
        pass

    # - Initializer ----------------------------------------------------------------------------------------------------

    def _onInitialize(self):
        super(SystemGame, self)._onInitialize()
        pass

    def _onFinalize(self):
        super(SystemGame, self)._onFinalize()
        pass

    # - System ---------------------------------------------------------------------------------------------------------

    def _onSave(self):
        super(SystemGame, self)._onSave()
        return None

    def _onLoad(self, save_dict):
        super(SystemGame, self)._onLoad(save_dict)
        pass

    def _onRun(self):
        super(SystemGame, self)._onRun()

        self.addObserver(Notificator.onLevelStart, self._onLevelStart)
        self.addObserver(Notificator.onLevelLivesChanged, self._onLevelLivesChanged)
        self.addObserver(Notificator.onLevelEnd, self._onLevelEnd)

        return True

    def _onStop(self):
        super(SystemGame, self)._onStop()
        pass

    # - Observers ------------------------------------------------------------------------------------------------------

    def _onLevelStart(self, game):
        # pick items from level
        if self.existTaskChain("LevelItemsPick") is True:
            self.removeTaskChain("LevelItemsPick")

        with self.createTaskChain("LevelItemsPick") as tc:
            for item, parallel in tc.addParallelTaskList(game.search_level.items):
                parallel.addTask("TaskItemClick", Item=item, Filter=game.filterItemClick)
                parallel.addPrint(" * CLICK ON '{}'".format(item.getName()))
                parallel.addTask("TaskAppendParam", Object=game.object, Param="FoundItems", Value=item)
                parallel.addFunction(game.search_level.items.remove, item)
                parallel.addFunction(game.search_panel.addRemovingItem, item)
                parallel.addScope(game.moveLevelItemToPanelItem, item)
                parallel.addScope(game.search_panel.playRemovePanelItemAnim, item)

            tc.addNotify(Notificator.onLevelEnd, True)

        # hint logic
        if self.existTaskChain("SearchPanelHint") is True:
            self.removeTaskChain("SearchPanelHint")

        with self.createTaskChain("SearchPanelHint", Repeat=True) as tc:
            with tc.addRaceTask(2) as (hint, hint_ad):
                hint.addTask("TaskMovie2ButtonClick", Movie2Button=game.search_panel.hint.button.movie)
                hint.addScope(self._scopeHint)

                hint_ad.addTask("TaskMovie2ButtonClick", Movie2Button=game.search_panel.hint_ad.button.movie)
                hint_ad.addScope(self._scopeHintAd)

        # lives logic
        if self.existTaskChain("SearchPanelLives") is True:
            self.removeTaskChain("SearchPanelLives")

        with self.createTaskChain("SearchPanelLives", Repeat=True) as tc:
            with tc.addRaceTask(2) as (hotspot_click, unavailable_item_click):
                hotspot_click.addListener(Notificator.onLevelMissClicked)
                unavailable_item_click.addListener(Notificator.onItemClick, Filter=game.filterUnavailableItemClick)

            tc.addNotify(Notificator.onLevelLivesDecrease)

        return False

    def _onLevelLivesChanged(self, lives_count):
        if lives_count <= 0:
            Notification.notify(Notificator.onLevelEnd, False)

        return False

    def _onLevelEnd(self, is_win):
        if is_win is True:
            Notification.notify(Notificator.onPopUpShow, "LevelWon")
        else:
            Notification.notify(Notificator.onPopUpShow, "LevelLost")

        if self.existTaskChain("LevelItemsPick") is True:
            self.removeTaskChain("LevelItemsPick")

        if self.existTaskChain("SearchPanelHint") is True:
            self.removeTaskChain("SearchPanelHint")

        if self.existTaskChain("SearchPanelLives") is True:
            self.removeTaskChain("SearchPanelLives")

        return False

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _scopeHint(self, source):
        game_object = DemonManager.getDemon("GameArea")
        game = game_object.entity
        hint = game.search_panel.hint

        # get random panel item from search panel
        panel_item = game.search_panel.getRandomAvailableItem()
        if panel_item is None:
            return

        # save hint item
        hint.hint_item = panel_item.item_obj

        # calc item hint point
        hint_point = hint.hint_item.calcWorldHintPoint()

        # create temp hint node
        temp_hint_node = Mengine.createNode("Interender")
        temp_hint_node.setName("TempHintNode")

        # setting items position to temp node
        game.addChild(temp_hint_node)
        temp_hint_node.setWorldPosition(hint_point)

        # getting transformation from temp node
        hint_item_transformation = temp_hint_node.getTransformation()

        # destroy temp hint node
        temp_hint_node.removeFromParent()
        Mengine.destroyNode(temp_hint_node)

        # hint effect logic
        source.addFunction(hint.decHintCount)
        source.addFunction(game.search_panel.switchHints)

        source.addFunction(game.search_panel.hint.button.movie.setBlock, True)
        source.addFunction(game.search_panel.virtual_area.freeze, True)
        source.addFunction(game.search_level.virtual_area.freeze, True)

        source.addScope(hint.hint_effect.show, hint_item_transformation)
        source.addListener(Notificator.onItemClick, Filter=lambda item: item == hint.hint_item)
        source.addScope(hint.hint_effect.hide, hint_item_transformation)

        source.addFunction(hint.cleanHintItem)

        source.addFunction(game.search_panel.hint.button.movie.setBlock, False)
        source.addFunction(game.search_panel.virtual_area.freeze, False)
        source.addFunction(game.search_level.virtual_area.freeze, False)

    def _scopeHintAd(self, source):
        game_object = DemonManager.getDemon("GameArea")
        game = game_object.entity

        source.addPrint("[HintAd] Call onAdvertisement event")
        source.addFunction(game.search_panel.hint.incHintCount)
        source.addFunction(game.search_panel.switchHints)
