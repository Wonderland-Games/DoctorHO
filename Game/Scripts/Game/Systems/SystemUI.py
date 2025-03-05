from UIKit.Systems.SystemUserInterface import SystemUserInterface as BaseSystem


class SystemUI(BaseSystem):
    def _setTexts(self):
        Mengine.setTextAlias("Settings_Languages", "$UIButton", "ID_Settings_Languages")
        Mengine.setTextAlias("Settings_Support", "$UIButton", "ID_Settings_Support")
        Mengine.setTextAlias("Settings_Credits", "$UIButton", "ID_Settings_Credits")
        Mengine.setTextAlias("Settings_Lobby", "$UIButton", "ID_Settings_Lobby")

        Mengine.setTextAlias("LevelLost_Ad", "$UIButton", "ID_LevelLost_Ad")
        Mengine.setTextAlias("LevelLost_Restart", "$UIButton", "ID_LevelLost_Restart")
