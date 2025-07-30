from Foundation.System import System
from Foundation.DemonManager import DemonManager
from Foundation.SystemManager import SystemManager
from Foundation.Task.Capture import Capture
from Game.Managers.GameManager import GameManager, GAME_MODE_STORY


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
        self.addObserver(Notificator.onFinalStageStart, self._onFinalStageStart)
        self.addObserver(Notificator.onLevelEnd, self._onLevelEnd)
        self.addObserver(Notificator.onCallRewardedAd, self._onCallRewardedAd)

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
                hint_ad.addNotify(Notificator.onCallRewardedAd, "Hint")

        # lives logic
        if self.existTaskChain("SearchPanelLives") is True:
            self.removeTaskChain("SearchPanelLives")

        with self.createTaskChain("SearchPanelLives", Repeat=True) as tc:
            mouse_position_capture = Capture(None)

            with tc.addRaceTask(2) as (hotspot_click, unavailable_item_click):
                hotspot_click.addListener(Notificator.onLevelMissClicked, Capture=mouse_position_capture)
                unavailable_item_click.addListener(Notificator.onItemClick, Filter=game.filterUnavailableItemClick, Capture=mouse_position_capture)

            with tc.addNotifyRequest(Notificator.onLevelLivesDecrease, 1) as (response_lives_changed,):
                def __onLevelLivesChanged(source, lives_count):
                    if lives_count <= 0:
                        popup_object = DemonManager.getDemon("PopUp")
                        popup = popup_object.entity
                        source.addNotify(Notificator.onPopUpShow, "LevelLost", popup.BUTTONS_STATE_DISABLE, popup.PROTOTYPE_BG_BIG)
                    else:
                        x_pos, y_pos = self._extractPosition(mouse_position_capture)
                        source.addNotify(Notificator.onMissClickEffect, x_pos, y_pos)

                    return True

                response_lives_changed.addScopeListener(Notificator.onLevelLivesChanged, __onLevelLivesChanged)

        return False

    def _onFinalStageStart(self, final_stage):
        # pick items from level
        if self.existTaskChain("FinalStageItemsPick") is True:
            self.removeTaskChain("FinalStageItemsPick")

        items_to_click = list(final_stage.drop_panel.items)

        with self.createTaskChain("FinalStageItemsPick", Repeat=True) as tc:
            #for item, parallel in tc.addParallelTaskList(items_to_click):
            for item, parallel in tc.addRaceTaskList(items_to_click):
                item_obj = item.item_obj
                item_socket = item.getSocket()
                parallel.addTask("TaskNodeSocketClick", Socket=item_socket, isDown=True)
                parallel.addPrint(" * FINAL STAGE CLICK ON '{}'".format(item))
                #parallel.addFunction(final_stage.quest_items.remove, item_obj)
                parallel.addFunction(final_stage.drop_panel.findRemovingItem, item_obj)
                parallel.addFunction(final_stage.drop_panel.attachToCursor)
                #TODO scale to normal size 1,1,1 0.25 seconds and do it parallel TaskMouseButtonClick
                parallel.addScope(final_stage.drop_panel.playRemovePanelItemAnim, item_obj)
                with parallel.addParallelTask(2) as (scale, click):
                    scale.addScope(final_stage.drop_panel.scaleAttachItem)
                    click.addTask("TaskMouseButtonClick", isDown=False)
                parallel.addScope(final_stage.drop_panel.validateDropPos)

        return False


    def _onLevelEnd(self, is_win):
        popup_object = DemonManager.getDemon("PopUp")
        popup = popup_object.entity

        if is_win is True:
            # Notification.notify(Notificator.onPopUpShow, "LevelWon", popup.BUTTONS_STATE_DISABLE)
            self._removeTaskChains()

            quest_index = GameManager.getCurrentGameParam("QuestIndex")
            cutscene_object = DemonManager.getDemon("Cutscene")
            cutscene_id = GameManager.getCurrentQuestCutsceneId()

            if quest_index is not None:
                cutscene_object.setParam("CutsceneId", cutscene_id)
                Notification.notify(Notificator.onChangeScene, "Cutscene")
            else:
                Notification.notify(Notificator.onChangeScene, "Lobby")
        else:
            Notification.notify(Notificator.onPopUpShow, "LevelLost", popup.BUTTONS_STATE_DISABLE, popup.PROTOTYPE_BG_BIG)
            # Notification.notify(Notificator.onChangeScene, "Lobby")

        GameManager.endGame(GAME_MODE_STORY, is_win)

        return False

    def _removeTaskChains(self):
        if self.existTaskChain("LevelItemsPick") is True:
            self.removeTaskChain("LevelItemsPick")

        if self.existTaskChain("SearchPanelHint") is True:
            self.removeTaskChain("SearchPanelHint")

        if self.existTaskChain("SearchPanelLives") is True:
            self.removeTaskChain("SearchPanelLives")

        if self.existTaskChain("FinalStageItemsPick") is True:
            self.removeTaskChain("FinalStageItemsPick")

    def _onCallRewardedAd(self, reward):
        tc_name = "GameRewardedAd"

        reward_scope = {
            "Hint": self._scopeHintAd,
            "Lives": self._scopeLivesAd,
        }

        if reward not in reward_scope.keys():
            return False

        scope = reward_scope[reward]

        if self.existTaskChain(tc_name) is True:
            self.removeTaskChain(tc_name)

        with self.createTaskChain(tc_name) as tc:
            tc.addScope(scope)

        return False

    # - TaskChain ------------------------------------------------------------------------------------------------------

    def _scopeHint(self, source):
        game_object = DemonManager.getDemon("GameArea")
        game = game_object.entity

        source.addScope(game.showHintEffect)

    def _scopeHintAd(self, source):
        game_object = DemonManager.getDemon("GameArea")
        game = game_object.entity

        if _DEVELOPMENT is True:
            source.addNotify(Notificator.onPopUpShowDebugAd)
            source.addListener(Notificator.onPopUpHideEnd, lambda content_id: content_id == "DebugAd")

        source.addFunction(game.search_panel.hint.incHintCount)
        source.addFunction(game.search_panel.switchHints)

    def _scopeLivesAd(self, source):
        system_popup = SystemManager.getSystem("SystemPopUp")

        if _DEVELOPMENT is True:
            with source.addIfTask(lambda: system_popup.getPopUpState() == system_popup.STATE_HIDING) as (true, false):
                true.addListener(Notificator.onPopUpHideEnd)

            source.addNotify(Notificator.onPopUpShowDebugAd)
            source.addListener(Notificator.onPopUpHideEnd, lambda content_id: content_id == "DebugAd")

        source.addNotify(Notificator.onLevelLivesRestore)

    def _extractPosition(self, capture):
        type = capture.getType()

        if type == Notificator.onLevelMissClicked:
            x, y = capture.getArgs()
            return (x, y)

        elif type == Notificator.onItemClick:
            item, x, y = capture.getArgs()
            return (x, y)

