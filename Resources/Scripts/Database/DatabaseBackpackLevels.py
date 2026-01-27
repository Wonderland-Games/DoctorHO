from Foundation.Database import Database

class DatabaseBackpackLevels(Database):
    def __init__(self):
        super(DatabaseBackpackLevels, self).__init__()
        class RecordBackpackLevels(object):
            def __init__(self, ChapterId, SceneName, GroupName):
                self.ChapterId = ChapterId
                self.SceneName = SceneName
                self.GroupName = GroupName
                pass
            pass

        self.addORM(RecordBackpackLevels(1, "01_Backpack", "01_Backpack"))
        self.addORM(RecordBackpackLevels(2, "02_Backpack", "02_Backpack"))
        pass
    pass
