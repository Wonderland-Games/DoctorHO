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
        self.addORM(RecordLanguages("ID_Language_German", "de"))
        self.addORM(RecordLanguages("ID_Language_French", "fr"))
        self.addORM(RecordLanguages("ID_Language_Spanish", "es"))
        self.addORM(RecordLanguages("ID_Language_Italian", "it"))
        self.addORM(RecordLanguages("ID_Language_Portuguese", "pt"))
        self.addORM(RecordLanguages("ID_Language_Polish", "pl"))
        self.addORM(RecordLanguages("ID_Language_Romanian", "ro"))
        self.addORM(RecordLanguages("ID_Language_Turkish", "tr"))
        self.addORM(RecordLanguages("ID_Language_Chinese", "zh"))
        self.addORM(RecordLanguages("ID_Language_Japanese", "ja"))
        self.addORM(RecordLanguages("ID_Language_Swedish", "sv"))
        self.addORM(RecordLanguages("ID_Language_Dutch", "nl"))
        self.addORM(RecordLanguages("ID_Language_Hindi", "hi"))
        self.addORM(RecordLanguages("ID_Language_Indonesian", "id"))
        pass
    pass
