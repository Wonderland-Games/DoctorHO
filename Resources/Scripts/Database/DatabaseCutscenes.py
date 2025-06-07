from Foundation.Database import Database

class DatabaseCutscenes(Database):
    def __init__(self):
        super(DatabaseCutscenes, self).__init__()
        self.addRecord(CutsceneId="Intro", CutsceneGroupName="Intro", CutsceneMovies=[])
        self.addRecord(CutsceneId="Cutscene_01_Armor", CutsceneGroupName="Cutscene_01", CutsceneMovies=["Movie2_Armor_Play_1", "Movie2_Armor_Loop_1", "Movie2_Armor_Play_2", "Movie2_Armor_Loop_2"])
        self.addRecord(CutsceneId="Cutscene_01_Helmet", CutsceneGroupName="Cutscene_01", CutsceneMovies=["Movie2_Helmet_Play_1", "Movie2_Helmet_Loop_1", "Movie2_Helmet_Play_2", "Movie2_Helmet_Loop_2"])
        self.addRecord(CutsceneId="Cutscene_01_Bust", CutsceneGroupName="Cutscene_01", CutsceneMovies=["Movie2_Bust_Play_1", "Movie2_Bust_Loop_1", "Movie2_Bust_Play_2", "Movie2_Bust_Loop_2"])
        self.addRecord(CutsceneId="Cutscene_02_Armor", CutsceneGroupName="Cutscene_02", CutsceneMovies=["Movie2_Armor_Play_1", "Movie2_Armor_Loop_1", "Movie2_Armor_Play_2", "Movie2_Armor_Loop_2"])
        self.addRecord(CutsceneId="Cutscene_02_Helmet", CutsceneGroupName="Cutscene_02", CutsceneMovies=["Movie2_Helmet_Play_1", "Movie2_Helmet_Loop_1", "Movie2_Helmet_Play_2", "Movie2_Helmet_Loop_2"])
        self.addRecord(CutsceneId="Cutscene_02_Sword", CutsceneGroupName="Cutscene_02", CutsceneMovies=["Movie2_Sword_Play_1", "Movie2_Sword_Loop_1", "Movie2_Sword_Play_2", "Movie2_Sword_Loop_2"])
        self.addRecord(CutsceneId="Cutscene_02_Gun", CutsceneGroupName="Cutscene_02", CutsceneMovies=["Movie2_Gun_Play_1", "Movie2_Gun_Loop_1", "Movie2_Gun_Play_2", "Movie2_Gun_Loop_2"])
        self.addRecord(CutsceneId="Cutscene_02_Spaceship", CutsceneGroupName="Cutscene_02", CutsceneMovies=["Movie2_Spaceship_Play_1", "Movie2_Spaceship_Loop_1", "Movie2_Spaceship_Play_2", "Movie2_Spaceship_Loop_2"])
        pass
    pass
