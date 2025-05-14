from Foundation.Group import Group

class GroupLevelCards(Group):
    Category = "Resources"

    def _getLayerParams(self):
        params = { "Size" : (2736,1536), "Type" : "Layer2D", "Name" : "Layer2D_Main", "Main" : True }
        return params
        pass

    def _onLoader(self):
        self.createLayer( "Layer2D_Main", Type = "Layer2D", Size = (2736, 1536), Main = True )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientEgypt_Active" , ResourceMovie = "Movie2_LevelCards", CompositionName = "01_AncientEgypt_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientEgypt_Unlocking" , ResourceMovie = "Movie2_LevelCards", CompositionName = "01_AncientEgypt_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientEgypt_Blocked" , ResourceMovie = "Movie2_LevelCards", CompositionName = "01_AncientEgypt_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientGreece_Active" , ResourceMovie = "Movie2_LevelCards", CompositionName = "01_AncientGreece_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientGreece_Unlocking" , ResourceMovie = "Movie2_LevelCards", CompositionName = "01_AncientGreece_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientGreece_Blocked" , ResourceMovie = "Movie2_LevelCards", CompositionName = "01_AncientGreece_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientRome_Active" , ResourceMovie = "Movie2_LevelCards", CompositionName = "01_AncientRome_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientRome_Unlocking" , ResourceMovie = "Movie2_LevelCards", CompositionName = "01_AncientRome_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_01_AncientRome_Blocked" , ResourceMovie = "Movie2_LevelCards", CompositionName = "01_AncientRome_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Europa_Active" , ResourceMovie = "Movie2_LevelCards", CompositionName = "02_Europa_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Europa_Unlocking" , ResourceMovie = "Movie2_LevelCards", CompositionName = "02_Europa_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Europa_Blocked" , ResourceMovie = "Movie2_LevelCards", CompositionName = "02_Europa_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Mars_Active" , ResourceMovie = "Movie2_LevelCards", CompositionName = "02_Mars_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Mars_Unlocking" , ResourceMovie = "Movie2_LevelCards", CompositionName = "02_Mars_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Mars_Blocked" , ResourceMovie = "Movie2_LevelCards", CompositionName = "02_Mars_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Titan_Active" , ResourceMovie = "Movie2_LevelCards", CompositionName = "02_Titan_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Titan_Unlocking" , ResourceMovie = "Movie2_LevelCards", CompositionName = "02_Titan_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Titan_Blocked" , ResourceMovie = "Movie2_LevelCards", CompositionName = "02_Titan_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Venus_Active" , ResourceMovie = "Movie2_LevelCards", CompositionName = "02_Venus_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Venus_Unlocking" , ResourceMovie = "Movie2_LevelCards", CompositionName = "02_Venus_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Venus_Blocked" , ResourceMovie = "Movie2_LevelCards", CompositionName = "02_Venus_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Moon_Active" , ResourceMovie = "Movie2_LevelCards", CompositionName = "02_Moon_Active"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Moon_Unlocking" , ResourceMovie = "Movie2_LevelCards", CompositionName = "02_Moon_Unlocking"  )
        self.addPrototype( "Movie2", Name = "Movie2_02_Moon_Blocked" , ResourceMovie = "Movie2_LevelCards", CompositionName = "02_Moon_Blocked"  )
        self.addPrototype( "Movie2", Name = "Movie2_ChapterSlots_Ancient" , ResourceMovie = "Movie2_LevelCards", CompositionName = "ChapterSlots_Ancient"  )
        self.addPrototype( "Movie2", Name = "Movie2_ChapterSlots_SolarSystem" , ResourceMovie = "Movie2_LevelCards", CompositionName = "ChapterSlots_SolarSystem"  )
        self.addPrototype( "Movie2", Name = "Movie2_Card_Ancient" , ResourceMovie = "Movie2_LevelCards", CompositionName = "Card_Ancient"  )
        self.addPrototype( "Movie2", Name = "Movie2_Card_Space" , ResourceMovie = "Movie2_LevelCards", CompositionName = "Card_Space"  )
        self.addPrototype( "Movie2", Name = "Movie2_QuestIndicator" , ResourceMovie = "Movie2_LevelCards", CompositionName = "QuestIndicator"  )
        self.addPrototype( "Movie2ProgressBar", Name = "Movie2ProgressBar_Quest", ResourceMovie = "Movie2_LevelCards", CompositionNameIdle = "Quest_Idle", CompositionNameOver = "Quest_Over", CompositionNameProgress = "Quest_Progress", CompositionNameBlock = "Quest_Block", CompositionNameFullProgress = "Quest_FullProgress", CompositionNameHolder = "Quest_Holder" )
        pass
    pass
