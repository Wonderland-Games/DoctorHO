from Foundation.Database import Database

class DatabaseLanguages(Database):
    def __init__(self):
        super(DatabaseLanguages, self).__init__()
        class RecordLanguages(object):
            def __init__(self, TextId, Language):
                self.TextId = TextId
                self.Language = Language
                pass
            pass

        self.addORM(RecordLanguages("ID_Language_English", "en"))
        self.addORM(RecordLanguages("ID_Language_Ukrainian", "uk"))
        self.addORM(RecordLanguages("ID_Language_Russian", "ru"))
        pass
    pass
