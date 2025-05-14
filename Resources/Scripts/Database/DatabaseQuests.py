from Foundation.Database import Database

class DatabaseQuests(Database):
    def __init__(self):
        super(DatabaseQuests, self).__init__()
        class RecordQuests(object):
            def __init__(self, ChapterId, LevelId, ItemsCount, QuestItem):
                self.ChapterId = ChapterId
                self.LevelId = LevelId
                self.ItemsCount = ItemsCount
                self.QuestItem = QuestItem
                pass
            pass

        self.addORM(RecordQuests(1, 1, 5, "Item_Quest_Armor"))
        self.addORM(RecordQuests(1, 2, 8, "Item_Quest_Helmet"))
        self.addORM(RecordQuests(1, 3, 12, "Item_Quest_Bust"))
        self.addORM(RecordQuests(2, 4, 6, "Item_Quest_Armor"))
        self.addORM(RecordQuests(2, 5, 9, "Item_Quest_Helmet"))
        self.addORM(RecordQuests(2, 6, 12, "Item_Quest_Sword"))
        self.addORM(RecordQuests(2, 7, 9, "Item_Quest_Gun"))
        self.addORM(RecordQuests(2, 8, 15, "Item_Quest_Spaceship"))
        pass
    pass
