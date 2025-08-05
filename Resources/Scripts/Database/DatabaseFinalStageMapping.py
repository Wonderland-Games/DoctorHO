from Foundation.Database import Database

class DatabaseFinalStageMapping(Database):
    def __init__(self):
        super(DatabaseFinalStageMapping, self).__init__()
        class RecordFinalStageMapping(object):
            def __init__(self, ItemName, MovieName, GroupName):
                self.ItemName = ItemName
                self.MovieName = MovieName
                self.GroupName = GroupName
                pass
            pass

        self.addORM(RecordFinalStageMapping("Item_Quest_Armor", "Movie2_Armor", "01_FinalStage"))
        self.addORM(RecordFinalStageMapping("Item_Quest_Helmet", "Movie2_Helmet", "01_FinalStage"))
        self.addORM(RecordFinalStageMapping("Item_Quest_Bust", "Movie2_Bust", "01_FinalStage"))
        self.addORM(RecordFinalStageMapping("Item_Quest_Armor", "Movie2_Armor", "02_FinalStage"))
        self.addORM(RecordFinalStageMapping("Item_Quest_Helmet", "Movie2_Helmet", "02_FinalStage"))
        self.addORM(RecordFinalStageMapping("Item_Quest_Sword", "Movie2_Sword", "02_FinalStage"))
        self.addORM(RecordFinalStageMapping("Item_Quest_Gun", "Movie2_Gun", "02_FinalStage"))
        self.addORM(RecordFinalStageMapping("Item_Quest_Spaceship", "Movie2_Spaceship", "02_FinalStage"))
        pass
    pass
