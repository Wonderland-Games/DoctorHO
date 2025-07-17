from Foundation.Database import Database

class DatabaseSceneSlots(Database):
    def __init__(self):
        super(DatabaseSceneSlots, self).__init__()
        self.addRecord(SceneName="Loading", SceneSlots="SceneSlots_Loading")
        self.addRecord(SceneName="Lobby", SceneSlots="SceneSlots_Lobby")
        self.addRecord(SceneName="GameArea", SceneSlots="SceneSlots_GameArea")
        self.addRecord(SceneName="FinalStage", SceneSlots="SceneSlots_FinalStage")
        self.addRecord(SceneName="Advertising", SceneSlots="SceneSlots_Advertising")
        self.addRecord(SceneName="QuestBackpack", SceneSlots="SceneSlots_QuestBackpack")
        self.addRecord(SceneName="Cutscene", SceneSlots="SceneSlots_Cutscene")
        pass
    pass
