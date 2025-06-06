from Foundation.Database import Database

class DatabaseQuests(Database):
    def __init__(self):
        super(DatabaseQuests, self).__init__()
        class RecordQuests(object):
            def __init__(self, ChapterId, LevelId, ItemsCount, QuestItem, CutsceneId):
                self.ChapterId = ChapterId
                self.LevelId = LevelId
                self.ItemsCount = ItemsCount
                self.QuestItem = QuestItem
                self.CutsceneId = CutsceneId
                pass
            pass

        self.addORM(RecordQuests(1, 1, 5, "Item_Quest_Armor", "Cutscene_01_Armor"))
        self.addORM(RecordQuests(1, 2, 8, "Item_Quest_Helmet", "Cutscene_01_Helmet"))
        self.addORM(RecordQuests(1, 3, 12, "Item_Quest_Bust", "Cutscene_01_Bust"))
        self.addORM(RecordQuests(2, 4, 6, "Item_Quest_Armor", "Cutscene_02_Armor"))
        self.addORM(RecordQuests(2, 5, 9, "Item_Quest_Helmet", "Cutscene_02_Helmet"))
        self.addORM(RecordQuests(2, 6, 12, "Item_Quest_Sword", "Cutscene_02_Sword"))
        self.addORM(RecordQuests(2, 7, 9, "Item_Quest_Gun", "Cutscene_02_Gun"))
        self.addORM(RecordQuests(2, 8, 15, "Item_Quest_Spaceship", "Cutscene_02_Spaceship"))
        pass
    pass
