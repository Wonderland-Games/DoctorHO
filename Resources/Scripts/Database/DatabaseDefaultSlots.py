from Foundation.Database import Database

class DatabaseDefaultSlots(Database):
    def __init__(self):
        super(DatabaseDefaultSlots, self).__init__()
        self.addRecord(SceneName="Loading", DefaultSlot="DefaultSlots_Loading")
        self.addRecord(SceneName="Lobby", DefaultSlot="DefaultSlots_Lobby")
        self.addRecord(SceneName="GameArea", DefaultSlot="DefaultSlots_GameArea")
        self.addRecord(SceneName="Advertising", DefaultSlot="DefaultSlots_Advertising")
        self.addRecord(SceneName="QuestBackpack", DefaultSlot="DefaultSlots_QuestBackpack")
        self.addRecord(SceneName="Cutscene", DefaultSlot="DefaultSlots_Cutscene")
        pass
    pass
