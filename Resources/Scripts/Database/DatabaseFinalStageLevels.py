from Foundation.Database import Database

class DatabaseFinalStageLevels(Database):
    def __init__(self):
        super(DatabaseFinalStageLevels, self).__init__()
        class RecordFinalStageLevels(object):
            def __init__(self, ChapterId, SceneName):
                self.ChapterId = ChapterId
                self.SceneName = SceneName
                pass
            pass

        self.addORM(RecordFinalStageLevels(1, "01_FinalStage"))
        self.addORM(RecordFinalStageLevels(2, "02_FinalStage"))
        pass
    pass
