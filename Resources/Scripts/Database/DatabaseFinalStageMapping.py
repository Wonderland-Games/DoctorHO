from Foundation.Database import Database

class DatabaseFinalStageMapping(Database):
    def __init__(self):
        super(DatabaseFinalStageMapping, self).__init__()
        class RecordFinalStageMapping(object):
            def __init__(self, StageName, ItemName, GroupName, MovieName):
                self.StageName = StageName
                self.ItemName = ItemName
                self.GroupName = GroupName
                self.MovieName = MovieName
                pass
            pass

        self.addORM(RecordFinalStageMapping("01_FinalStage", "Item_Quest_Armor", "01_FinalStage", "Movie2_Armor"))
        self.addORM(RecordFinalStageMapping("01_FinalStage", "Item_Quest_Helmet", "01_FinalStage", "Movie2_Helmet"))
        self.addORM(RecordFinalStageMapping("01_FinalStage", "Item_Quest_Bust", "01_FinalStage", "Movie2_Bust"))
        self.addORM(RecordFinalStageMapping("02_FinalStage", "Item_Quest_Armor", "02_FinalStage", "Movie2_Armor"))
        self.addORM(RecordFinalStageMapping("02_FinalStage", "Item_Quest_Helmet", "02_FinalStage", "Movie2_Helmet"))
        self.addORM(RecordFinalStageMapping("02_FinalStage", "Item_Quest_Sword", "02_FinalStage", "Movie2_Sword"))
        self.addORM(RecordFinalStageMapping("02_FinalStage", "Item_Quest_Gun", "02_FinalStage", "Movie2_Gun"))
        self.addORM(RecordFinalStageMapping("02_FinalStage", "Item_Quest_Spaceship", "02_FinalStage", "Movie2_Spaceship"))
        pass
    pass
