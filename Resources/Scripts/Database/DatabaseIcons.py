from Foundation.Database import Database

class DatabaseIcons(Database):
    def __init__(self):
        super(DatabaseIcons, self).__init__()
        class RecordIcons(object):
            def __init__(self, Prototype, Size, Name, Type, Params={}):
                self.Prototype = Prototype
                self.Size = Size
                self.Name = Name
                self.Type = Type
                self.Params = Params
                pass
            pass

        self.addORM(RecordIcons("Heart", None, "Heart", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="Heart", Play=False, Loop=False)))
        self.addORM(RecordIcons("Heart_Big", None, "Heart_Big", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="Heart_Big", Play=False, Loop=False)))
        self.addORM(RecordIcons("PopUpButton", "Close", "PopUpButton", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="PopUpButton_Close", Play=False, Loop=False)))
        self.addORM(RecordIcons("PopUpButton", "Back", "PopUpButton", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="PopUpButton_Back", Play=False, Loop=False)))
        self.addORM(RecordIcons("Settings", None, "Settings", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="Settings", Play=False, Loop=False)))
        self.addORM(RecordIcons("Hint", None, "Hint", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="Hint", Play=False, Loop=False)))
        self.addORM(RecordIcons("Sound", None, "Sound", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="Sound", Play=False, Loop=False)))
        self.addORM(RecordIcons("Music", None, "Music", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="Music", Play=False, Loop=False)))
        self.addORM(RecordIcons("Vibration", None, "Vibration", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="Vibration", Play=False, Loop=False)))
        self.addORM(RecordIcons("Languages", None, "Languages", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="Languages", Play=False, Loop=False)))
        self.addORM(RecordIcons("Support", None, "Support", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="Support", Play=False, Loop=False)))
        self.addORM(RecordIcons("Credits", None, "Credits", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="Credits", Play=False, Loop=False)))
        self.addORM(RecordIcons("Lobby", None, "Lobby", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="Lobby", Play=False, Loop=False)))
        self.addORM(RecordIcons("Advertising", "Medium", "Advertising", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="Advertising_Medium", Play=False, Loop=False)))
        self.addORM(RecordIcons("Advertising", "Small", "Advertising", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="Advertising_Small", Play=False, Loop=False)))
        self.addORM(RecordIcons("Backpack", None, "Backpack", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="Backpack", Play=False, Loop=False)))
        self.addORM(RecordIcons("InvestigationBoard", None, "InvestigationBoard", "Movie2", Params=dict(ResourceMovie="Movie2_IconStore", CompositionName="InvestigationBoard", Play=False, Loop=False)))

        self.makeIndexer("Prototype")
        pass
    pass
