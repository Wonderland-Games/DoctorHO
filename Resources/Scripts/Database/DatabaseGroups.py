from Foundation.Database import Database

class DatabaseGroups(Database):
    def __init__(self):
        super(DatabaseGroups, self).__init__()
        self.addRecord(GroupName="Loading")
        self.addRecord(GroupName="Lobby")
        self.addRecord(GroupName="GameArea")
        self.addRecord(GroupName="Advertising")
        self.addRecord(GroupName="QuestBackpack")
        self.addRecord(GroupName="Cutscene")
        self.addRecord(GroupName="Fade")
        self.addRecord(GroupName="FadeUI")
        self.addRecord(GroupName="BlockInput")
        self.addRecord(GroupName="Background")
        self.addRecord(GroupName="UIStore")
        self.addRecord(GroupName="PopUp")
        self.addRecord(GroupName="Header")
        self.addRecord(GroupName="GameHeader")
        self.addRecord(GroupName="Banner")
        self.addRecord(GroupName="LevelCards")
        self.addRecord(GroupName="QuestItemStore")
        self.addRecord(GroupName="01_AncientEgypt")
        self.addRecord(GroupName="01_AncientGreece")
        self.addRecord(GroupName="01_AncientRome")
        self.addRecord(GroupName="02_Europa")
        self.addRecord(GroupName="02_Mars")
        self.addRecord(GroupName="02_Titan")
        self.addRecord(GroupName="02_Venus")
        self.addRecord(GroupName="02_Moon")
        self.addRecord(GroupName="Intro")
        pass
    pass
