from Foundation.Database import Database

class DatabaseDefaultSlots_Advertising(Database):
    def __init__(self):
        super(DatabaseDefaultSlots_Advertising, self).__init__()
        self.addRecord(Slot="Advertising", Type="Scene", Group="Advertising", Enable=1)
        self.addRecord(Slot="Fade", Type="Scene", Group="Fade", Enable=1)
        self.addRecord(Slot="BlockInput", Type="Scene", Group="BlockInput", Enable=1)
        pass
    pass
