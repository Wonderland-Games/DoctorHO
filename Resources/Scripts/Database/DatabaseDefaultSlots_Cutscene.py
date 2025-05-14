from Foundation.Database import Database

class DatabaseDefaultSlots_Cutscene(Database):
    def __init__(self):
        super(DatabaseDefaultSlots_Cutscene, self).__init__()
        self.addRecord(Slot="Background", Type="Scene", Group="Background", Enable=1)
        self.addRecord(Slot="Cutscene", Type="Scene", Group="Cutscene", Enable=1)
        self.addRecord(Slot="Intro", Type="Scene", Group="Intro", Enable=0)
        self.addRecord(Slot="Header", Type="Scene", Group="Header", Enable=1)
        self.addRecord(Slot="Banner", Type="Scene", Group="Banner", Enable=1, Platform="PC")
        self.addRecord(Slot="Fade", Type="Scene", Group="Fade", Enable=1)
        self.addRecord(Slot="BlockInput", Type="Scene", Group="BlockInput", Enable=1)
        pass
    pass
