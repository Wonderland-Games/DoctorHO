from Foundation.Database import Database

class DatabaseCutscenes(Database):
    def __init__(self):
        super(DatabaseCutscenes, self).__init__()
        self.addRecord(CutsceneId="Intro", CutsceneGroupName="Intro", CutsceneMovies=[])
        self.addRecord(CutsceneId="Cutscene_01_Armor", CutsceneGroupName="Cutscene_01_Armor", CutsceneMovies=[])
        self.addRecord(CutsceneId="Cutscene_01_Helmet", CutsceneGroupName="Cutscene_01_Helmet", CutsceneMovies=[])
        self.addRecord(CutsceneId="Cutscene_01_Bust", CutsceneGroupName="Cutscene_01_Bust", CutsceneMovies=[])
        self.addRecord(CutsceneId="Cutscene_02_Armor", CutsceneGroupName="Cutscene_02_Armor", CutsceneMovies=[])
        self.addRecord(CutsceneId="Cutscene_02_Helmet", CutsceneGroupName="Cutscene_02_Helmet", CutsceneMovies=[])
        self.addRecord(CutsceneId="Cutscene_02_Sword", CutsceneGroupName="Cutscene_02_Sword", CutsceneMovies=[])
        self.addRecord(CutsceneId="Cutscene_02_Gun", CutsceneGroupName="Cutscene_02_Gun", CutsceneMovies=[])
        self.addRecord(CutsceneId="Cutscene_02_Spaceship", CutsceneGroupName="Cutscene_02_Spaceship", CutsceneMovies=[])
        pass
    pass
