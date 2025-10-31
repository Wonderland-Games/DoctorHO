from Foundation.Database import Database

class DatabaseBackpackLevels(Database):
    def __init__(self):
        super(DatabaseBackpackLevels, self).__init__()
        class RecordBackpackLevels(object):
            def __init__(self, ChapterId, SceneName):
                self.ChapterId = ChapterId
                self.SceneName = SceneName
                pass
            pass

        self.addORM(RecordBackpackLevels(1, "01_Backpack"))
        self.addORM(RecordBackpackLevels(2, "02_Backpack"))
        pass
    pass
