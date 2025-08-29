from UIKit.Systems.SystemUserInterface import SystemUserInterface as BaseSystem
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils
from Foundation.GroupManager import GroupManager
from Foundation.TaskManager import TaskManager


class SystemUI(BaseSystem):
    def _cbRun(self):
        super(SystemUI, self)._cbRun()
        self._devAdjustBanner()
        return True

    def _devAdjustBanner(self):
        dummy_banner = GroupManager.getObject("DummyBanner", "Movie2_Banner")

        if _DEVELOPMENT is False or Mengine.hasOption("nobanner") is True:
            dummy_banner.setEnable(False)
            return

        def _setup():
            if dummy_banner.isActive() is False:
                Trace.msg_err("SystemUI._devAdjustBanner: Movie2_Banner entity is not active!!!!!")
                return

            # Get dummy banner size
            dummy_banner_bounds = dummy_banner.getCompositionBounds()
            dummy_banner_size = Utils.getBoundingBoxSize(dummy_banner_bounds)

            # Get advertisement banner size
            ad_banner_size = AdjustableScreenUtils.getBannerSize()

            # Get dummy banner node
            dummy_banner_node = dummy_banner.getEntityNode()

            # Set dummy banner scale
            scale_width = ad_banner_size.x / dummy_banner_size.x
            scale_height = ad_banner_size.y / dummy_banner_size.y
            dummy_banner_node.setScale((scale_width, scale_height, 1.0))

            # Set dummy banner position
            game_viewport = Mengine.getGameViewport()
            game_center = AdjustableScreenUtils.getGameCenter()
            dummy_banner_node.setWorldPosition((
                game_center.x,
                game_viewport.end.y - ad_banner_size.y / 2
            ))

        with TaskManager.createTaskChain() as tc:
            tc.addListener(Notificator.onSceneInit, Filter=lambda scene: scene == "Lobby")
            tc.addEnable(dummy_banner)
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
