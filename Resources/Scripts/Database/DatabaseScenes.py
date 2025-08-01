from Foundation.Database import Database

class DatabaseScenes(Database):
    def __init__(self):
        super(DatabaseScenes, self).__init__()
        self.addRecord(SceneName="Loading", DefaultScene="Loading", BaseScene="Loading", SlotName="Loading", SceneType="Scene", GroupName="Loading", GameScene=0)
        self.addRecord(SceneName="Lobby", DefaultScene="Lobby", BaseScene="Lobby", SlotName="Lobby", SceneType="Scene", GroupName="Lobby", GameScene=0)
        self.addRecord(SceneName="01_AncientEgypt", DefaultScene="GameArea", BaseScene="GameArea", SlotName="Level", SceneType="Scene", GroupName="01_AncientEgypt", GameScene=0)
        self.addRecord(SceneName="01_AncientGreece", DefaultScene="GameArea", BaseScene="GameArea", SlotName="Level", SceneType="Scene", GroupName="01_AncientGreece", GameScene=0)
        self.addRecord(SceneName="01_AncientRome", DefaultScene="GameArea", BaseScene="GameArea", SlotName="Level", SceneType="Scene", GroupName="01_AncientRome", GameScene=0)
        self.addRecord(SceneName="02_Europa", DefaultScene="GameArea", BaseScene="GameArea", SlotName="Level", SceneType="Scene", GroupName="02_Europa", GameScene=0)
        self.addRecord(SceneName="02_Mars", DefaultScene="GameArea", BaseScene="GameArea", SlotName="Level", SceneType="Scene", GroupName="02_Mars", GameScene=0)
        self.addRecord(SceneName="02_Titan", DefaultScene="GameArea", BaseScene="GameArea", SlotName="Level", SceneType="Scene", GroupName="02_Titan", GameScene=0)
        self.addRecord(SceneName="02_Venus", DefaultScene="GameArea", BaseScene="GameArea", SlotName="Level", SceneType="Scene", GroupName="02_Venus", GameScene=0)
        self.addRecord(SceneName="02_Moon", DefaultScene="GameArea", BaseScene="GameArea", SlotName="Level", SceneType="Scene", GroupName="02_Moon", GameScene=0)
        self.addRecord(SceneName="QuestBackpack", DefaultScene="QuestBackpack", BaseScene="QuestBackpack", SlotName="QuestBackpack", SceneType="Scene", GroupName="QuestBackpack", GameScene=0)
        self.addRecord(SceneName="Cutscene", DefaultScene="Cutscene", BaseScene="Cutscene", SlotName="Cutscene", SceneType="Scene", GroupName="Cutscene", GameScene=0)
        pass
    pass
