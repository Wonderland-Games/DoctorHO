from Foundation.Database import Database

class DatabaseSceneSlots_Lobby(Database):
    def __init__(self):
        super(DatabaseSceneSlots_Lobby, self).__init__()
        self.addRecord(Name="Background", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="Lobby", Type="Layer2D", Width=2736, Height=1536, Main=1)
        self.addRecord(Name="01_AncientEgypt", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="01_AncientGreece", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="01_AncientRome", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="02_Europa", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="02_Mars", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="02_Titan", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="02_Venus", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="02_Moon", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="QuestItemStore", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="Header", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="DummyBanner", Type="Layer2D", Width=2736, Height=1536, Main=0, Platform="PC")
        self.addRecord(Name="FadeUI", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="PopUp", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="Fade", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="BlockInput", Type="Layer2D", Width=2736, Height=1536, Main=0)
        pass
    pass
