from Foundation.Database import Database

class DatabaseDefaultSlots_GameArea(Database):
    def __init__(self):
        super(DatabaseDefaultSlots_GameArea, self).__init__()
        self.addRecord(Slot="Background", Type="Scene", Group="Background", Enable=1)
        self.addRecord(Slot="GameArea", Type="Scene", Group="GameArea", Enable=1)
        self.addRecord(Slot="01_AncientEgypt", Type="Scene", Group="01_AncientEgypt", Enable=0)
        self.addRecord(Slot="01_AncientGreece", Type="Scene", Group="01_AncientGreece", Enable=0)
        self.addRecord(Slot="01_AncientRome", Type="Scene", Group="01_AncientRome", Enable=0)
        self.addRecord(Slot="02_Europa", Type="Scene", Group="02_Europa", Enable=0)
        self.addRecord(Slot="02_Mars", Type="Scene", Group="02_Mars", Enable=0)
        self.addRecord(Slot="02_Titan", Type="Scene", Group="02_Titan", Enable=0)
        self.addRecord(Slot="02_Venus", Type="Scene", Group="02_Venus", Enable=0)
        self.addRecord(Slot="02_Moon", Type="Scene", Group="02_Moon", Enable=0)
        self.addRecord(Slot="GameHeader", Type="Scene", Group="GameHeader", Enable=1)
        self.addRecord(Slot="DummyBanner", Type="Scene", Group="DummyBanner", Enable=1, Platform="PC")
        self.addRecord(Slot="FadeUI", Type="Scene", Group="FadeUI", Enable=1)
        self.addRecord(Slot="PopUp", Type="Scene", Group="PopUp", Enable=0)
        self.addRecord(Slot="Fade", Type="Scene", Group="Fade", Enable=1)
        self.addRecord(Slot="BlockInput", Type="Scene", Group="BlockInput", Enable=1)
        pass
    pass
