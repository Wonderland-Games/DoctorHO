from UIKit.Systems.SystemUserInterface import SystemUserInterface as BaseSystem


class SystemUI(BaseSystem):
    def _setTexts(self):
        environments = [
            "Settings_Languages",
            "Settings_Support",
            "Settings_Credits",
            "Settings_Lobby",

            "LevelLost_Ad",
            "LevelLost_Restart",

            "LevelWon_Lobby",

            "QuestItemReceived_Button",

            "Lobby_Play",
        ]
        
        for env in environments:
            Mengine.setTextAlias(env, "$UIButton", "ID_" + env)
