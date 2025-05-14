from Foundation.Database import Database

class DatabaseSystems(Database):
    def __init__(self):
        super(DatabaseSystems, self).__init__()
        self.addRecord(Module="Game.Systems", Name="SystemGlobal", Global=1, Priority=1)
        self.addRecord(Module="Game.Systems", Name="SystemGame", Global=1)
        self.addRecord(Module="Foundation.Systems", Name="SystemDebugNotifications", Global=1, Development=1)
        self.addRecord(Module="Foundation.Systems", Name="SystemFade", Global=1)
        self.addRecord(Module="UIKit.Systems", Name="SystemPopUp", Global=1)
        self.addRecord(Module="Game.Systems", Name="SystemUI", Global=1)
        self.addRecord(Module="Foundation.Systems", Name="SystemAdvertising", Global=1)
        pass
    pass
