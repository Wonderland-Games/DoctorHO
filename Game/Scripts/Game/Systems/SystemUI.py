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

            # Get banner movie size
            banner_movie_bounds = dummy_banner.getCompositionBounds()
            banner_movie_size = Utils.getBoundingBoxSize(banner_movie_bounds)

            # Get dummy advertisement banner size
            banner_width = AdjustableScreenUtils.getActualBannerWidth()
            banner_height = AdjustableScreenUtils.getActualBannerHeight()

            # Get banner movie node
            banner_node = dummy_banner.getEntityNode()

            # Set banner movie scale
            scale_factor_width = banner_width / banner_movie_size.x
            scale_factor_height = banner_height / banner_movie_size.y
            banner_node.setScale((scale_factor_width, scale_factor_height, 1.0))

            # Set banner movie position
            game_viewport = Mengine.getGameViewport()
            game_center = AdjustableScreenUtils.getGameCenter()
            banner_node.setWorldPosition((
                game_center.x,
                game_viewport.end.y - banner_height / 2
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
