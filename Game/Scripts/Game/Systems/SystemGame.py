from Foundation.System import System


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
        self.addObserver(Notificator.onLevelMissClicked, self._onLevelMissClicked)
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
                parallel.addFunction(game.search_level.items.remove, item)
                parallel.addFunction(game.search_panel.changeItemFromAvailableToRemove, item)
                parallel.addScope(game.moveLevelItemToPanelItem, item)
                parallel.addScope(game.search_panel.playRemovePanelItemAnim, item)

            tc.addNotify(Notificator.onLevelEnd, True)

        # hint logic
        if self.existTaskChain("SearchPanelHint") is True:
            self.removeTaskChain("SearchPanelHint")

        with self.createTaskChain("SearchPanelHint", Repeat=True) as tc:
            tc.addTask("TaskMovie2ButtonClick", Movie2Button=game.search_panel.hint.button)
            tc.addPrint(" * CLICK HINT")

            with tc.addIfTask(game.search_panel.hint.isAvailable) as (hint, advertisement):
                hint.addScope(game.search_panel.hint.clickHint)
                advertisement.addPrint("[Hint] Call onPopUpAdvertisement event")

        # lives logic
        if self.existTaskChain("SearchPanelLives") is True:
            self.removeTaskChain("SearchPanelLives")

        with self.createTaskChain("SearchPanelLives", Repeat=True) as tc:
            with tc.addRaceTask(2) as (hotspot_click, unavailable_item_click):
                hotspot_click.addEvent(game.miss_click.miss_click_event)
                unavailable_item_click.addListener(Notificator.onItemClick, Filter=game.filterUnavailableItemClick)

            # tc.addFunction(game.search_panel.lives_counter.decItemsCount)
            tc.addNotify(Notificator.onLevelLivesDecrease)

        return False

    def _onLevelMissClicked(self):
        Notification.notify(Notificator.onLevelLivesDecrease)

    def _onLevelLivesChanged(self, lives_count):
        if lives_count <= 0:
            Notification.notify(Notificator.onLevelEnd, False)

        return False

    def _onLevelEnd(self, is_win):
        if is_win is True:
            print("YOU WIN!")
        else:
            print("YOU LOSE!")

        if self.existTaskChain("LevelItemsPick") is True:
            self.removeTaskChain("LevelItemsPick")

        if self.existTaskChain("SearchPanelHint") is True:
            self.removeTaskChain("SearchPanelHint")

        if self.existTaskChain("SearchPanelLives") is True:
            self.removeTaskChain("SearchPanelLives")

        return False
