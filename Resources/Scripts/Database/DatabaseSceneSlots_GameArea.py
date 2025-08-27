from Foundation.Database import Database

class DatabaseSceneSlots_GameArea(Database):
    def __init__(self):
        super(DatabaseSceneSlots_GameArea, self).__init__()
        self.addRecord(Name="Background", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="GameArea", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="Level", Type="Layer2D", Width=2736, Height=1536, Main=1)
        self.addRecord(Name="LevelZones", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="GameHeader", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="DummyBanner", Type="Layer2D", Width=2736, Height=1536, Main=0, Platform="PC")
        self.addRecord(Name="MissClick", Type="Layer2D", Width=2736, Height=1536)
        self.addRecord(Name="FadeUI", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="PopUp", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="Fade", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="BlockInput", Type="Layer2D", Width=2736, Height=1536, Main=0)
        pass
    pass
