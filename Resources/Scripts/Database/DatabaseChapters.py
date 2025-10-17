from Foundation.Database import Database

class DatabaseChapters(Database):
    def __init__(self):
        super(DatabaseChapters, self).__init__()
        class RecordChapters(object):
            def __init__(self, ChapterId, LevelCardsGroupName, Slots, LevelsId):
                self.ChapterId = ChapterId
                self.LevelCardsGroupName = LevelCardsGroupName
                self.Slots = Slots
                self.LevelsId = LevelsId
                pass
            pass

        self.addORM(RecordChapters(1, "LevelCards_Ancient", "Movie2_ChapterSlots", [1, 2, 3]))
        self.addORM(RecordChapters(2, "LevelCards_SolarSystem", "Movie2_ChapterSlots", [4, 5, 6, 7, 8]))
        pass
    pass
