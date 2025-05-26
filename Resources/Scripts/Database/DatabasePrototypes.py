from Foundation.Database import Database

class DatabasePrototypes(Database):
    def __init__(self):
        super(DatabasePrototypes, self).__init__()
        class RecordPrototypes(object):
            def __init__(self, Name, Color, Size, Prototype, ObjectName, Type, Icon={}):
                self.Name = Name
                self.Color = Color
                self.Size = Size
                self.Prototype = Prototype
                self.ObjectName = ObjectName
                self.Type = Type
                self.Icon = Icon
                pass
            pass

        self.addORM(RecordPrototypes("PopUpBackground", None, "Normal", "Movie2_PopUpBackground_Normal", "Movie2_PopUpBackground_Normal", None, {}))
        self.addORM(RecordPrototypes("PopUpBackground", None, "Big", "Movie2_PopUpBackground_Big", "Movie2_PopUpBackground_Big", None, {}))
        self.addORM(RecordPrototypes("PopUpButton", None, "Close", "Movie2Button_PopUpButton", "Movie2Button_PopUpButton", None, Icon=dict(Slot="icon", Prototype="PopUpButton", Size="Close")))
        self.addORM(RecordPrototypes("PopUpButton", None, "Back", "Movie2Button_PopUpButton", "Movie2Button_PopUpButton", None, Icon=dict(Slot="icon", Prototype="PopUpButton", Size="Back")))
        self.addORM(RecordPrototypes("Settings", None, None, "Movie2Button_Circle", "Movie2Button_Circle", None, Icon=dict(Slot="icon", Prototype="Settings")))
        self.addORM(RecordPrototypes("Hint", None, None, "Movie2Button_Circle", "Movie2Button_Circle", None, Icon=dict(Slot="icon", Prototype="Hint")))
        self.addORM(RecordPrototypes("HintCounter", None, None, "Movie2_HintCounter", "Movie2_HintCounter", None, {}))
        self.addORM(RecordPrototypes("HintAdIcon", None, None, "Movie2_Circle_S", "Movie2_Circle_S", None, Icon=dict(Slot="icon", Prototype="Advertising", Size="Small")))
        self.addORM(RecordPrototypes("Settings_Sound", None, None, "Movie2Checkbox_Circle", "Movie2Checkbox_Circle", None, Icon=dict(Slot="icon", Prototype="Sound")))
        self.addORM(RecordPrototypes("Settings_Music", None, None, "Movie2Checkbox_Circle", "Movie2Checkbox_Circle", None, Icon=dict(Slot="icon", Prototype="Music")))
        self.addORM(RecordPrototypes("Settings_Vibration", None, None, "Movie2Checkbox_Circle", "Movie2Checkbox_Circle", None, Icon=dict(Slot="icon", Prototype="Vibration")))
        self.addORM(RecordPrototypes("Settings_Languages", None, None, "Movie2Button_Rectangle", "Movie2Button_Rectangle", None, Icon=dict(Slot="icon", Prototype="Languages")))
        self.addORM(RecordPrototypes("Settings_Support", None, None, "Movie2Button_Rectangle", "Movie2Button_Rectangle", None, Icon=dict(Slot="icon", Prototype="Support")))
        self.addORM(RecordPrototypes("Settings_Credits", None, None, "Movie2Button_Rectangle", "Movie2Button_Rectangle", None, Icon=dict(Slot="icon", Prototype="Credits")))
        self.addORM(RecordPrototypes("Settings_Lobby", None, None, "Movie2Button_Rectangle", "Movie2Button_Rectangle", None, Icon=dict(Slot="icon", Prototype="Lobby")))
        self.addORM(RecordPrototypes("LevelLost_Icon", None, None, "Movie2_Circle", "Movie2_Circle", None, Icon=dict(Slot="icon", Prototype="Heart_Big")))
        self.addORM(RecordPrototypes("LevelLost_Ad", None, None, "Movie2Button_Rectangle_Green", "Movie2Button_Rectangle_Green", None, Icon=dict(Slot="icon", Prototype="Advertising", Size="Medium")))
        self.addORM(RecordPrototypes("LevelLost_Restart", None, None, "Movie2Button_Rectangle", "Movie2Button_Rectangle", None, {}))
        self.addORM(RecordPrototypes("LevelLost_Lobby", None, None, "Movie2Button_Rectangle", "Movie2Button_Rectangle", None, {}))
        self.addORM(RecordPrototypes("Languages_Buttons", None, None, "Movie2Button_Rectangle", "Movie2Button_Rectangle", None, {}))
        self.addORM(RecordPrototypes("LevelWon_Lobby", None, None, "Movie2Button_Rectangle", "Movie2Button_Rectangle", None, Icon=dict(Slot="icon", Prototype="Lobby")))
        self.addORM(RecordPrototypes("Lobby_Play", None, None, "Movie2Button_Rectangle_Green", "Movie2Button_Rectangle_Green", None, {}))
        self.addORM(RecordPrototypes("MissClickEffect", None, None, "Movie2_MissClickEffect", "Movie2_MissClickEffect", None, {}))
        self.addORM(RecordPrototypes("ItemBox", None, None, "Movie2_Square", "Movie2_Square", None, {}))
        self.addORM(RecordPrototypes("SearchItemsCorner", None, "Left", "Movie2_SearchItemsCorner_Left", "Movie2_SearchItemsCorner_Left", None, {}))
        self.addORM(RecordPrototypes("SearchItemsCorner", None, "Right", "Movie2_SearchItemsCorner_Right", "Movie2_SearchItemsCorner_Right", None, {}))
        self.addORM(RecordPrototypes("HeaderLivesBackground", None, None, "Movie2_HeaderLivesBackground", "Movie2_HeaderLivesBackground", None, {}))
        self.addORM(RecordPrototypes("LoadingBar", None, None, "Movie2ProgressBar_Loading", "Movie2ProgressBar_Loading", None, {}))
        self.addORM(RecordPrototypes("QuestItemReceived_Button", None, None, "Movie2Button_Rectangle_Green", "Movie2Button_Rectangle_Green", None, {}))
        self.addORM(RecordPrototypes("QuestBackpack", None, None, "Movie2Button_Square_256", "Movie2Button_Square_256", None, Icon=dict(Slot="icon", Prototype="Backpack")))
        self.addORM(RecordPrototypes("Lobby", None, None, "Movie2Button_Square_256", "Movie2Button_Square_256", None, Icon=dict(Slot="icon", Prototype="InvestigationBoard")))
        self.addORM(RecordPrototypes("Cutscene_Skip", None, None, "Movie2Button_Rectangle_Green", "Movie2Button_Rectangle_Green", None, {}))
        pass
    pass
