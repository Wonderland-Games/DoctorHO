from Foundation.Database import Database

class DatabaseSceneSlots_QuestBackpack(Database):
    def __init__(self):
        super(DatabaseSceneSlots_QuestBackpack, self).__init__()
        self.addRecord(Name="Background", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="QuestBackpack", Type="Layer2D", Width=2736, Height=1536, Main=1)
        self.addRecord(Name="QuestItemStore", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="Header", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="Banner", Type="Layer2D", Width=2736, Height=1536, Main=0, Platform="PC")
        self.addRecord(Name="FadeUI", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="PopUp", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="Fade", Type="Layer2D", Width=2736, Height=1536, Main=0)
        self.addRecord(Name="BlockInput", Type="Layer2D", Width=2736, Height=1536, Main=0)
        pass
    pass
