from Foundation.Database import Database

class DatabaseDebugNotifications(Database):
    def __init__(self):
        super(DatabaseDebugNotifications, self).__init__()
        self.addRecord(Identity="onLevelStart")
        self.addRecord(Identity="onLevelEnd")
        self.addRecord(Identity="onLevelMissClicked")
        self.addRecord(Identity="onLevelHintClicked")
        self.addRecord(Identity="onLevelLivesDecrease")
        self.addRecord(Identity="onLevelLivesChanged")
        self.addRecord(Identity="onPopUpShow")
        self.addRecord(Identity="onPopUpHide")
        self.addRecord(Identity="onPopUpShowEnd")
        self.addRecord(Identity="onPopUpHideEnd")
        pass
    pass
