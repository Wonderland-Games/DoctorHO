from Foundation.Database import Database

class DatabaseDefault(Database):
    def __init__(self):
        super(DatabaseDefault, self).__init__()
        self.addRecord(Param="DefaultMusicVolume", Debug=1.0, Master=1.0)
        self.addRecord(Param="DefaultSoundVolume", Debug=1.0, Master=1.0)
        self.addRecord(Param="DefaultArrowRadius", Debug=10.0, Master=10.0)
        self.addRecord(Param="DefaultMobileArrowRadius", Debug=15.0, Master=15.0)
        self.addRecord(Param="TransitionFadeInTime", Debug=0.25, Master=0.25)
        self.addRecord(Param="TransitionFadeOutTime", Debug=0.25, Master=0.25)
        self.addRecord(Param="AutoSaveonWillTerminate", Debug=True, Master=True)
        self.addRecord(Param="AutoSaveWillResignActive", Debug=True, Master=True)
        self.addRecord(Param="AutoSaveTransition", Debug=True, Master=True)
        pass
    pass
