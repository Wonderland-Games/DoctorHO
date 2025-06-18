from UIKit.Systems.SystemUserInterface import SystemUserInterface as BaseSystem
from Foundation.GroupManager import GroupManager
from Foundation.TaskManager import TaskManager
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils

BANNER_HEIGHT = 50.0

class SystemUI(BaseSystem):
    def _cbRun(self):
        super(SystemUI, self)._cbRun()
        self._devAdjustBanner()
        return True

    def _devAdjustBanner(self):
        banner = GroupManager.getObject("Banner", "Movie2_Banner")

        if _DEVELOPMENT is False or Mengine.hasOption("nobanner") is True:
            banner.setEnable(False)
            return

        viewport = Mengine.getGameViewport()
        game_width = AdjustableScreenUtils.getGameWidth()
        game_height = AdjustableScreenUtils.getGameHeight()

        banner_width = 320.0
        scale = game_width / banner_width

        banner.setEnable(True)
        banner.setScale((scale, 1.0, 1.0))

        def _setup():
            if banner.isActive() is False:
                Trace.msg_err("SystemUI._devAdjustBanner: Movie2_Banner entity is not active!!!!!")
                return
            node = banner.getEntityNode()
            node.setLocalPosition((
                viewport.begin.x + game_width / 2,
                viewport.begin.y + game_height - BANNER_HEIGHT / 2
            ))

        with TaskManager.createTaskChain() as tc:
            tc.addListener(Notificator.onSceneInit, Filter=lambda scene: scene == "Lobby")
            tc.addFunction(_setup)

    def _setTexts(self):
        environments = [
            "Settings_Languages",
            "Settings_Support",
            "Settings_Credits",
            "Settings_Lobby",

            "LevelLost_Ad",
            "LevelLost_Restart",
            "LevelLost_Lobby",

            "LevelWon_Lobby",

            "QuestItemReceived_Button",

            "Lobby_Play",

            "Cutscene_Skip",
        ]
        
        for env in environments:
            Mengine.setTextAlias(env, "$UIButton", "ID_" + env)
