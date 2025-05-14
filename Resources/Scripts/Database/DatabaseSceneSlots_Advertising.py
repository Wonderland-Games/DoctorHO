from Foundation.Database import Database

class DatabaseSceneSlots_Advertising(Database):
    def __init__(self):
        super(DatabaseSceneSlots_Advertising, self).__init__()
        self.addRecord(Name="Advertising", Type="Layer2D", Width=2736, Height=1536, Main=1)
        self.addRecord(Name="Fade", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="BlockInput", Type="Layer2D", Width=2736, Height=1536, Main=0)
        pass
    pass
