from Foundation.Database import Database

class DatabaseDemons(Database):
    def __init__(self):
        super(DatabaseDemons, self).__init__()
        self.addRecord(DemonName="Loading", GroupName="Loading", ObjectName="Demon_Loading")
        self.addRecord(DemonName="Lobby", GroupName="Lobby", ObjectName="Demon_Lobby")
        self.addRecord(DemonName="GameArea", GroupName="GameArea", ObjectName="Demon_GameArea")
        self.addRecord(DemonName="FinalStage", GroupName="FinalStage", ObjectName="Demon_FinalStage")
        self.addRecord(DemonName="MissClick", GroupName="MissClick", ObjectName="Demon_MissClick")
        self.addRecord(DemonName="AdvertisingScene", GroupName="Advertising", ObjectName="Demon_AdvertisingScene")
        self.addRecord(DemonName="QuestBackpack", GroupName="QuestBackpack", ObjectName="Demon_QuestBackpack")
        self.addRecord(DemonName="Cutscene", GroupName="Cutscene", ObjectName="Demon_Cutscene")
        self.addRecord(DemonName="PopUp", GroupName="PopUp", ObjectName="Demon_PopUp")
        self.addRecord(DemonName="Header", GroupName="Header", ObjectName="Demon_Header")
        self.addRecord(DemonName="GameHeader", GroupName="GameHeader", ObjectName="Demon_GameHeader")
        pass
    pass
