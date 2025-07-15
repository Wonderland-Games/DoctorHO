from Foundation.Database import Database

class DatabaseSceneSlots_Cutscene(Database):
    def __init__(self):
        super(DatabaseSceneSlots_Cutscene, self).__init__()
        self.addRecord(Name="Background", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="Cutscene", Type="Layer2D", Width=2736, Height=1536, Main=1)
        self.addRecord(Name="Intro", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="Cutscene_01", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="Cutscene_02", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="Header", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="DummyBanner", Type="Layer2D", Width=2736, Height=1536, Main=0, Platform="PC")
        self.addRecord(Name="Fade", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="BlockInput", Type="Layer2D", Width=2736, Height=1536, Main=0)
        pass
    pass
