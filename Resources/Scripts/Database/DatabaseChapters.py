from Foundation.Database import Database

class DatabaseChapters(Database):
    def __init__(self):
        super(DatabaseChapters, self).__init__()
        class RecordChapters(object):
            def __init__(self, ChapterId, Slots, LevelsId):
                self.ChapterId = ChapterId
                self.Slots = Slots
                self.LevelsId = LevelsId
                pass
            pass

        self.addORM(RecordChapters(1, "Movie2_ChapterSlots_Ancient", [1, 2, 3]))
        self.addORM(RecordChapters(2, "Movie2_ChapterSlots_SolarSystem", [4, 5, 6, 7, 8]))
        pass
    pass
