from Foundation.Database import Database

class DatabaseManagers(Database):
    def __init__(self):
        super(DatabaseManagers, self).__init__()
        self.addRecord(Module="Foundation", Name="SettingsManager")
        self.addRecord(Module="Foundation", Name="DefaultManager", Param="Default")
        self.addRecord(Module="Foundation", Name="SystemManager")
        self.addRecord(Module="Foundation", Name="GroupManager", Param="Groups")
        self.addRecord(Module="Foundation", Name="DemonManager", Param="Demons")
        self.addRecord(Module="Foundation", Name="SceneManager", Param="DefaultSlots")
        self.addRecord(Module="Foundation", Name="SceneManager", Param="SceneSlots")
        self.addRecord(Module="Foundation", Name="SceneManager", Param="Scenes")
        self.addRecord(Module="Foundation", Name="LanguagesManager", Param="Languages")
        self.addRecord(Module="Foundation", Name="DebugNotificationsManager", Param="DebugNotifications")
        self.addRecord(Module="Game.Managers", Name="GameManager")
        pass
    pass
