from Foundation.Database import Database

class DatabaseScenes(Database):
    def __init__(self):
        super(DatabaseScenes, self).__init__()
        self.addRecord(SceneName="Loading", DefaultScene="Loading", BaseScene="Loading", SlotName="Loading", SceneType="Scene", GroupName="Loading", GameScene=0)
        self.addRecord(SceneName="Lobby", DefaultScene="Lobby", BaseScene="Lobby", SlotName="Lobby", SceneType="Scene", GroupName="Lobby", GameScene=0)
        self.addRecord(SceneName="GameArea", DefaultScene="GameArea", BaseScene="GameArea", SlotName="GameArea", SceneType="Scene", GroupName="GameArea", GameScene=0)
        self.addRecord(SceneName="QuestBackpack", DefaultScene="QuestBackpack", BaseScene="QuestBackpack", SlotName="QuestBackpack", SceneType="Scene", GroupName="QuestBackpack", GameScene=0)
        self.addRecord(SceneName="Cutscene", DefaultScene="Cutscene", BaseScene="Cutscene", SlotName="Cutscene", SceneType="Scene", GroupName="Cutscene", GameScene=0)
        pass
    pass
