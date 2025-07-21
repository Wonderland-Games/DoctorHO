from Foundation.Database import Database

class DatabaseDefaultSlots_FinalStage(Database):
    def __init__(self):
        super(DatabaseDefaultSlots_FinalStage, self).__init__()
        self.addRecord(Slot="Background", Type="Scene", Group="Background", Enable=1)
        self.addRecord(Slot="FinalStage", Type="Scene", Group="FinalStage", Enable=1)
        self.addRecord(Slot="QuestItemStore", Type="Scene", Group="QuestItemStore", Enable=0)
        self.addRecord(Slot="01_FinalStage", Type="Scene", Group="01_FinalStage", Enable=0)
        self.addRecord(Slot="QuestItemStore", Type="Scene", Group="QuestItemStore", Enable=0)
        self.addRecord(Slot="Header", Type="Scene", Group="GameHeader", Enable=1)
        self.addRecord(Slot="MissClick", Type="Scene", Group="MissClick")
        self.addRecord(Slot="DummyBanner", Type="Scene", Group="DummyBanner", Enable=1, Platform="PC")
        self.addRecord(Slot="FadeUI", Type="Scene", Group="FadeUI", Enable=1)
        self.addRecord(Slot="PopUp", Type="Scene", Group="PopUp", Enable=0)
        self.addRecord(Slot="Fade", Type="Scene", Group="Fade", Enable=1)
        self.addRecord(Slot="BlockInput", Type="Scene", Group="BlockInput", Enable=1)
        pass
    pass
