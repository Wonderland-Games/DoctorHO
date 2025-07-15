from UIKit.Systems.SystemUserInterface import SystemUserInterface as BaseSystem
from UIKit.AdjustableScreenUtils import AdjustableScreenUtils
from Foundation.GroupManager import GroupManager
from Foundation.TaskManager import TaskManager
from Foundation.Providers.DummyAdvertisement import DummyAdvertisement


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

            # Get banner node
            banner_node = dummy_banner.getEntityNode()

            # Banner movie size (REMAKE HARDCODE TO SOMETHING MORE AUTOMATIC!)
            banner_movie_width = 320.0
            banner_movie_height = 50.0

            # Dummy advertisement banner size
            banner_width = DummyAdvertisement.getBannerWidth()
            banner_height = DummyAdvertisement.getBannerHeight()

            # Set banner scale
            scale_factor_width = banner_width / banner_movie_width
            scale_factor_height = banner_height / banner_movie_height
            banner_node.setScale((scale_factor_width, scale_factor_height, 1.0))

            # Game screen parameters, set banner position
            game_viewport = Mengine.getGameViewport()
            game_width = AdjustableScreenUtils.getGameWidth()
            game_height = AdjustableScreenUtils.getGameHeight()

            banner_node.setLocalPosition((
                game_viewport.begin.x + game_width / 2,
                game_viewport.begin.y + game_height - banner_height / 2
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
