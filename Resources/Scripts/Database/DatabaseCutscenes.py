from Foundation.Database import Database

class DatabaseCutscenes(Database):
    def __init__(self):
        super(DatabaseCutscenes, self).__init__()
        self.addRecord(CutsceneId="Intro", CutsceneGroupName="Intro", CutsceneMovies=[])
        pass
    pass
