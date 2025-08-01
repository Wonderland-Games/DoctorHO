from Foundation.Database import Database

class DatabaseDefaultSlots_GameArea(Database):
    def __init__(self):
        super(DatabaseDefaultSlots_GameArea, self).__init__()
        self.addRecord(Slot="Background", Type="Scene", Group="Background", Enable=1)
        self.addRecord(Slot="GameArea", Type="Scene", Group="GameArea", Enable=1)
        self.addRecord(Slot="GameHeader", Type="Scene", Group="GameHeader", Enable=1)
        self.addRecord(Slot="MissClick", Type="Scene", Group="MissClick")
        self.addRecord(Slot="DummyBanner", Type="Scene", Group="DummyBanner", Enable=1, Platform="PC")
        self.addRecord(Slot="FadeUI", Type="Scene", Group="FadeUI", Enable=1)
        self.addRecord(Slot="PopUp", Type="Scene", Group="PopUp", Enable=0)
        self.addRecord(Slot="Fade", Type="Scene", Group="Fade", Enable=1)
        self.addRecord(Slot="BlockInput", Type="Scene", Group="BlockInput", Enable=1)
        pass
    pass
