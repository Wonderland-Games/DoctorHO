from Foundation.Database import Database

class DatabaseCutscenes(Database):
    def __init__(self):
        super(DatabaseCutscenes, self).__init__()
        self.addRecord(CutsceneId="Intro", CutsceneGroupName="Intro", CutsceneMovieName="Movie2_Cutscene", CutsceneMovies=["Movie2_Play_1", "Movie2_Loop_1", "Movie2_Play_2", "Movie2_Loop_2"])
        pass
    pass
