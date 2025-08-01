from Foundation.Database import Database

class DatabaseLevels(Database):
    def __init__(self):
        super(DatabaseLevels, self).__init__()
        class RecordLevels(object):
            def __init__(self, LevelId, ChapterId, SceneName, CardMovie, LevelCardTextId, LevelMovie, QuestPointsToUnlock):
                self.LevelId = LevelId
                self.ChapterId = ChapterId
                self.SceneName = SceneName
                self.CardMovie = CardMovie
                self.LevelCardTextId = LevelCardTextId
                self.LevelMovie = LevelMovie
                self.QuestPointsToUnlock = QuestPointsToUnlock
                pass
            pass

        self.addORM(RecordLevels(1, 1, "01_AncientEgypt", "Movie2_Card_Ancient", "ID_LevelCardTitle_01_AncientEgypt", "Movie2_01_AncientEgypt", 0))
        self.addORM(RecordLevels(2, 1, "01_AncientGreece", "Movie2_Card_Ancient", "ID_LevelCardTitle_01_AncientGreece", "Movie2_01_AncientGreece", 200))
        self.addORM(RecordLevels(3, 1, "01_AncientRome", "Movie2_Card_Ancient", "ID_LevelCardTitle_01_AncientRome", "Movie2_01_AncientRome", 300))
        self.addORM(RecordLevels(4, 2, "02_Europa", "Movie2_Card_Space", "ID_LevelCardTitle_02_Europa", "Movie2_02_Europa", 0))
        self.addORM(RecordLevels(5, 2, "02_Mars", "Movie2_Card_Space", "ID_LevelCardTitle_02_Mars", "Movie2_02_Mars", 150))
        self.addORM(RecordLevels(6, 2, "02_Titan", "Movie2_Card_Space", "ID_LevelCardTitle_02_Titan", "Movie2_02_Titan", 200))
        self.addORM(RecordLevels(7, 2, "02_Venus", "Movie2_Card_Space", "ID_LevelCardTitle_02_Venus", "Movie2_02_Venus", 250))
        self.addORM(RecordLevels(8, 2, "02_Moon", "Movie2_Card_Space", "ID_LevelCardTitle_02_Moon", "Movie2_02_Moon", 300))
        pass
    pass
